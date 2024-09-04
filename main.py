import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

boid_list = []

class Boid:
    def __init__(self, x, y):
        self.pos = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.randint(0, 100)/100, random.randint(0, 100)/100)
        self.total_velocity = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(x, y, 10, 10)

        boid_list.append(self)

    def update(self):
        other_boids = boid_list.copy()
        other_boids.remove(self)
        if len(other_boids) > 0:
            # Calculate the cohesion vector
            total_locations = pygame.Vector2(0, 0)
            for boid in other_boids:
                total_locations += boid.pos
            average_position = total_locations // len(other_boids)

            cohesion_vector = pygame.Vector2(average_position - self.pos)


            # Calculate the alignment vector
            total_velocity = pygame.Vector2(0, 0)
            for boid in other_boids:
                total_velocity += boid.velocity
            average_velocity = total_velocity // len(other_boids)

            alignment_vector = pygame.Vector2(average_velocity - self.pos)

            cohesion_vector.scale_to_length(1)
            alignment_vector.scale_to_length(1)

            self.total_velocity += cohesion_vector
            self.total_velocity += alignment_vector

            if cohesion_vector.length() >= 1:
                print("yes")

        self.total_velocity += self.velocity

        self.velocity = self.total_velocity // 3

        self.total_velocity = pygame.Vector2(0, 0)

        if self.velocity.length() > 1:
            self.velocity.scale_to_length(1)

        self.pos += self.velocity
        self.rect.center = self.pos

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            Boid(event.pos[0], event.pos[1])

    for boid in boid_list:
        boid.update()
        boid.draw(screen)

    pygame.display.update()
    screen.fill((60, 60, 60))
    clock.tick(60)