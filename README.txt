Asteroids Game Project
Welcome to my Asteroids game project! 🎮 This was a fun learning exercise where I built basic game mechanics, practiced Object-Oriented Programming (OOP) with Python, and honed my skills with Git and GitHub for version control. The game is developed using the Pygame library and is designed to be modular and maintainable.

What's Inside
Language: Python 🐍
Library: Pygame for game development.
What I Learned
Object-Oriented Programming:

Created a hierarchy of classes like CircleShape, Player, Asteroid, Shot, and FloatingText.
Used inheritance and encapsulation to build flexible game components.

Game Mechanics:

Implemented player controls for rotation and movement.
Developed asteroid spawning, movement, and splitting mechanics.
Added collision detection between the player, asteroids, and shots.
Implemented screen wrapping so objects reappear on the opposite side.

Code Modularity:

Organized the code into multiple files for better readability and maintenance.
Utilized sprite groups in Pygame for efficient updates and rendering.
Version Control:

Managed the project using Git and GitHub, which was great for tracking changes and collaborating.
How to Play

Controls:

Rotate: Left/Right arrow keys or A/D.
Move: Up/Down arrow keys or W/S.
Shoot: Spacebar.
Restart: Press Enter after game over.

Objective:

Navigate your spaceship, avoid collisions with asteroids, and destroy them by shooting. Asteroids will split into smaller ones when hit until they reach the smallest size.

Future Plans. I'm excited to add more features soon:

Alien Ships: Introducing new challenges.
Scoring System: Displaying current and high scores.
Player Profiles: Adding a menu to enter player names before starting.

Getting Started:

pip install pygame
git clone https://github.com/RapolasRimeika/asteroids-game.git
cd asteroids-game
python3 main.py


File Structure

constants.py: Defines game-wide constants like screen dimensions and object sizes.
circleshape.py: Base class CircleShape for circular game objects.
player.py: Implements the Player class for the player-controlled spaceship.
asteroid.py: Defines the Asteroid class for asteroid objects.
asteroidfield.py: Manages the spawning and updating of asteroids.
shot.py: Implements the Shot class for player projectiles.
floating_text.py: Handles floating text messages displayed during gameplay.
state.py: Manages the game state, including player lives and respawning.
main.py: The main game loop, handling events, updates, and rendering.

Contact

Feel free to reach out if you have any questions or suggestions. I'm always open to feedback!

