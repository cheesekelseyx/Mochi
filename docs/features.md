# Mochi features
This document records the possible features of mochi. Features are divided into different stages so that the first version remains managable. 

## Version 0.1
The first version should contain only the basic terminal companion. 

 /\_/\
( o.o )
 > ^ <
 /   \
 \_v_/


 /\_/\
( o.o )
 > ^  \  
 (_____)


 /\_/\
( -.- )     /
_(_  <  )--'

## Core Interaction
### Pet
The player pets the cat.
Possible reactions depend on mood, time, habits, and temperament.
Petting should not produce visible points.
Examples:
* delayed purring;
* closing its eyes;
* leaning closer;
* looking surprised;
* remaining quietly nearby.

### Feed (possible)
The player offers food. Feeding is an affectionate interaction, not a survival requirement. The cat does not starve if the player is absent.
Possible reactions:
* eating immediately;
* inspecting the food;
* sharing attention with a visiting mouse;
* saving the food for later.

### Play
The player invites the cat to play.
Repeated play may gradually strengthen playful habits, but it does not erase the cat's innate temperament.
Possible events:
* string;
* rolling object;
* box;
* plastic bag;
* jumping;
* sudden loss of interest.

### Sit Together
The player and cat remain together without a task.
The interaction must allow the player to leave at any time.
This interaction may include:
* silence;
* purring;
* a small tail movement;
* music;
* a short observation;
* looking through the window.

### Look Outside
The player observes the world with the cat.
This interaction may become more common for quiet or home-loving cats.
Possible content:
* weather;
* time of day;
* moon;
* birds;
* trees;
* falling leaves;
* distant lights;
* detailed ASCII scenery.

## Time System
The program reads the device's local time.
Suggested periods:
* early morning;
* morning;
* afternoon;
* evening;
* late night.

Time may affect:
* dialogue;
* animation;
* music;
* event availability;
* window scenes;
* sleeping probability.

## Weather System
Weather integration should be optional.
Weather affects atmosphere.
Possible modes:
1. Online weather using a manually selected city.
2. Device-based approximate location with clear permission.
3. Manual weather selection.
4. Offline seasonal mode.

## Music System
Music is optional and disabled or adjustable through settings.
Music files may include original compositions.
(The application must still work when audio playback fails.)
Suggested categories:
* main theme;
* quiet room;
* rain;
* night;
* winter;
* festival;
* sit together.

## Random Events
Events are selected using conditions and weighted probabilities.
Possible events:
* a bird visits;
* a mouse appears;
* a butterfly passes;
* the cat finds a box;
* the cat becomes a loaf;
* a feather is found;
* a tree changes for a festival;
* a package appears;
* the cat watches rain;
* nothing happens.

**“Nothing happens” is an intentional event outcome.**

## Little Things / Treasures
The collection is not controlled directly by the player.
The cat decides what is meaningful enough to bring home.
Possible objects:
* 🪶 feather;
* 🌼 flower;
* 🍄 mushroom;
* ⭐ small star-like object;
* unusual button;
* ribbon;
* stone;
* note.

Natural objects do not automatically become collectibles.
Different cats interpret objects differently.

## Temperament
Temperament is generated when the save file is created.
Possible hidden dimensions:
* curiosity;
* sociability;
* reflectiveness;
* home attachment;
* playfulness;
* collecting tendency.
These dimensions should not be presented as a character-selection menu.
The player discovers the cat's personality through its behaviour.

## Habits
Habits change gradually according to interactions and experiences.
Possible habits:
* enjoys sitting together;
* watches the window;
* talks at night;
* plays frequently;
* interacts with birds;
* explores outside;
* brings objects home.
(Habits should change slowly and have upper and lower limits.)

## Companion Agency
The cat evaluates events rather than following automatic collection rules.
The decision may depend on:
* innate temperament;
* learned habits;
* current mood;
* object qualities;
* weather;
* season;
* recent events;
* controlled randomness.
The resulting behaviour should be understandable in retrospect.
