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
NUM_BOIDS = 6
SPEED = 10
FORCE = 0.05
PERCEPTION_RADIUS = 50

# mouse repeling
CLICK_RADIUS = 80
CLICK_FORCE = 0.5

# Behavior Weights (the 3 steering forces)
ALIGN_WEIGHT = 1.0
COHESION_WEIGHT = 1.0
SEPARATION_WEIGHT = 1.5

class Boids:
    """A boid holds position, velocity, acceleration, and steering behaviors."""
    def __init__(self):
        self.position = pygame.math.Vector2(
            random.uniform(0, WIDTH),
            random.uniform(0, HEIGHT)
        )
        #Random starting heading angle. -> converts to a direction vector
        angle = random.uniform(0, math.pi * 2)
        self.velocity = pygame.math.Vector2(math.cos(angle), math.sin(angle))
        # Give initial velocity a random length between 2 and SPEED for varaity of motion.
        self.velocity.scale_to_length(random.uniform(2, SPEED))
        self.acceleration = pygame.math.Vector2(0, 0)

    def update(self):
        """Apply acceleration to velocity, clamp to SPEED, update position, and reset acceleration."""
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
        """Avoids screen warping:
        - if boids goes out of the screen then it appears on the opposite side.
        """
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
    
    def mouse_repulsion(self, mouse_pos):
        """Extra force: repels boids away from mouse click."""
        diff = self.position - pygame.math.Vector2(mouse_pos)
        dist = diff.length()
        if 0.001 < dist < CLICK_RADIUS:
            # stregth will fade further away from the center
            repel = diff.normalize() * (CLICK_FORCE * (CLICK_RADIUS - dist) / CLICK_RADIUS)
            return repel
        return pygame.math.Vector2()

    def flock(self, boids, mouse_pos=None, mouse_pressed=False):
        """Combines the 3 steering behaviors: Alignment, Cohesion, and Seperation. And click seperation.
        - Each behavior is multiply by its weight.
        """
        alignment = self.align(boids) * ALIGN_WEIGHT
        cohesion = self.cohesion(boids) * COHESION_WEIGHT
        separation = self.separation(boids) * SEPARATION_WEIGHT

        self.acceleration += alignment
        self.acceleration += cohesion
        self.acceleration += separation

        if mouse_pressed and mouse_pos is not None:
            self.acceleration += self.mouse_repulsion(mouse_pos)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    
    # Creates boids list. look up spacial hashing
    boids = [Boids() for _ in range(NUM_BOIDS)]

    # Pause / add / remove boids
    paused = False
    
    running = True
    while running:
        # Mouse clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # for exiting the screen
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # for Pause / add / remove boids
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused # toggled pause
                elif event.key == pygame.K_a:
                    boids.append(Boids()) # add a boid
                elif event.key == pygame.K_r:
                    if boids:
                        boids.pop() # remove a boid


        screen.fill(SCREEN_COLOR)   

        # Drawing the Boids
        for b in boids:
            b.edges()       # wrap-around boundaries
            if not paused:
                b.flock(boids, mouse_pos, mouse_pressed)  # compute steering forces based on neighbors
                b.update()      # apply acceleration and move
            b.show(screen)  # render to the screen

        if mouse_pressed:
            pygame.draw.circle(screen, (255, 50, 50), mouse_pos, CLICK_RADIUS, 2)

        # updates the surface display per frame
        pygame.display.flip()
        # For the FPS
        clock.tick(60)

if __name__ == "__main__":
    main()