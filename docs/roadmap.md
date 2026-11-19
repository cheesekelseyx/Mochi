# Development Roadmap
This roadmap is provisional. Features may move between versions as the project develops. The goal is to release small, complete versions rather than build every feature at once.

## v0.1
Goal: create the smallest playable companion.

### Required
* Display the base ASCII cat.
* Show a simple text menu.
* Allow the player to:
  * pet the cat;
  * feed the cat;
  * sit together;
  * leave.
* Display simple reactions and short animations.
* Support Linux terminals and Windows PowerShell through Python.
* Keep all dialogue gentle and pressure-free.

### Base cat
```text
 /\_/\
( o.o )
 > ^ <
 /   \
 \_v_/
```
The base cat may not be redesigned unless there is an intentional art update.

## v0.2 —— Memory and Time
Goal: allow the companion to remember basic information.

### Features
* First-launch naming.
* JSON save file.
* Visit count.
* Last visit date.
* Basic action history.
* Morning, afternoon, evening, and late-night dialogue.
* Welcome-back messages.

### Skills required
* Python dictionaries;
* JSON reading and writing;
* `datetime`;
* file paths;
* basic error handling.

## v0.3 — A Small Living World
Goal: introduce environmental variation.

### Features
* Random ambient events.
* Basic seasons.
* Unicode weather and environmental symbols.
* Small visitors:
  * bird;
  * mouse;
  * butterfly represented with Unicode;
  * selected environmental objects.
* Box-cat event.
* Bread-cat event.
* Simple “Little Things” or “Treasures” display.

### Skills required
* Python `random`;
* weighted probabilities;
* event conditions;
* separating data from code;
* loading event text from JSON.

## v0.4 — Music and Atmosphere
Goal: make the terminal world feel more atmospheric.

### Features
* Optional original music.
* Music can be turned off.
* Different tracks for:
  * daytime;
  * night;
  * rain;
  * winter;
  * quiet sitting.
* Volume setting.
* Graceful fallback if audio playback is unavailable.

### Skills required
* audio file formats;
* Python audio library;
* background playback;
* settings files;
* cross-platform testing.

## v0.5 — Weather, Seasons, and Festivals
Goal: connect the small world to real time and optional real-world conditions.

### Features
* Device-local date and time.
* Seasonal scene changes.
* Festival event system.
* Examples:
  * 🌲 becomes 🎄 during Christmas;
  * snow scenes in winter;
  * autumn leaves;
  * selected culturally appropriate festival events.
* Optional weather API integration.
* Manual location or weather mode for privacy.
* Offline fallback when weather is unavailable.

### Skills required
* APIs;
* HTTP requests;
* environment variables;
* configuration files;
* time zones;
* privacy-conscious location design;
* error handling and caching.

## v0.6 — Temperament and Habits
Goal: give each cat a distinct behavioural identity.
### Features
* Hidden innate temperament.
* Behaviour tendencies such as:
  * curiosity;
  * sociability;
  * reflectiveness;
  * attachment to home;
  * playfulness;
  * interest in collecting.
* Player actions influence habits slowly.
* Innate temperament remains meaningful.
* Different cats receive different event weights.
* Personality is shown through behaviour, not statistics.
* No visible personality score screen.

### Example differences
A curious cat may:
* go outside more often;
* inspect unfamiliar objects;
* bring home more small treasures.

A reflective cat may:
* leave natural objects where they belong;
* speak more about what it observes;
* spend more time by the window.

A home-loving cat may:
* display indoor events more frequently;
* show detailed window scenes;
* enjoy tea, music, sleep, and quiet sitting.

### Skills required
* structured save data;
* weighted random selection;
* state machines or rule systems;
* behavioural modelling;
* data-driven event conditions;
* testing probability-based behaviour.

## v0.7 — Companion Agency
Goal: allow the cat to make small, understandable decisions.
### Features
* The player cannot directly choose what the cat collects.
* Objects have qualities such as:
  * natural;
  * lost;
  * temporary;
  * beautiful;
  * useful;
  * belonging to another living thing.
* The cat evaluates objects according to its temperament and current habits.
* The cat may:
  * collect an object;
  * observe it;
  * leave it;
  * mention it later;
  * give it to the player;
  * forget about it.
* Decisions should feel consistent without becoming completely predictable.

### Example
A fallen leaf appears.
Possible outcomes:
* a curious cat brings it home;
* a reflective cat leaves it beneath the tree;
* a playful cat bats it around and then lets it blow away;
* a home-loving cat watches it through the window.

### Skills required
* rule-based decision systems;
* scoring and weighting;
* event context;
* decision logging;
* balancing deterministic rules with randomness.

## v0.8 — Rooms, Windows, and Detailed Scenes
Goal: give quieter personalities equally rich content.
### Features
* Multiple indoor scenes.
* More complex window ASCII art.
* Weather visible through the window.
* Indoor objects and seasonal decorations.
* Cats that collect fewer objects receive more observational and conversational content.
* Scene selection depends on temperament, time, weather, and recent events.

## v0.9 — Language and Content Expansion
### Features
* Separate dialogue files by language.
* English and Arabic support may be explored.
* Text direction and terminal compatibility testing.
* Community dialogue packs.
* Additional festivals and regional content.
* Accessibility settings.

## v1.0 — Complete Terminal Companion
A stable cross-platform release containing:

* a complete core interaction loop;
* save files;
* time and seasonal systems;
* optional music;
* random events;
* temperament and habits;
* companion agency;
* collections and observational alternatives;
* Linux, macOS, and Windows support;
* installation documentation;
* tests and release packaging.

---

## Future possibilities
These ideas are not commitments:
* plugin-based event packs;
* user-created dialogue;
* additional companion species;
* custom music packs;
* richer terminal interfaces;
* distributable executables;
* package installation through `pip`;
* open-source community contributions.
