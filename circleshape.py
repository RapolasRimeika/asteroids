import pygame
import random
from floating_text import FloatingText
from constants import GLOBAL_COLLISION_MODIFIER, ASTEROID_MIN_RADIUS, PLAYER_SHOT_SPEED
from text_lists import shrapnel_flames


# Base class for circular game objects with full inertia and friction
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, friction=0.995, angular_friction=0.95):
        # Initialize sprite and add to groups if containers are set
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.destroyed = False  # Add a flag to track if the object has been destroyed
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)  # Linear velocity for movement
        self.radius = radius
        self.angular_velocity = 0  # Angular velocity (rotational inertia)
        self.rotation = 0  # Current rotation angle
        self.friction = friction  # Linear friction factor
        self.angular_friction = angular_friction  # Rotational friction factor
        self.speed = self.velocity.length() # Speed is the lenght of the vector "velocity"
        self.health = self.radius * 2
        self.max_health = self.health
        self.color = (255, 255, 255)

    def apply_force(self, force):
        # Apply force to the velocity (affects linear movement)
        self.velocity += force
    
    def apply_torque(self, torque):
        # Apply torque to angular velocity (affects rotation)
        self.angular_velocity += torque

    def update(self, dt):
        # Apply linear friction to slow down movement over time
        self.velocity *= self.friction

        # Apply rotational friction to slow down rotation over time
        self.angular_velocity *= self.angular_friction

        # Update position based on velocity (linear inertia)
        self.position += self.velocity * dt

        # Update rotation based on angular velocity (rotational inertia)
        self.rotation += self.angular_velocity * dt

        # Optional: Keep rotation within 0-360 degrees
        self.rotation %= 360

    def collision(self, other, bounce=True):
        if hasattr(other, "is_explosion") and other.is_explosion == True:
            return

        # Check for collision with another CircleShape
        distance = self.position.distance_to(other.position)
        if self.radius + other.radius > distance:
            if hasattr(other, "is_shot") and other.is_shot == True:
                other.shot_explode(self)
                return
            
            # Calculate damage based combined object radius and speed
            impact_force = (other.radius * other.velocity.length() + self.radius * self.velocity.length()) 
            self.health -= impact_force * GLOBAL_COLLISION_MODIFIER
            other.health -= impact_force * GLOBAL_COLLISION_MODIFIER
            
            # Handle destruction and shrapnel generation for `self`
            if self.health <= 0 and not self.destroyed:
                self.shrapnel_obj(self.radius)

            # Handle destruction and shrapnel generation for `other`
            if other.health <= 0 and not other.destroyed:
                other.shrapnel_obj(other.radius)  # Use `other.radius` instead of `self.radius` here


            if bounce:                      # Bounce if enabled
                self.bounce(other)


    def bounce(self, other):       
        # Calculate the normal vector (line of impact)
        normal = self.position - other.position
        # Normalize the normal vector
        normal_distance = normal.length()
        if normal_distance == 0:
            # Avoid division by zero; choose an arbitrary normal vector
            normal = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            normal.normalize_ip()
        else:
            normal /= normal_distance  # Normalize

        # Calculate relative velocity
        relative_velocity = self.velocity - other.velocity

        # Calculate velocity along the normal
        velocity_along_normal = relative_velocity.dot(normal)

        # Do not resolve if velocities are separating
        if velocity_along_normal > 0:
            return

        # Calculate restitution (elasticity of the collision)
        restitution = 1  # 1 for perfectly elastic collision, 0 for perfectly inelastic

        # Calculate masses (using radius as mass or radius squared)
        mass_self = self.radius  # Or self.radius ** 2
        mass_other = other.radius  # Or other.radius ** 2

        # Calculate impulse scalar
        impulse_scalar = -(1 + restitution) * velocity_along_normal
        impulse_scalar /= (1 / mass_self + 1 / mass_other)

        # Calculate impulse vector
        impulse = impulse_scalar * normal

        # Update velocities based on collision response
        self.velocity += impulse / mass_self
        other.velocity -= impulse / mass_other

        # Apply rotational effects (optional, if objects spin after collision)
        collision_torque_self = normal.cross(impulse) * mass_self
        collision_torque_other = normal.cross(impulse) * mass_other
        self.apply_torque(collision_torque_self)
        other.apply_torque(-collision_torque_other)

    def draw(self, screen):
        # Subclasses should override this method to draw themselves
        pass

    def shrapnel_obj(self, mass, RGB=(150, 150, 150),):
        if self.destroyed:      # Check if the object is already destroyed
            return              # If destroyed, exit early to prevent multiple splits

        self.kill()             # Kill the object
        self.destroyed = True   # Mark the object as destroyed to prevent further shrapnel or split calls
        
        if hasattr(self, "is_explosion") and self.is_explosion == True:
            return
        
        if hasattr(self, 'death'): # Player and Alien classes have .death() method
            self.death()  # Call death() if it exists
            self.create_shrapnel(30)
            return
        
        if hasattr(self, 'split'):                  # if asteroid
            if self.radius > ASTEROID_MIN_RADIUS:   # bigger radius than 20
                self.split()                        # split
                return                              # skip
        self.create_shrapnel(mass)


    def create_shrapnel(self, mass):
        while mass > 3:
            random_angle = random.uniform(0, 360)  # Generate a random angle for the shrapnel direction
            velocity_a = self.velocity.rotate(random_angle) * random.uniform(0.1, 2)  # Generate random velocity

            new_radius = random.randrange(1, 3, 1)  # Create a random radius for the shrapnel piece
            shrapnel_piece = Shrapnel(self.position.x, self.position.y, new_radius, self.color)  # Create shrapnel piece

            # Check if velocity is effectively zero (e.g., if the object is stationary)
            if velocity_a.length() == 0:
                # Set a minimum velocity based on PLAYER_SHOT_SPEED to ensure it's not zero
                velocity_a = pygame.Vector2(1, 0).rotate(random_angle) * PLAYER_SHOT_SPEED

            # Apply the velocity to the shrapnel piece
            shrapnel_piece.velocity = velocity_a

            # Ensure shrapnel velocity is at least PLAYER_SHOT_SPEED
            if shrapnel_piece.velocity.length() < PLAYER_SHOT_SPEED/10:
                shrapnel_piece.velocity.scale_to_length(PLAYER_SHOT_SPEED/10)

            mass -= new_radius  # Decrease the remaining mass
            print(f"New shrapnel from {self}, shrapnel mass {new_radius}, remaining mass is {mass}")


class Shrapnel(CircleShape):
    def __init__(self, x, y, radius, RGB=(235, 5, 2)):
        super().__init__(x, y, radius)
        self.lifetime = random.randrange(100, 700, 100)     # Lifetime in milliseconds
        self.spawn_time = pygame.time.get_ticks()
        self.rgb = RGB
        self.angular_velocity = 0                           # Disable angular velocity

    def update(self, dt):
        self.position += self.velocity * dt                 # Update position based on velocity and time delta
        self.velocity *= self.friction                      # Apply linear friction to slow down movement over time
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:  # Remove the shrapnel if its lifetime has expired
            self.kill()

    def draw(self, screen):                                 # Draw the shrapnel as a white circle outline
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius, )
        flame = random.choice(shrapnel_flames)              # Draw random floating flame characters
        FloatingText(self.position.x, self.position.y, (f"{flame}"), self.rgb, 40)
    
    def apply_torque(self, torque):
        pass

