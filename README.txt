# Asteroids Game Project

This project is a learning exercise focused on building basic game mechanics, practicing Object-Oriented Programming (OOP) with Python, and working with Git and GitHub for version control. The game is developed using the **Pygame** library, and it incorporates multiple files that reference each other, promoting modular and maintainable code design.

## Project Features:
- **Languages**: Python
- **Packages**: 
  - [Pygame](https://www.pygame.org/news) – a popular library for building games and multimedia applications in Python.

## Key Concepts Practiced:
1. **Object-Oriented Programming**: 
   - The game utilizes OOP principles like classes and inheritance.
   - A `CircleShape` class is created using `pygame.sprite.Sprite` to represent basic circular shapes in the game. 
   - A `Player` subclass is derived from the `CircleShape` class, inheriting its properties, and represents the player-controlled spaceship.

2. **Game Mechanics**:
   - The project simulates a spaceship controlled by the player, represented by a rotating triangle.
   - The triangle (ship) rotates and moves based on player input.
   - The circle shape is used purely for hit detection (hitpoints) to manage collisions.

3. **File Structure and Modularity**:
   - The project is split into multiple files for different responsibilities:
     - **`constants.py`**: Stores game-wide constants like screen dimensions and object sizes.
     - **`circleshape.py`**: Defines the base `CircleShape` class for game objects.
     - **`player.py`**: Implements the `Player` class that extends the `CircleShape` to create the player-controlled object (a rotating triangle).
     - **`main.py`**: Handles the main game loop, player input, and rendering.

4. **Game Loop & FPS Management**:
   - The frame rate of the game is controlled using `pygame.time.Clock()`, which ensures consistent game speed across different hardware.

5. **Git and GitHub**:
   - The project is under version control using Git and hosted on GitHub, allowing for efficient code management and collaboration.

## Gameplay Overview:
- The player's ship is represented by a rotating triangle.
- The ship's rotation and movement are controlled using the keyboard.
- The base shape of the player (a circle) is used for collision detection but is visually represented as a triangle.
