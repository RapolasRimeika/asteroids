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

**Game State Management:**  
    The game constantly tracks the player's state, including death, and manages transitions between different modes (e.g., playing, game over, name entry). During gameplay, it monitors player score and playtime, updating the game state based on player actions and events, ensuring smooth transitions.

- **Player Highscores:**  
    After the game finishes, the player is prompted to enter their name, and the scores are saved. The high score system retains up to 10 entries, showing the leaderboard at the end of the game, giving players the chance to compete for the top spots.

- **Alien Ships:**  
    Alien ships track the player, navigate around asteroids, and strategically shoot when in range. Upon destruction, they drop various loot items, adding dynamic gameplay and resource rewards for the player.

- **Loot System:**  
    Loot spawns upon defeating Alien ships, offering power-ups like health, speed boosts, stabilizers, and other upgrades. Each loot item modifies the ship's attributes, making gameplay progressively more challenging and rewarding.

- **Global Collision:**  
    A robust physics engine governs collisions, where objects not only collide but also take damage based on their relative velocity and mass. The impact forces cause them to bounce off each other, leading to realistic interactions between all in-game objects.

- **Shrapnel:**  
    Upon destruction, objects break apart into multiple shrapnel pieces, the amount of which is determined by their radius. The shrapnel scatters in various directions, colliding with nearby objects and dealing additional damage, enhancing the unpredictability of space combat.

- **Inertia:**  
    The game employs a full physics system with both linear and angular inertia. Spaceships experience friction and momentum, adding a layer of control and realism to movement. While all objects have inertia, non-controllable objects have angular inertia disabled for smoother performance.

- **Stabilizers:**  
    Spaceships (both Player and Alien) have angular momentum and built-in stabilizers to counteract small, unintended movements caused by inertia. This system helps control both linear and angular momentum when movement keys aren't pressed. The stabilizers are upgradable through loot, providing better handling.

- **Black Holes (BlackHole Class):**  
    Black holes spawn randomly in space, pulling in nearby objects based on proximity. As objects get too close, they are pulled in and eventually disappear, introducing an ever-present environmental hazard with gravitational physics.

- **Background Generation:**  
    A complex, multi-layered background system generates star and planet layers with procedurally generated textures. Gaussian blur is applied to the planet layer, creating a sense of depth and immersion in the game’s expansive space environment.

- **Explosion Physics:**  
    Explosions affect nearby objects based on proximity, applying realistic force dynamics. The closer an object is to the explosion, the greater the force exerted, causing ripple effects across the environment and impacting gameplay significantly.

### Code Modularity:

- The code is split into multiple files for readability, maintainability, and scalability:

  - **`constants.py`**        : Stores global constants like screen dimensions and object sizes.
  - **`circleshape.py`**      : A base class for circular game objects with full inertia and friction.
  - **`player.py`**           : Manages player controls, movement, shooting, and collision detection.
  - **`asteroid.py`**         : Handles asteroid movement, splitting, and texture generation.
  - **`asteroidfield.py`**    : Manages asteroid spawning and interactions, including black holes.
  - **`aliens.py`**           : Manages alien ship behavior and interactions with the player.
  - **`loot.py`**             : Implements the loot system with power-ups for the player.
  - **`explosion.py`**        : Handles explosion physics and their interactions with objects.
  - **`floating_text.py`**    : Displays floating text effects during gameplay.
  - **`background.py`**       : Generates dynamic multi-layered star and planet backgrounds.
  - **`main.py`**             : The main game loop handling events, updates, and rendering.
  - **`AlienField.py`**       : Special field or behavior management for alien ships.
  - **`black_hole.py`**       : Manages the behavior and physics of black holes within the game.
  - **`high_scores.json`**    : Stores the top player scores after each session.
  - **`state.py`**            : Manages the game states like playing, game over, and name entry.
  - **`shot.py`**             : Implements the mechanics for player and alien shots.
  - **`text_lists.py`**       : Stores pre-defined text messages or lists for gameplay.


## How to Play

**Controls:**
- Rotate: Left/Right arrow keys.
- Move: Up/Down arrow keys.
- Shoot: Spacebar.
- Stabilizers: Automatically engage when not pressing movement keys to stop small movements.
- Restart: Press Return after game over. Enter your name, press Return to save score and start a new game.
- Quit Game: Press Escape at any point to quit the game.

**Objective:**
Navigate your spaceship, avoid asteroids, black holes and enemy fire.
Destroy aliens and asteroids by shooting at them to score points. 
Collect loot from defeated enemies to gain power-ups and increase your score. 
Survive as long as possible!

## Getting Started

This project requires **Python 3.9.6** or higher.

### 1. Install Python (if not already installed)

For macOS users, you can install Python via Homebrew:

brew install python

For other platforms, refer to the [official Python website](https://www.python.org/downloads/) version.

### 2. Clone the repository and move into the directory

git clone https://github.com/RapolasRimeika/asteroids.git

cd asteroids

### 3. Install the dependencies

pip install -r requirements.txt

### 3.1 (Optional) Create and activate a virtual environment

It is recommended to use a virtual environment to keep dependencies isolated.

#### Create a virtual environment and activate the virtual environment:
python3 -m venv venv
### On Mac
source venv/bin/activate

### On Windows:
venv\Scripts\activate

#### Deactivate the virtual environment once finished with the game:
deactivate

### 4. Configure screen size

To adjust the screen size to fit your monitor or personal preference, edit the `constants.py` file:

### Inside constants.py, modify the SCREEN_WIDTH and SCREEN_HEIGHT
SCREEN_WIDTH = 1920  # Example
SCREEN_HEIGHT = 1080  # Example

### 5. Run the game

After configuring the screen size, you can start the game by running the following in the directory:

python3 main.py