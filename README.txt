Asteroids Game Project
This project was a huge learning milestone for me, focusing on building core game mechanics, mastering Object-Oriented Programming (OOP) in Python, and using Git for version control. It’s built using Pygame, and I’m really proud of how it came together after a lot of effort and debugging.

Project Highlights:
Language: Python
Library:
Pygame – a key tool in learning game development with Python.
Concepts I Practiced:
Object-Oriented Programming:

Learning how to design a game using OOP was one of the most challenging but rewarding parts of the project.
Created a flexible CircleShape class, and the Player class inherits from it to represent the player's spaceship.
Understanding inheritance and structuring game objects took some real work!
Modularity & File Structure:

I broke the project into separate modules to keep the code clean and manageable:
constants.py for game settings.
player.py for player control and movement.
asteroid.py and asteroidfield.py for generating asteroids.
floating_text.py for rendering in-game feedback like scores.
Game Mechanics:

Built a spaceship controlled by rotating and moving using the keyboard, with simple collision detection.
Asteroids spawn and move randomly, making the game more interesting and adding to the challenge.
Sprite Grouping & Updates:

Used Pygame’s sprite groups to manage rendering and updates, which helped me keep everything organized and smooth.
Game Loop & FPS Control:

Managing the frame rate with pygame.time.Clock() was crucial for consistent gameplay across different devices.
Version Control:

All the code is tracked with Git, which helped me stay organized and push my changes to GitHub.
Gameplay:
Control a rotating triangle spaceship with the arrow keys and "W" for forward movement.
Avoid or destroy asteroids, with a simple collision system using circular hitboxes.
Next Steps:
Adding an alien ship and wrapping the screen edges.
A scoreboard with a high score system and a pre-game menu to enter player names.