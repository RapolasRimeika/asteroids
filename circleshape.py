import pygame
import random
from floating_text import FloatingText

# Base class for circular game objects with full inertia and friction
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, friction=0.995, angular_friction=0.95):
        # Initialize sprite and add to groups if containers are set
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

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

        if self.health <= 0:
            self.shrapnel_obj(self.radius)

    def collision(self, other, bounce=True):
        # Check for collision with another CircleShape
        distance = self.position.distance_to(other.position)
        if self.radius + other.radius > distance:
            self.health -= other.radius * other.speed
            if bounce:
                self.bounce(other)
            return True
        return False

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

    def shrapnel_obj(self, mass, RGB=(150, 150, 150)):
        while mass > 1:
            random_angle = random.uniform(0, 360)
            velocity_a = self.velocity.rotate(random_angle) * random.uniform(0.5, 2.5)
            new_radius = random.uniform(2, 5)
            # Spawn shrapnel
            shrapnel_piece = Shrapnel(self.position.x, self.position.y, new_radius, RGB)
            shrapnel_piece.velocity = velocity_a
            mass -= new_radius
            self.kill()

class Shrapnel(CircleShape):
    def __init__(self, x, y, radius, RGB=(235, 5, 2)):
        super().__init__(x, y, radius)
        self.lifetime = 700  # Lifetime in milliseconds
        self.spawn_time = pygame.time.get_ticks()
        self.rgb = RGB

    def draw(self, screen):
        # Draw the asteroid as a white circle
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)
        flames = ["§", "¶", "∞", "∑", "≈", "Ω", "µ", "∆", "∫", "≈", "¬", "π", "≠", "√", "≤"]
        flame = random.choice(flames)
        FloatingText(self.position.x, self.position.y, (f"{flame}"), self.rgb, 40)

    def update(self, dt):
        # Update position based on velocity and time delta
        self.position += self.velocity * dt
         # Remove the shrapnel if its lifetime has expired
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.kill()