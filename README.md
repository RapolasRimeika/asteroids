# Asteroids Game Project

Welcome to my Asteroids game project! 🎮 This has been a fun and challenging learning exercise where I implemented complex game mechanics, practiced Object-Oriented Programming (OOP) in Python, and refined my skills in Git and GitHub for version control. The game is built with the Pygame library and designed to be modular, maintainable, and scalable.

## What's Inside

- **Language:** Python 🐍
- **Libraries:** Pygame for game development, Pillow for image processing (Gaussian blur).

## What I Learned

### Object-Oriented Programming:
- Built a hierarchy of classes like `CircleShape`, `Player`, `Asteroid`, `Shot`, `FloatingText`, `Loot`, and `AlienShip`.
- Applied inheritance, encapsulation, and composition to build reusable, flexible game components.
- Implemented sprite groups for efficient updates and rendering of game objects.

### Game Mechanics:
- **Player Controls:** 
    Rotate, move, and shoot with smooth physics.
- **Asteroids:** 
    Randomly generated textures and splitting mechanics when destroyed. Asteroids also generate shrapnel upon destruction.
- **Alien Ships:** 
    Alien ships track the player, avoid asteroids, shoot when in range, and drop loot upon destruction.
- **Loot System:** 
    Different power-ups like health regeneration, speed boosts, stabilizers, and more spawn upon defeating enemies.
- **Inertia and Stabilizers:** 
    Full physics system with linear and angular inertia, friction, and stabilizers that stop small movements when not pressing movement keys.
- **Black Holes (BLK Class):** 
    A black hole that spawns randomly, pulls objects in based on proximity, and removes objects when too close.
- **Background Generation:** 
    Multi-layered star and planet backgrounds with randomly generated textures, Gaussian blur applied to the planet layer for depth.
- **Explosion Physics:** 
    Objects interact with explosions based on proximity, and forces are applied accordingly.

### Code Modularity:
- The code is split into multiple files for readability, maintainability, and scalability:
  - `constants.py`        : Stores all global constants like screen dimensions and object sizes.
  - `circleshape.py`      : A base class for circular game objects with full inertia and friction.
  - `player.py`           : Manages player controls, movement, shooting, and collision detection.
  - `asteroid.py`         : Handles asteroid movement, splitting, and texture generation.
  - `asteroidfield.py`    : Manages asteroid spawning, including black holes.
  - `aliens.py`           : Manages alien ship behavior and interactions with the player.
  - `loot.py`             : Implements the loot system with power-ups for the player.
  - `explosion.py`        : Handles explosion interactions with objects.
  - `floating_text.py`    : Displays text effects during gameplay.
  - `background_layers.py`: Generates dynamic star and planet backgrounds.
  - `main.py`             : The main game loop handling events, updates, and rendering.

### Version Control:
- Managed the entire project using Git and GitHub, effectively tracking changes and allowing collaboration.

## How to Play

**Controls:**
- Rotate: Left/Right arrow keys or A/D.
- Move: Up/Down arrow keys or W/S.
- Shoot: Spacebar.
- Stabilizers: Automatically engage when not pressing movement keys to stop small movements.
- Restart: Press Enter after game over.
- Quit Game: Press Escape.

**Objective:**
Navigate your spaceship, avoid asteroids, black holes and enemy fire.
Destroy aliens and asteroids by shooting at them. 
Collect loot from defeated enemies to gain power-ups and increase your score. 
Survive as long as possible!

## Future Plans

- **More Alien Ships:** New enemy types with unique behaviors.
- **Persistent High Score System:** A way to save and display the high score.
- **Player Profiles:** Adding a menu to enter player names and track performance.

## Getting Started

1. Clone the repository:
    git clone https://github.com/RapolasRimeika/asteroids-game.git
2. Install the dependencies:
    pip install -r requirements.txt
3. Run the game:
    python3 main.py