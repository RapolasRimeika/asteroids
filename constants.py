"""
This module defines various constants used throughout the game, including player settings,
alien settings, explosion effects, loot attributes, and global game parameters.

These constants help in configuring object behavior like movement speed, collision detection,
color properties, and loot effects, ensuring consistency and ease of tweaking gameplay mechanics.
"""

import pygame                                                   # Pygame library for keys

# Screen dimensions
SCREEN_WIDTH = 2560                                             # Screen width in pixels
SCREEN_HEIGHT = 1440                                            # Screen height in pixels

# Asteroids
ASTEROID_MIN_RADIUS = 20                                        # Minimum asteroid size
ASTEROID_KINDS = 3                                              # Number of asteroid types
ASTEROID_SPAWN_RATE = 0.9                                       # Time interval (seconds) between asteroid spawns
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS      # Max size for asteroids

# Player settings
PLAYER_RADIUS = 20                                              # Radius of the player object
PLAYER_TURN_SPEED = 300                                         # Player turning speed in degrees per second
PLAYER_SPEED = 200                                              # Player movement speed in pixels per second
STABILISER_STR = 0.5                                            # Strength of the player's stabiliser effect

# Key mappings for movement and rotation
KEY_UP =            [pygame.K_w, pygame.K_UP, pygame.K_KP8]     # Keys for moving up/forward
KEY_DOWN =          [pygame.K_s, pygame.K_DOWN, pygame.K_KP5]   # Keys for moving down/backward
KEY_STRAFE_LEFT =   [pygame.K_a, pygame.K_KP4]                  # Keys for strafing left
KEY_STRAFE_RIGHT =  [pygame.K_d, pygame.K_KP6]                  # Keys for strafing right
KEY_TURN_LEFT =     [pygame.K_q, pygame.K_LEFT, pygame.K_KP7]   # Keys for turning left
KEY_TURN_RIGHT =    [pygame.K_e, pygame.K_RIGHT, pygame.K_KP9]  # Keys for turning right
KEY_SHOOT =         pygame.K_SPACE                              # Key for shooting

# Shots
SHOT_RADIUS = 5                                                 # Radius of a player's shot
SHOT_LIFETIME = 2000                                            # Lifetime of a shot in milliseconds
PLAYER_SHOT_SPEED = 700                                         # Speed of a player's shot in pixels per second
PLAYER_SHOOT_COOLDOWN = 0.3                                     # Cooldown time between shots in seconds
PLAYER_SHOT_DMG = 40                                            # Damage dealt by player's shot
SHOT_EXPLOSION_BUFFER = SHOT_RADIUS                             # Buffer for shot explosion before direct collision

# Alien settings
ALIEN_SPEED = 50                                                # Speed of alien ship
ALIEN_SHOT_SPEED = 300                                          # Speed of alien's shot
ALIEN_SHOOT_COOLDOWN = 1.5                                      # Time between alien shots
ALIEN_RADIUS = 25                                               # Radius of the alien ship
ALIEN_HEALTH = ALIEN_RADIUS * 3                                 # Health of the alien
ALIEN_SPAWN_RATE = 3.0                                          # Time interval for spawning alien ships
ALIEN_SHOOTING_RANGE = 600                                      # Maximum range at which aliens can shoot
ALIEN_TURN_SPEED = PLAYER_TURN_SPEED * 1.5                      # Alien turning speed
ALIEN_MOVE_SPEED = PLAYER_SPEED * 1.5                           # Alien movement speed
ALIEN_COLOR = (50, 190, 50)                                     # Alien ship color (green)
ALIEN_MAX_SPEED = 300                                           # Maximum speed for the alien ship
ALIEN_MAX_ANGULAR_VELOCITY = 300                                # Maximum angular velocity for the alien ship
ALIEN_STABILISER_STRENGTH = 0.5                                 # Strength of the alien ship's stabiliser

# Global settings
GLOBAL_COLLISION_MODIFIER = 0.002                   # Modifier for collision damage calculations
LOOT_DROP_CHANCE = 0.7                              # Probability of loot dropping from destroyed enemies
STABILISER_VELOSITY_THRESHOLD = 1                   # Threshold for stabiliser to stop small movements
MIN_SHRAPNEL_SPEED = PLAYER_SHOT_SPEED / 10         # Minimum speed for shrapnel pieces, based on player shot speed

# Explosion settings
EXPLOSION_NEAR_STRENGTH = 200                       # Explosion strength at close range
EXPLOSION_MID_STRENGTH = 100                        # Explosion strength at mid-range
EXPLOSION_FAR_STRENGTH = 50                         # Explosion strength at far range
EXPLOSION_COLOR = (189, 12, 16)                     # Color of explosion (red)
EXPLOSION_INITIAL_RADIUS = 1                        # Initial radius for explosions
EXPLOSION_FAR_RADIUS = EXPLOSION_INITIAL_RADIUS * 200 # Far radius for explosion effects
EXPLOSION_NEAR_RADIUS = EXPLOSION_FAR_RADIUS / 3    # Near radius for close-range explosion effects
EXPLOSION_MID_RADIUS = EXPLOSION_FAR_RADIUS / 1.5   # Mid radius for mid-range explosion effects

# Black Hole (BLK) settings
BLACK_HOLE_X = 100                                  # X-coordinate of the black hole
BLACK_HOLE_Y = 100                                  # Y-coordinate of the black hole
BLACK_HOLE_RADIUS = 75                              # Radius of the black hole
BLACK_HOLE_FRICTION = 1                             # Friction of the black hole
BLACK_HOLE_ANGULAR_FRICTION = 1                     # Angular friction of the black hole
BLACK_HOLE_FAR_RADIUS = BLACK_HOLE_RADIUS * 10      # Far radius for black hole's pull effect
BLACK_HOLE_NEAR = BLACK_HOLE_FAR_RADIUS / 4         # Near range pull radius
BLACK_HOLE_MID_RADIUS = BLACK_HOLE_FAR_RADIUS / 2   # Mid range pull radius
BLACK_HOLE_COLOR = (150, 120, 160)                  # Black hole color (purple-ish)
BLACK_HOLE_HEALTH = 1_000_000                       # Black hole's health
BLACK_HOLE_COLLI_BUFFER = 15                        # Collision buffer for black hole
BLACK_HOLE_NEAR_PULL = -100                         # Pull strength near black hole
BLACK_HOLE_MID_PULL = -10                           # Pull strength mid-range black hole
BLACK_HOLE_FAR_PULL = -3                            # Pull strength far-range black hole

# Text settings
TEXT_COLOR = (250, 200, 100)                        # Color for on-screen text
LINE_SPACING = 30                                   # Spacing between lines of text
FONT_SIZE = 34                                      # Font size for in-game text
PLAYER_FIRE_COLOR = (255, 0, 0)                     # Color for player fire effect
PLAYER_COLOR = (234, 0, 0)                          # Player's color

# Loot constants
LOOT_HEALTH = 1000000000                            # Infinite health to keep loot until picked up
LOOT_COLLECTION_BUFFER = 10                         # Buffer to make loot easier to collect
LOOT_MSG_DURATION = 1000                            # Duration in milliseconds for displaying loot effect messages

# Loot effect multipliers and values
LOOT_HEAL_AMOUNT = 200                              # Amount of health restored by health loot
LOOT_SCORE_POINTS = 50                              # Points awarded for collecting score loot
LOOT_FIRE_COOLDOWN_MULTIPLIER = 0.7                 # Multiplier to decrease shot cooldown
LOOT_DMG_MULTIPLIER = 2                             # Multiplier to increase shot damage
LOOT_SPEED_MULTIPLIER = 1.2                         # Multiplier to increase player speed
LOOT_ROTATION_MULTIPLIER = 1.2                      # Multiplier to increase turn speed

# Loot colors
LOOT_COLOR_HEALTH = (0, 255, 0)                     # Color for health loot (green)
LOOT_COLOR_SPEED = (0, 0, 255)                      # Color for speed loot (blue)
LOOT_COLOR_SCORE = (255, 255, 0)                    # Color for score loot (yellow)
LOOT_COLOR_FIRE = (255, 0, 255)                     # Color for fire rate loot (magenta)
LOOT_COLOR_ROTATION = (0, 50, 200)                  # Color for rotation speed loot (blue)
LOOT_COLOR_STABILISERS = (99, 50, 15)               # Color for stabiliser loot (brown)
LOOT_COLOR_DMG = (255, 0, 75)                       # Color for damage loot (red)

# Loot descriptions
LOOT_DESCRIPTION_HEAL = (f'+{LOOT_HEAL_AMOUNT} Health')  # Description for health loot
LOOT_DESCRIPTION_SPEED = 'Engine upgrade!'               # Description for speed loot
LOOT_DESCRIPTION_SCORE = (f'{LOOT_SCORE_POINTS}+ Score!') # Description for score loot
LOOT_DESCRIPTION_FIRE = 'Fire rate increase!'            # Description for fire rate loot
LOOT_DESCRIPTION_ROTATION = 'Thruster upgrade!'          # Description for rotation speed loot
LOOT_DESCRIPTION_STABILISERS = 'STABILISERS!!!!'         # Description for stabiliser loot
LOOT_DESCRIPTION_DMG = 'Fire damage increase!'           # Description for damage loot

# Loot effects
LOOT_EFFECT_HEAL = 'heal'                                # Effect for health loot
LOOT_EFFECT_SPEED = 'speed'                              # Effect for speed loot
LOOT_EFFECT_SCORE = 'score'                              # Effect for score loot
LOOT_EFFECT_FIRE = 'fire'                                # Effect for fire rate loot
LOOT_EFFECT_ROTATION = 'rotation'                        # Effect for rotation speed
LOOT_EFFECT_STABILISERS = 'stabilisers'                  # Effect for stabilisers loot (improves stabiliser strength)
LOOT_EFFECT_DMG = 'dmg'                                  # Effect for damage loot (increases shot damage)