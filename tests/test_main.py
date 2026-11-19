"""Small deterministic checks for Mochi's v0.3 world."""

import random
import sys
import unittest
from datetime import datetime
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import main  # noqa: E402


class WorldTests(unittest.TestCase):
    def test_seasons_cover_the_year(self):
        self.assertEqual(main.get_season(1), "winter")
        self.assertEqual(main.get_season(4), "spring")
        self.assertEqual(main.get_season(7), "summer")
        self.assertEqual(main.get_season(10), "autumn")

    def test_device_time_periods(self):
        self.assertEqual(main.get_time_period(6), "Early morning")
        self.assertEqual(main.get_time_period(10), "Morning")
        self.assertEqual(main.get_time_period(14), "Afternoon")
        self.assertEqual(main.get_time_period(20), "Evening")
        self.assertEqual(main.get_time_period(1), "Late night")
        display = main.get_local_time_display(datetime(2026, 11, 1, 20, 5))
        self.assertEqual(display, "🕒 20:05 Evening")

    def test_live_weather_payload_is_reduced_to_world_data(self):
        payload = {
            "current_condition": [{
                "temp_C": "9",
                "weatherCode": "296",
                "weatherDesc": [{"value": "Light rain"}],
            }],
            "nearest_area": [{"areaName": [{"value": "London"}]}],
        }
        report = main.parse_live_weather(payload)
        self.assertEqual(report["weather_key"], "rain")
        self.assertEqual(report["temperature_c"], "9")
        self.assertEqual(report["location"], "London")

    def test_box_blink_changes_only_the_eyes(self):
        expected = main.BOX_CAT.replace("( o.o )", "( -.- )")
        self.assertEqual(main.BOX_CAT_BLINK, expected)

    def test_bird_drawing_is_recognisable_ascii(self):
        self.assertIn("( o)>", main.BIRD_SCENE)
        self.assertTrue(all(ord(character) < 128 for character in main.BIRD_SCENE))

    def test_box_blink_interval_is_three_to_five_seconds(self):
        self.assertEqual(main.BOX_BLINK_MIN_SECONDS, 3.0)
        self.assertEqual(main.BOX_BLINK_MAX_SECONDS, 5.0)

    def test_event_file_loads(self):
        events, warning = main.load_events()
        self.assertIsNone(warning)
        self.assertGreaterEqual(len(events), 10)

    def test_conditions_filter_events(self):
        world = main.World(season_key="winter", weather_key="snow")
        spring_event = {
            "id": "spring_only",
            "weight": 1,
            "messages": ["hello"],
            "conditions": {"seasons": ["spring"]},
        }
        snow_event = {
            "id": "snow_only",
            "weight": 1,
            "messages": ["hello"],
            "conditions": {"weather": ["snow"]},
        }
        self.assertFalse(main.event_matches(spring_event, world))
        self.assertTrue(main.event_matches(snow_event, world))

    def test_weighted_choice_returns_an_eligible_event(self):
        world = main.World(season_key="summer", weather_key="clear")
        events = [
            {
                "id": "winter",
                "weight": 100,
                "messages": ["no"],
                "conditions": {"seasons": ["winter"]},
            },
            {
                "id": "summer",
                "weight": 1,
                "messages": ["yes"],
                "conditions": {"seasons": ["summer"]},
            },
        ]
        chosen = main.choose_event(events, world, random.Random(3))
        self.assertEqual(chosen["id"], "summer")

    def test_treasures_do_not_duplicate(self):
        world = main.World(season_key="summer", weather_key="clear")
        treasure = {"symbol": "🎀", "name": "short ribbon"}
        self.assertTrue(main.add_treasure(world, treasure))
        self.assertFalse(main.add_treasure(world, treasure))
        self.assertEqual(len(world.treasures), 1)


if __name__ == "__main__":
    unittest.main()
