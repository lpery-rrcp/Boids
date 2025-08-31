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
SCREEN_COLOR = (30, 30, 30)
BOID_COLOR = (200, 200, 255)

class Boids:
    pass

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    running = True
    while running:
        screen.fill(SCREEN_COLOR)

        # for exiting the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # For the FPS
        clock.tick(60)

if __name__ == "__main__":
    main()