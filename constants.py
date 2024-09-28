# Screen dimensions
SCREEN_WIDTH = 2560
SCREEN_HEIGHT = 1440

# Asteroids
ASTEROID_MIN_RADIUS = 20
ASTEROID_KINDS = 3
ASTEROID_SPAWN_RATE = 0.9  # seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

# Player settings
PLAYER_RADIUS = 20
PLAYER_TURN_SPEED = 300
PLAYER_SPEED = 200

# Shots
SHOT_RADIUS = 5
SHOT_LIFETIME = 2000  # milliseconds
PLAYER_SHOT_SPEED = 700
PLAYER_SHOOT_COOLDOWN = 0.3  # seconds
PLAYER_SHOT_DMG = 40

# Alien settings
ALIEN_SPEED = 50
ALIEN_SHOT_SPEED = 300
ALIEN_SHOOT_COOLDOWN = 1.5  # seconds
ALIEN_RADIUS = 25
ALIEN_HEALTH = ALIEN_RADIUS * 3
ALIEN_SPAWN_RATE = 3.0
ALIEN_SHOOTING_RANGE = 600
ALIEN_TURN_SPEED = PLAYER_TURN_SPEED * 1.5
ALIEN_MOVE_SPEED = PLAYER_SPEED * 1.5
ALIEN_COLOR = (50, 190, 50)
ALIEN_MAX_SPEED = 300               # Maximum speed for the alien
ALIEN_MAX_ANGULAR_VELOCITY = 300    # Maximum angular velocity in degrees per second
ALIEN_STABILISER_STRENGTH = 0.5     # Strength of stabilisation


# Global settings
GLOBAL_COLLISION_MODIFIER = 0.002
LOOT_DROP_CHANCE = 0.7

# Explosion settings
EXPLOSION_NEAR_STRENGTH = 400
EXPLOSION_MID_STRENGTH = 200
EXPLOSION_FAR_STRENGTH = 100
EXPLOSION_COLOR = (189, 12, 16)
EXPLOSION_INITIAL_RADIUS = 1
EXPLOSION_FAR_RADIUS = EXPLOSION_INITIAL_RADIUS * 200
EXPLOSION_NEAR_RADIUS = EXPLOSION_FAR_RADIUS / 3
EXPLOSION_MID_RADIUS = EXPLOSION_FAR_RADIUS / 1.5

# Black Hole (BLK) settings
BLACK_HOLE_X = 100
BLACK_HOLE_Y = 100
BLACK_HOLE_RADIUS = 75
BLACK_HOLE_FRICTION = 1
BLACK_HOLE_ANGULAR_FRICTION = 1

BLACK_HOLE_FAR_RADIUS = BLACK_HOLE_RADIUS * 10
BLACK_HOLE_NEAR = BLACK_HOLE_FAR_RADIUS / 4
BLACK_HOLE_MID_RADIUS = BLACK_HOLE_FAR_RADIUS / 2

BLACK_HOLE_COLOR = (150, 120, 160)
BLACK_HOLE_HEALTH = 1_000_000

BLACK_HOLE_COLLI_BUFFER = 15

BLACK_HOLE_NEAR_PULL = -100
BLACK_HOLE_MID_PULL = -10
BLACK_HOLE_FAR_PULL = -3


TEXT_COLOR = (250, 200, 100)
LINE_SPACING = 30
FONT_SIZE = 34           # Font size for FloatingText
PLAYER_FIRE_COLOR = (255, 0, 0)

# Loot constants
LOOT_HEALTH = 1000000000  # Infinite health to keep loot until picked up
LOOT_COLLECTION_BUFFER = 5  # Buffer to make loot easier to collect

# Loot effect multipliers and values
LOOT_HEAL_AMOUNT = 200
LOOT_SCORE_POINTS = 50
LOOT_FIRE_COOLDOWN_MULTIPLIER = 0.7
LOOT_DMG_MULTIPLIER = 2
LOOT_SPEED_MULTIPLIER = 1.2
LOOT_ROTATION_MULTIPLIER = 1.2
LOOT_ALREADY_HAVE_STABILISERS_POINTS = 50
LOOT_ALREADY_HAVE_STABILISERS_MSG = "Already have Stabilisers, let's sell it"

# Loot type colors
LOOT_COLOR_HEALTH = (0, 255, 0)
LOOT_COLOR_SPEED = (0, 0, 255)
LOOT_COLOR_SCORE = (255, 255, 0)
LOOT_COLOR_FIRE = (255, 0, 255)
LOOT_COLOR_ROTATION = (0, 50, 200)
LOOT_COLOR_STABILISERS = (99, 50, 15)
LOOT_COLOR_DMG = (255, 0, 75)

# Loot descriptions
LOOT_DESCRIPTION_HEAL = (f'+{LOOT_HEAL_AMOUNT} Health')
LOOT_DESCRIPTION_SPEED = 'Engine upgrade!'
LOOT_DESCRIPTION_SCORE = (f'{LOOT_SCORE_POINTS}+ Score!')
LOOT_DESCRIPTION_FIRE = 'Fire rate increase!'
LOOT_DESCRIPTION_ROTATION = 'Thruster upgrade!'
LOOT_DESCRIPTION_STABILISERS = 'STABILISERS!!!!'
LOOT_DESCRIPTION_DMG = 'Fire damage increase!'

LOOT_EFFECT_HEAL = 'heal'
LOOT_EFFECT_SPEED = 'speed'
LOOT_EFFECT_SCORE = 'score'
LOOT_EFFECT_FIRE = 'fire'
LOOT_EFFECT_ROTATION = 'rotation'
LOOT_EFFECT_STABILISERS = 'stabilisers'
LOOT_EFFECT_DMG = 'dmg'

LOOT_MSG_DURATION = 1000