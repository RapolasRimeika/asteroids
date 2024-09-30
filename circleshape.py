import pygame
import random
from floating_text import FloatingText
from constants import GLOBAL_COLLISION_MODIFIER, ASTEROID_MIN_RADIUS, PLAYER_SHOT_SPEED
from text_lists import shrapnel_flames

class CircleShape(pygame.sprite.Sprite):
    """
    A base class for circular objects in the game. This class includes attributes 
    for linear and angular movement, friction, and health, and provides collision 
    handling and shrapnel generation on destruction.

    Attributes:
        position (pygame.Vector2): The position of the object in 2D space.
        velocity (pygame.Vector2): The linear velocity of the object.
        radius (float): The radius of the object.
        angular_velocity (float): The angular velocity of the object (rotational speed).
        rotation (float): The current rotation angle of the object.
        friction (float): The factor to slow down linear velocity over time.
        angular_friction (float): The factor to slow down angular velocity over time.
        health (float): The health of the object, based on its radius.
        destroyed (bool): A flag to determine if the object is destroyed.
    """
    def __init__(self, x, y, radius, friction=0.995, angular_friction=0.95):
        if hasattr(self, "containers"):                                       # Initialize sprite and add to groups if containers are set
            super().__init__(self.containers)
        else:
            super().__init__()                                                # Initialize sprite without containers
        self.destroyed = False                                                # Add a flag to track if the object has been destroyed
        self.position = pygame.Vector2(x, y)                                  # Set position as a 2D vector
        self.velocity = pygame.Vector2(0, 0)                                  # Linear velocity for movement, starts at (0,0)
        self.radius = radius                                                  # Set the radius of the object
        self.angular_velocity = 0                                             # Angular velocity (rotational inertia), initially 0
        self.rotation = 0                                                     # Current rotation angle, starts at 0
        self.friction = friction                                              # Linear friction factor to reduce velocity over time
        self.angular_friction = angular_friction                              # Rotational friction factor to reduce angular velocity
        self.speed = self.velocity.length()                                   # Speed is the magnitude (length) of the velocity vector
        self.health = self.radius * 2                                         # Health is twice the radius
        self.max_health = self.health                                         # Max health is the initial health value
        self.color = (255, 255, 255)                                          # Default color of the object is white

    def update(self, dt):
        self.velocity *= self.friction                          # Apply linear friction to slow down movement over time
        self.angular_velocity *= self.angular_friction          # Apply rotational friction to slow down rotation
        self.position += self.velocity * dt                     # Update position based on velocity (linear inertia)
        self.rotation += self.angular_velocity * dt             # Update rotation based on angular velocity
        self.rotation %= 360                                    # Keep rotation within 0-360 degrees (optional)

    def apply_force(self, force):
        self.velocity += force                                  # Apply force to velocity for linear movement

    def apply_torque(self, torque):
        self.angular_velocity += torque                         # Apply torque to angular velocity for rotation
        
    def collision(self, other, bounce=True):
        if hasattr(other, "is_explosion") and other.is_explosion == True:     # Ignore collisions with explosion objects
            return

        distance = self.position.distance_to(other.position)                  # Check for collision with another CircleShape
        if self.radius + other.radius > distance:                             # Check if the objects are overlapping
            if hasattr(other, "is_shot") and other.is_shot == True:           # Handle collisions with shots
                other.shot_explode(self)
                return
            impact_force = (other.radius * other.velocity.length() +          # Calculate damage based on combined
                            self.radius * self.velocity.length())             # object radius and velocity
            self.health -= impact_force * GLOBAL_COLLISION_MODIFIER           # Apply damage to `self`
            other.health -= impact_force * GLOBAL_COLLISION_MODIFIER          # Apply damage to `other`
            if self.health <= 0 and not self.destroyed:                       # Handle destruction for `self`
                self.shrapnel_obj(self.radius)
            if other.health <= 0 and not other.destroyed:                     # Handle destruction for `other`
                other.shrapnel_obj(other.radius)
            if bounce:                                                        # Bounce if enabled
                self.bounce(other)

    def bounce(self, other):
        normal = self.position - other.position                                   # Calculate the normal vector (line of impact)
        normal_distance = normal.length()                                         # Normalize the normal vector
        if normal_distance == 0:
            normal = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1)) # Avoid division by zero; choose an arbitrary normal vector
            normal.normalize_ip()                                                 # Normalize the chosen normal vector
        else:
            normal /= normal_distance                                             # Normalize the normal if distance is valid
        relative_velocity = self.velocity - other.velocity                        # Calculate relative velocity
        velocity_along_normal = relative_velocity.dot(normal)                     # Calculate velocity along the normal
        if velocity_along_normal > 0:                                             # Do not resolve if velocities are separating
            return
        restitution = 1                                                           # Elasticity of the collision (1 = elastic)
        mass_self = self.radius                                                   # Use radius as mass or radius squared
        mass_other = other.radius                                                 # Use radius as mass or radius squared
        impulse_scalar = -(1 + restitution) * velocity_along_normal               # Calculate impulse scalar
        impulse_scalar /= (1 / mass_self + 1 / mass_other)                        # Impulse scalar depends on masses
        impulse = impulse_scalar * normal                                         # Calculate impulse vector
        self.velocity += impulse / mass_self                                      # Update velocities based on collision response
        other.velocity -= impulse / mass_other                                    # Update the other object's velocity
        collision_torque_self = normal.cross(impulse) * mass_self                 # Apply rotational effects (optional)
        collision_torque_other = normal.cross(impulse) * mass_other               # Apply rotational effects to other object
        self.apply_torque(collision_torque_self)                                  # Apply torque to self
        other.apply_torque(-collision_torque_other)                               # Apply opposite torque to the other object


    def draw(self, screen):                                             # Subclasses should override this method to draw themselves
        pass

    def shrapnel_obj(self, mass, RGB=(150, 150, 150),):
        if self.destroyed:                                              # Check if the object is already destroyed
            return                                                      # If destroyed, exit early to prevent multiple splits
        self.kill()                                                     # Kill the object
        self.destroyed = True                                           # Mark the object as destroyed to prevent further shrapnel or split calls
        if hasattr(self, "is_explosion") and self.is_explosion == True: # Skip if the object is an explosion
            return
        if hasattr(self, 'death'):                                      # Check if the object has a .death() method (e.g., Player, Alien)
            self.death()                                                # Call the death() method if it exists
            self.create_shrapnel(30)                                    # Create shrapnel after death
            return
        if hasattr(self, 'split'):                                      # Check if the object has a .split() method (e.g., Asteroid)
            if self.radius > ASTEROID_MIN_RADIUS:                       # Only split if the radius is larger than the minimum
                self.split()                                            # Call split() for the asteroid
                return                                                  # Skip shrapnel generation if split is successful
        self.create_shrapnel(mass)                                      # Create shrapnel using the remaining mass

    def create_shrapnel(self, mass):
        while mass > 3:
            random_angle = random.uniform(0, 360)                                               # Generate a random angle for the shrapnel direction
            velocity_a = self.velocity.rotate(random_angle) * random.uniform(0.1, 2)            # Generate random velocity
            new_radius = random.randrange(1, 3, 1)                                              # Create a random radius for the shrapnel piece
            shrapnel_piece = Shrapnel(self.position.x, self.position.y, new_radius, self.color) # Create the shrapnel piece
            if velocity_a.length() == 0:                                                        # Check if velocity is effectively zero
                velocity_a = pygame.Vector2(1, 0).rotate(random_angle) * PLAYER_SHOT_SPEED      # Set minimum velocity if stationary
            shrapnel_piece.velocity = velocity_a                                                # Apply velocity to the shrapnel piece
            if shrapnel_piece.velocity.length() < PLAYER_SHOT_SPEED / 10:                       # Ensure velocity is at least PLAYER_SHOT_SPEED/10
                shrapnel_piece.velocity.scale_to_length(PLAYER_SHOT_SPEED / 10)
            mass -= new_radius                                                                  # Decrease the remaining mass
            print(f"New shrapnel from {self}, shrapnel mass {new_radius}, remaining mass is {mass}")

class Shrapnel(CircleShape):
    def __init__(self, x, y, radius, RGB=(235, 5, 2)):
        super().__init__(x, y, radius)
        self.lifetime = random.randrange(100, 700, 100)             # Set random lifetime for the shrapnel in milliseconds
        self.spawn_time = pygame.time.get_ticks()                   # Get the spawn time in ticks
        self.rgb = RGB                                              # Set the color of the shrapnel (default or passed in)
        self.angular_velocity = 0                                   # Disable angular velocity (no rotation)

    def update(self, dt):
        self.position += self.velocity * dt                         # Update position based on velocity and time delta
        self.velocity *= self.friction                              # Apply friction to slow down movement
        current_time = pygame.time.get_ticks()                      # Get current time in ticks
        if current_time - self.spawn_time > self.lifetime:          # Check if lifetime has expired
            self.kill()                                             # Remove shrapnel if its lifetime is over

    def draw(self, screen):                                         # Draw the shrapnel on the screen as a white circle as the shrapnel outline
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius)
        flame = random.choice(shrapnel_flames)                      # Choose a random floating flame character
        FloatingText(self.position.x, self.position.y, (f"{flame}"), self.rgb, 40) # Display floating flame text
    
    def apply_torque(self, torque):                                 # Torque is disabled for shrapnel (no rotation)
        pass