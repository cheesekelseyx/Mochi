# architecture.md

## Current Architecture Goal
The project should begin simply and become modular only when features require it.
Do not create every module in advance.

## Suggested early structure
```text
project-root/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── vision.md
│   ├── roadmap.md
│   ├── features.md
│   ├── ideas.md
│   ├── architecture.md
│   └── design.md
│   └── styleguide.md
├── src/
│   └── main.py
├── assets/
│   ├── ascii/
│   └── music/
├── data/
│   ├── dialogues/
│   └── events/
└── tests/
```

## Possible later structure
```text
src/
├── main.py
├── cat.py
├── state.py
├── interactions.py
├── animation.py
├── event_engine.py
├── personality.py
├── decisions.py
├── save.py
├── time_system.py
├── weather.py
├── music.py
├── ui.py
└── paths.py
```

## Responsibilities
### `main.py`
Starts the program and connects the systems.
It should not contain all game logic.

### `cat.py`
Represents the cat and its current state.
Possible information:
* name;
* current expression;
* current action;
* temperament;
* habits;
* recent experiences.

### `state.py`
Stores the overall game state in memory.

### `interactions.py`
Handles player actions such as pet, feed, play, and sit together.

### `event_engine.py`
Finds events whose conditions are currently valid and chooses among them using weighted probabilities.

### `personality.py`
Defines temperament and habit dimensions.
It calculates behavioural tendencies but does not display raw scores.

### `decisions.py`
Allows the cat to evaluate an object or event and select a response.
Possible responses:
* collect;
* observe;
* leave;
* play;
* discuss;
* ignore.

### `save.py`
Loads, validates, and writes save data.

### `time_system.py`
Translates the current device time into useful game periods and seasons.

### `weather.py`
Retrieves optional weather information and provides offline fallbacks.

### `music.py`
Controls optional audio playback.(Possible)

### `ui.py`
Displays the terminal scene, menus, messages, and animations.

## Data-driven content
Dialogue and events should gradually move outside Python files.

```text
data/
├── dialogues/
│   ├── general.json
│   ├── night.json
│   └── weather.json
└── events/
    ├── bird.json
    ├── feather.json
    ├── leaf.json
    └── box.json
```