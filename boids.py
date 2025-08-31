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
        """Avoids screen warping/flashing"""
        if self.position.x > WIDTH: self.position.x = 0
        if self.position.x < 0: self.position.x = WIDTH
        if self.position.y > HEIGHT: self.position.y = 0
        if self.position.y < 0: self.position.y = HEIGHT

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
            b.update()
            b.show(screen)

        # updates the surface display per frame
        pygame.display.flip()
        # For the FPS
        clock.tick(60)

if __name__ == "__main__":
    main()