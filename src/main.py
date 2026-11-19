"""Mochi: a small, gentle terminal companion."""

from __future__ import annotations

import json
import os
import random
import sys
import time
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from threading import Event, Thread
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


MOCHI_AWAKE = r""" /\_/\
( o.o )
 > ^ <
 /   \
 \_v_/"""

MOCHI_BLINK = r""" /\_/\
( -.- )
 > ^ <
 /   \
 \_v_/"""

MOCHI_HAPPY = r""" /\_/\
( ^.^ )
 > ^ <
 /   \
 \_v_/"""

BOX_CAT = r"""   /\_/\
  ( o.o )
 /|  ^  |\
|_______|"""

BOX_CAT_BLINK = r"""   /\_/\
  ( -.- )
 /|  ^  |\
|_______|"""

BREAD_CAT = r"""  /\_/\
 ( -.- )
 /     \
(_______)"""

BIRD_SCENE = r"""       __
   ___( o)>
   \ <_. )
    `---'
     ^ ^"""

BOX_BLINK_MIN_SECONDS = 3.0
BOX_BLINK_MAX_SECONDS = 5.0

SCENES = {
    "bird": BIRD_SCENE,
    "mouse": "      ᘛ⁰̤ᕐᐇ",
    "butterfly": "       🦋",
    "leaf": "       🍂",
    "flower": "       🌼",
    "feather": "       🪶",
    "rain": "    │  │  │  ☂",
    "snow": "    ❄  ·  ❄  ·",
    "ribbon": "       🎀",
    "button": "       ◉",
    "box_cat": BOX_CAT,
    "bread_cat": BREAD_CAT,
    "bowl": "       🥣",
}

SEASONS = {
    "spring": ("🌱", "Spring"),
    "summer": ("☀", "Summer"),
    "autumn": ("🍂", "Autumn"),
    "winter": ("❄", "Winter"),
}

WEATHER = {
    "clear": ("☀", "clear"),
    "cloudy": ("☁", "cloudy"),
    "rain": ("☔", "soft rain"),
    "wind": ("🍃", "a light breeze"),
    "snow": ("❄", "quiet snow"),
}

WEATHER_WEIGHTS = {
    "spring": {"clear": 35, "cloudy": 25, "rain": 30, "wind": 10},
    "summer": {"clear": 55, "cloudy": 20, "rain": 15, "wind": 10},
    "autumn": {"clear": 25, "cloudy": 30, "rain": 25, "wind": 20},
    "winter": {"clear": 20, "cloudy": 30, "rain": 10, "wind": 10, "snow": 30},
}

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EVENTS_PATH = PROJECT_ROOT / "data" / "events" / "ambient.json"

# The fallback keeps Mochi playable if the data file is missing or malformed.
FALLBACK_EVENTS: List[Dict[str, Any]] = [
    {"id": "quiet", "weight": 45, "messages": []},
    {
        "id": "bird_visit",
        "weight": 20,
        "scene": "bird",
        "messages": ["A small bird pauses nearby. Mochi watches without hurrying it."],
    },
    {
        "id": "box_cat",
        "weight": 15,
        "scene": "box_cat",
        "messages": ["The box was empty. Now it is exactly full of Mochi."],
    },
    {
        "id": "ribbon",
        "weight": 20,
        "scene": "ribbon",
        "messages": ["Mochi tucks away a short ribbon that was already loose."],
        "treasure": {"symbol": "🎀", "name": "short ribbon"},
    },
]


@dataclass
class World:
    season_key: str
    weather_key: str
    treasures: List[Dict[str, str]] = field(default_factory=list)
    last_event_id: Optional[str] = None
    temperature_c: Optional[str] = None
    weather_description: Optional[str] = None
    weather_location: Optional[str] = None
    weather_is_live: bool = False

    @property
    def season_display(self) -> str:
        symbol, name = SEASONS[self.season_key]
        return f"{symbol} {name}"

    @property
    def weather_display(self) -> str:
        symbol, offline_name = WEATHER[self.weather_key]
        if not self.weather_is_live:
            return f"{symbol} {offline_name}"

        description = self.weather_description or offline_name
        temperature = f"{self.temperature_c}°C · " if self.temperature_c else ""
        location = f" · {self.weather_location}" if self.weather_location else ""
        return f"{symbol} {temperature}{description}{location}"


def configure_terminal() -> None:
    """Use UTF-8 where the stream supports reconfiguration."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass


def clear_screen() -> None:
    if sys.stdout.isatty():
        os.system("cls" if os.name == "nt" else "clear")


def get_season(month: Optional[int] = None) -> str:
    month = month or date.today().month
    if month in (3, 4, 5):
        return "spring"
    if month in (6, 7, 8):
        return "summer"
    if month in (9, 10, 11):
        return "autumn"
    return "winter"


def get_time_period(hour: int) -> str:
    if 5 <= hour < 9:
        return "Early morning"
    if 9 <= hour < 12:
        return "Morning"
    if 12 <= hour < 18:
        return "Afternoon"
    if 18 <= hour < 22:
        return "Evening"
    return "Late night"


def get_local_time_display(now: Optional[datetime] = None) -> str:
    now = now or datetime.now().astimezone()
    return f"🕒 {now:%H:%M} {get_time_period(now.hour)}"


def choose_weather(season: str, rng: random.Random = random) -> str:
    weights = WEATHER_WEIGHTS[season]
    return rng.choices(list(weights), weights=list(weights.values()), k=1)[0]


def create_world(rng: random.Random = random) -> World:
    season = get_season()
    return World(season_key=season, weather_key=choose_weather(season, rng))


def weather_key_from_report(code: Any, description: str) -> str:
    """Translate wttr.in/WorldWeatherOnline conditions into Mochi's small set."""
    try:
        numeric_code = int(code)
    except (TypeError, ValueError):
        numeric_code = -1

    snow_codes = {
        179, 182, 227, 230, 317, 320, 323, 326, 329, 332,
        335, 338, 350, 362, 365, 368, 371, 374, 377, 392, 395,
    }
    rain_codes = {
        176, 185, 200, 263, 266, 281, 284, 293, 296, 299,
        302, 305, 308, 311, 314, 353, 356, 359, 386, 389,
    }
    cloudy_codes = {116, 119, 122, 143, 248, 260}
    if numeric_code in snow_codes:
        return "snow"
    if numeric_code in rain_codes:
        return "rain"
    if numeric_code in cloudy_codes:
        return "cloudy"
    if numeric_code == 113:
        return "clear"

    lower_description = description.lower()
    if any(word in lower_description for word in ("snow", "sleet", "blizzard", "ice")):
        return "snow"
    if any(word in lower_description for word in ("rain", "drizzle", "shower", "thunder")):
        return "rain"
    if any(word in lower_description for word in ("cloud", "overcast", "fog", "mist")):
        return "cloudy"
    return "clear"


def _first_api_value(container: Dict[str, Any], key: str) -> Optional[str]:
    values = container.get(key)
    if isinstance(values, list) and values and isinstance(values[0], dict):
        value = values[0].get("value")
        if isinstance(value, str) and value:
            return value
    return None


def parse_live_weather(payload: Any) -> Dict[str, str]:
    """Extract only the small amount of weather data Mochi displays."""
    if not isinstance(payload, dict):
        raise ValueError("weather response was not an object")
    if isinstance(payload.get("data"), dict):
        payload = payload["data"]

    conditions = payload.get("current_condition")
    if not isinstance(conditions, list) or not conditions or not isinstance(conditions[0], dict):
        raise ValueError("current weather was missing")
    current = conditions[0]
    description = _first_api_value(current, "weatherDesc") or "current weather"

    location = None
    areas = payload.get("nearest_area")
    if isinstance(areas, list) and areas and isinstance(areas[0], dict):
        location = _first_api_value(areas[0], "areaName")

    report = {
        "weather_key": weather_key_from_report(current.get("weatherCode"), description),
        "description": description,
    }
    temperature = current.get("temp_C")
    if isinstance(temperature, str) and temperature:
        report["temperature_c"] = temperature
    if location:
        report["location"] = location
    return report


def fetch_live_weather(location: Optional[str] = None, timeout: float = 5.0) -> Dict[str, str]:
    """Fetch current weather; an empty location lets wttr.in use approximate IP location."""
    location_path = quote(location.strip()) if location else ""
    url = f"https://wttr.in/{location_path}?format=j1"
    request = Request(url, headers={"User-Agent": "Mochi-terminal-companion/0.3"})
    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return parse_live_weather(payload)


def enable_live_weather(world: World) -> Optional[str]:
    """Ask before sharing an IP address, then apply live weather if available."""
    configured_location = os.environ.get("MOCHI_WEATHER_LOCATION", "").strip()
    if not configured_location:
        clear_screen()
        print("Mochi can check approximate local weather from wttr.in.")
        print("This sends this connection's public IP address to that weather service.")
        try:
            consent = input("Use live weather for this visit? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            consent = ""
        if consent not in ("y", "yes"):
            return None

    try:
        report = fetch_live_weather(configured_location or None)
    except (
        HTTPError,
        URLError,
        TimeoutError,
        OSError,
        json.JSONDecodeError,
        ValueError,
    ):
        return "Live weather is resting, so Mochi is using a seasonal sky instead."

    world.weather_key = report["weather_key"]
    world.temperature_c = report.get("temperature_c")
    world.weather_description = report["description"]
    world.weather_location = report.get("location") or configured_location or None
    world.weather_is_live = True
    return None


def _valid_event(event: Any) -> bool:
    if not isinstance(event, dict):
        return False
    if not isinstance(event.get("id"), str):
        return False
    if not isinstance(event.get("weight"), (int, float)) or event["weight"] <= 0:
        return False
    messages = event.get("messages", [])
    return isinstance(messages, list) and all(isinstance(message, str) for message in messages)


def load_events(path: Path = EVENTS_PATH) -> Tuple[List[Dict[str, Any]], Optional[str]]:
    """Load event content, returning safe defaults and a gentle warning on failure."""
    try:
        with path.open("r", encoding="utf-8") as event_file:
            payload = json.load(event_file)
        raw_events = payload.get("events") if isinstance(payload, dict) else None
        if not isinstance(raw_events, list):
            raise ValueError("the top-level 'events' value must be a list")
        events = [event for event in raw_events if _valid_event(event)]
        if not events:
            raise ValueError("no usable events were found")
        return events, None
    except (OSError, json.JSONDecodeError, ValueError) as error:
        warning = f"The event notes could not be read ({error}). A smaller world is being used."
        return FALLBACK_EVENTS.copy(), warning


def event_matches(event: Dict[str, Any], world: World) -> bool:
    conditions = event.get("conditions", {})
    if not isinstance(conditions, dict):
        return False
    seasons = conditions.get("seasons")
    weather = conditions.get("weather")
    if seasons is not None and world.season_key not in seasons:
        return False
    if weather is not None and world.weather_key not in weather:
        return False
    return True


def choose_event(
    events: Sequence[Dict[str, Any]],
    world: World,
    rng: random.Random = random,
    visible_only: bool = False,
) -> Optional[Dict[str, Any]]:
    eligible = [event for event in events if event_matches(event, world)]
    if visible_only:
        eligible = [event for event in eligible if event.get("messages")]

    # Avoid an immediate repeat when another eligible event exists.
    alternatives = [event for event in eligible if event["id"] != world.last_event_id]
    if alternatives:
        eligible = alternatives
    if not eligible:
        return None

    return rng.choices(eligible, weights=[event["weight"] for event in eligible], k=1)[0]


def draw_world(
    world: World,
    cat: str = MOCHI_AWAKE,
    message: Optional[str] = None,
    scene: Optional[str] = None,
) -> None:
    clear_screen()
    now = datetime.now().astimezone()
    world.season_key = get_season(now.month)
    print(
        f"{world.season_display}  ·  {get_local_time_display(now)}"
        f"  ·  {world.weather_display}\n"
    )
    if scene:
        print(SCENES.get(scene, scene))
        print()
    print(cat)
    if message:
        print(f"\n{message}")


def wait_for_enter(prompt: str = "\nPress Enter when you are ready...") -> None:
    try:
        input(prompt)
    except EOFError:
        pass


def wait_with_box_blinks(
    world: World,
    message: str,
    rng: random.Random = random,
) -> None:
    """Keep the box cat blinking until the player leaves the event."""
    stop_blinking = Event()
    prompt = "\nPress Enter when you are ready..."

    def draw_box(cat: str) -> None:
        draw_world(world, cat=cat, message=message)
        print(prompt, flush=True)

    def animate() -> None:
        while not stop_blinking.wait(
            rng.uniform(BOX_BLINK_MIN_SECONDS, BOX_BLINK_MAX_SECONDS)
        ):
            draw_box(BOX_CAT_BLINK)
            if stop_blinking.wait(0.18):
                return
            draw_box(BOX_CAT)

    draw_box(BOX_CAT)
    animation = Thread(target=animate, name="mochi-box-blink", daemon=True)
    animation.start()
    try:
        input()
    except EOFError:
        pass
    finally:
        stop_blinking.set()
        animation.join(timeout=0.25)


def blink(world: World, delay: float = 0.18) -> None:
    draw_world(world, MOCHI_BLINK)
    time.sleep(delay)
    draw_world(world, MOCHI_AWAKE)


def add_treasure(world: World, treasure: Any) -> bool:
    if not isinstance(treasure, dict):
        return False
    symbol, name = treasure.get("symbol"), treasure.get("name")
    if not isinstance(symbol, str) or not isinstance(name, str):
        return False
    if any(item["name"] == name for item in world.treasures):
        return False
    world.treasures.append({"symbol": symbol, "name": name})
    return True


def show_event(
    world: World,
    events: Sequence[Dict[str, Any]],
    rng: random.Random = random,
    visible_only: bool = False,
) -> bool:
    event = choose_event(events, world, rng, visible_only)
    if event is None:
        return False

    world.last_event_id = event["id"]
    messages = event.get("messages", [])
    if not messages:
        return False  # "Nothing happens" is an intentional ambient outcome.

    message = rng.choice(messages)
    found_something = add_treasure(world, event.get("treasure"))
    if found_something:
        message += " It joins the little things kept here for this visit."
    scene = event.get("scene")
    if scene == "box_cat":
        wait_with_box_blinks(world, message, rng)
        return True
    elif scene == "bread_cat":
        draw_world(world, cat=BREAD_CAT, message=message)
    else:
        draw_world(world, message=message, scene=scene)
    wait_for_enter()
    return True


def pet_mochi(world: World, rng: random.Random = random) -> None:
    draw_world(world, MOCHI_AWAKE, "You hold out a hand. Mochi considers it.")
    time.sleep(0.35)
    reactions = [
        "Mochi leans into the gentle scratch and begins to purr.",
        "Mochi closes both eyes for a moment, staying close.",
        "A small, pleased chirp. Mochi's tail curls beside you.",
    ]
    draw_world(world, MOCHI_HAPPY, rng.choice(reactions))
    wait_for_enter()


def feed_mochi(world: World, rng: random.Random = random) -> None:
    draw_world(world, MOCHI_AWAKE, "You set down a small snack.", "bowl")
    time.sleep(0.35)
    reactions = [
        "Mochi takes a careful bite, then another. There is no hurry.",
        "Mochi sniffs the snack thoughtfully, then settles down to eat.",
        "Mochi eats a little and leaves the rest for later.",
    ]
    draw_world(world, MOCHI_BLINK, rng.choice(reactions), "bowl")
    wait_for_enter()


def sit_together(world: World, rng: random.Random = random) -> None:
    thoughts = [
        "For a little while, nothing needs to happen.",
        "Mochi sits nearby. The room feels unhurried.",
        "You listen to the small sounds around you together.",
    ]
    draw_world(world, MOCHI_BLINK, "You sit together quietly.")
    time.sleep(0.7)
    draw_world(world, MOCHI_AWAKE, rng.choice(thoughts))
    wait_for_enter("\nPress Enter whenever you would like to get up...")


def show_treasures(world: World) -> None:
    draw_world(world, message="Little Things")
    if world.treasures:
        print()
        for item in world.treasures:
            print(f"  {item['symbol']}  {item['name']}")
        print("\nMochi chose these small things during this visit.")
    else:
        print("\n  The little shelf is empty for now, and that is all right.")
    print("  (They will not be saved until the memory update.)")
    wait_for_enter()


def read_choice() -> str:
    try:
        return input("\nChoose gently: ").strip().lower()
    except EOFError:
        return "6"


def draw_menu(world: World) -> None:
    draw_world(world)
    print(
        "\n"
        "  1. Pet Mochi\n"
        "  2. Offer a snack\n"
        "  3. Sit together\n"
        "  4. Look around\n"
        "  5. View Little Things\n"
        "  6. Leave for now"
    )


def main(rng: random.Random = random) -> None:
    configure_terminal()
    world = create_world(rng)
    events, warning = load_events()
    weather_warning = enable_live_weather(world)

    draw_world(world, MOCHI_BLINK)
    time.sleep(0.18)
    draw_world(world, message="Mochi notices you and blinks hello.")
    if warning:
        print(f"\n{warning}")
    if weather_warning:
        print(f"\n{weather_warning}")
    wait_for_enter()

    choices = {
        "1": lambda: pet_mochi(world, rng),
        "pet": lambda: pet_mochi(world, rng),
        "2": lambda: feed_mochi(world, rng),
        "feed": lambda: feed_mochi(world, rng),
        "3": lambda: sit_together(world, rng),
        "sit": lambda: sit_together(world, rng),
        "4": lambda: show_event(world, events, rng, visible_only=True),
        "look": lambda: show_event(world, events, rng, visible_only=True),
        "5": lambda: show_treasures(world),
        "things": lambda: show_treasures(world),
    }

    try:
        while True:
            # Ambient events stay occasional; Look around always finds a visible moment.
            if rng.random() < 0.22:
                show_event(world, events, rng)

            draw_menu(world)
            choice = read_choice()
            if choice in ("6", "leave", "quit", "q"):
                break
            action = choices.get(choice)
            if action:
                action()
            else:
                draw_world(world, message="Mochi waits. You can choose whenever you are ready.")
                wait_for_enter()
    except KeyboardInterrupt:
        pass

    draw_world(world, MOCHI_BLINK, "Mochi settles down. Come back whenever you like.")


if __name__ == "__main__":
    main()
