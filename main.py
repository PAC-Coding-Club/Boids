import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

align_multiplier = 2
cohere_multiplier = 3
separate_multiplier = 10

align_perception_radius = 100
cohere_perception_radius = 50
separate_perception_radius = 15

boid_list = []


class Boid:
    # Initializing the boid with all required variables
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.max_speed = 4
        self.max_force = 0.1
        self.rect = pygame.Rect(x, y, 10, 10)

        boid_list.append(self)

    # Main update code for each boid
    def update(self):
        self.flock(boid_list)
        self.pos += self.velocity
        self.rect.center = self.pos
        self.velocity = self.velocity.normalize() * self.max_speed

        # Wrap around screen edges
        if self.pos.x < 0: self.pos.x = 800
        if self.pos.x > 800: self.pos.x = 0
        if self.pos.y < 0: self.pos.y = 600
        if self.pos.y > 600: self.pos.y = 0

    # Simple draw method
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    # Flock method runs each method affecting the boid's direction
    def flock(self, boids):
        alignment = self.align(boids) * align_multiplier
        cohesion = self.cohere(boids) * cohere_multiplier
        separation = self.separate(boids) * separate_multiplier

        # Apply behaviours
        self.velocity += alignment + cohesion + separation

    # Align calculates the average direction of all boids within 50 pixels and matches their direction
    def align(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        avg_velocity = pygame.Vector2(0, 0)
        for boid in boids:
            if boid != self and self.pos.distance_to(boid.pos) < align_perception_radius:
                avg_velocity += boid.velocity
                total += 1
        if total > 0:
            avg_velocity /= total
            avg_velocity = avg_velocity.normalize() * self.max_speed
            steering = avg_velocity - self.velocity
            steering = steering.normalize() * self.max_force
        return steering

    # Cohere calculates the center point (or average position) of all the boids within 50 pixels and steers toward that point
    def cohere(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        centre_of_mass = pygame.Vector2(0, 0)
        for boid in boids:
            if boid != self and self.pos.distance_to(boid.pos) < cohere_perception_radius:
                centre_of_mass += boid.pos
                total += 1
        if total > 0:
            centre_of_mass /= total
            vector_to_com = centre_of_mass - self.pos
            vector_to_com = vector_to_com.normalize() * self.max_speed
            steering = vector_to_com - self.velocity
            steering = steering.normalize() * self.max_force
        return steering

    # Separation method forces boids to steer away from boids closest to themselves to avoid colliding
    def separate(self, boids):
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            distance = self.pos.distance_to(boid.pos)
            if boid != self and distance < separate_perception_radius:
                diff = self.pos - boid.pos
                diff = diff.normalize() / distance
                steering += diff
                total += 1
        if total > 0:
            steering /= total
        if steering.magnitude() > 0:
            steering = steering.normalize() * self.max_speed
            steering -= self.velocity
            steering = steering.normalize() * self.max_force
        return steering


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            Boid(event.pos[0], event.pos[1])

    screen.fill((60, 60, 60))

    for boid in boid_list:
        boid.update()
        boid.draw(screen)

    pygame.display.flip()
    clock.tick(60)
