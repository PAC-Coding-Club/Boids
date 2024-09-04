import pygame
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

alignment_multiplier = 2
cohesion_multiplier = 2
separation_multiplier = 2

boid_list = []

class Boid:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.max_speed = 4
        self.max_force = 0.1
        self.rect = pygame.Rect(x, y, 10, 10)

        boid_list.append(self)

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

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def flock(self, boids):
        alignment = self.align(boids) * alignment_multiplier
        cohesion = self.cohere(boids) * cohesion_multiplier
        separation = self.separate(boids) * separation_multiplier

        # Apply behaviours
        self.velocity += alignment + cohesion + separation

    def align(self, boids):
        perception_radius = 50
        steering = pygame.Vector2(0, 0)
        total = 0
        avg_velocity = pygame.Vector2(0, 0)
        for boid in boids:
            if boid != self and self.pos.distance_to(boid.pos) < perception_radius:
                avg_velocity += boid.velocity
                total += 1
        if total > 0:
            avg_velocity /= total
            avg_velocity = avg_velocity.normalize() * self.max_speed
            steering = avg_velocity - self.velocity
            steering = steering.normalize() * self.max_force
        return steering

    def cohere(self, boids):
        perception_radius = 50
        steering = pygame.Vector2(0, 0)
        total = 0
        centre_of_mass = pygame.Vector2(0, 0)
        for boid in boids:
            if boid != self and self.pos.distance_to(boid.pos) < perception_radius:
                centre_of_mass += boid.pos
                total += 1
        if total > 0:
            centre_of_mass /= total
            vector_to_com = centre_of_mass - self.pos
            vector_to_com = vector_to_com.normalize() * self.max_speed
            steering = vector_to_com - self.velocity
            steering = steering.normalize() * self.max_force
        return steering

    def separate(self, boids):
        perception_radius = 25
        steering = pygame.Vector2(0, 0)
        total = 0
        for boid in boids:
            distance = self.pos.distance_to(boid.pos)
            if boid != self and distance < perception_radius:
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
