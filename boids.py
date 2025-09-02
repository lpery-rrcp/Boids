# Name: Lance Pery
# Date: Augest, 28, 2025
# Description: Boids simulator. 
#   Simulates the flocking behaviour using 3 steering rules: Separation, Alignment, and Cohesion.

# imports
import pygame
import random
import math

# Screen Variables
WIDTH = 800
HEIGHT = 600
SCREEN_COLOR = (30, 30, 150)
BOID_COLOR = (200, 200, 255)

# Boids Variables
NUM_BOIDS = 60
SPEED = 4
FORCE = 0.05
PERCEPTION_RADIUS = 50

# Behavior Weights
ALIGN_WEIGHT = 1.0
COHESION_WEIGHT = 1.0
SEPARATION_WEIGHT = 1.5

class Boids:
    """Spawns boids to simulate flock of birds."""
    def __init__(self):
        self.position = pygame.math.Vector2(
            random.uniform(0, WIDTH),
            random.uniform(0, HEIGHT)
        )
        angle = random.uniform(0, math.pi * 2)
        self.velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle))
        self.velocity.scale_to_length(random.uniform(2, SPEED))
        self.acceleration = pygame.math.Vector2(0, 0)

    def update(self):
        self.velocity += self.acceleration
        if self.velocity.length() > SPEED:
            self.velocity.scale_to_length(SPEED)
        self.position += self.velocity
        self.acceleration.update(0, 0) # resets each frame

    def show(self, screen):
        """Draws triagles that point to the direction the boids go."""
        angle = self.velocity.angle_to(pygame.math.Vector2(1, 0))
        points = [
            (self.position + pygame.math.Vector2(10, 0).rotate(-angle)),
            (self.position + pygame.math.Vector2(-10, 5).rotate(-angle)),
            (self.position + pygame.math.Vector2(-10, -5).rotate(-angle)),
        ]

        pygame.draw.polygon(screen, BOID_COLOR, points)

    def edges(self):
        """Avoids screen warping"""
        if self.position.x > WIDTH: self.position.x = 0
        if self.position.x < 0: self.position.x = WIDTH
        if self.position.y > HEIGHT: self.position.y = 0
        if self.position.y < 0: self.position.y = HEIGHT

    def neighbors(self, boids, radius=PERCEPTION_RADIUS):
        """Finds which boids are the closest to it."""
        result = []
        for other in boids:
            if other is self:
                continue
            if self.position.distance_to(other.position) < radius:
                result.append(other)
        return result
    
    def align(self, boids):
        """Alignment rule: finds nearby boids and make them go in the same velocity."""

        neigh = self.neighbors(boids, PERCEPTION_RADIUS)
        if not neigh:
            return pygame.math.Vector2()
        
        # Average neighbor velocities
        avg_vec = pygame.math.Vector2()
        for n in neigh:
            avg_vec += n.velocity
        avg_vec /= len(neigh)

        # Convert average to desired velocity
        if avg_vec.length() > 0:
            avg_vec = avg_vec.normalize() * SPEED

        # Steering = desired - current velocity (limited by FORCE)
        steer = avg_vec - self.velocity
        if steer.length() > FORCE:
            steer.scale_to_length(FORCE)
        return steer
    
    def cohesion(self, boids):
        """Cohesion rule: finds nearby boids and make them go in the same direction."""
        neigh = self.neighbors(boids, PERCEPTION_RADIUS)
        if not neigh:
            return pygame.math.Vector2()
        
        center = pygame.math.Vector2()
        for o in neigh:
            center += o.position
        center /= len(neigh)

        desired = center - self.position
        if desired.length() > 0:
            desired = desired.normalize() * SPEED

        steer = desired - self.velocity
        if steer.length() > FORCE:
            steer.scale_to_length(FORCE)
        return steer
    
    def separation(self, boids):
        """Seperation rule: finds nearby boids and makes sure to avoid collisions."""
        neigh = self.neighbors(boids, )
        if not neigh:
            return pygame.math.Vector2()
        
        steer = pygame.math.Vector2()
        for o in neigh:
            diff = self.position - o.position
            dist = diff.length()
            if dist> 0:
                diff /= dist # weight nby distance
            steer += diff

        steer /= len(neigh)
        if steer.length() > 0:
            steer = steer.normalize() * SPEED - self.velocity
            if steer.length() > FORCE:
                steer.scale_to_length(FORCE)
        return steer
    
    def flock(self, boids):
        alignment = self.align(boids) * ALIGN_WEIGHT
        cohesion = self.cohesion(boids) * COHESION_WEIGHT
        separation = self.separation(boids) * SEPARATION_WEIGHT

        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    boids = [Boids() for _ in range(NUM_BOIDS)]
    
    running = True
    while running:
        # for exiting the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(SCREEN_COLOR)   

        # Drawing the Boids
        for b in boids:
            b.edges()
            b.flock(boids)
            b.update()
            b.show(screen)

        # updates the surface display per frame
        pygame.display.flip()
        # For the FPS
        clock.tick(60)

if __name__ == "__main__":
    main()