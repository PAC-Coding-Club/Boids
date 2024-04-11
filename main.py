import math
import random

import pygame
debug = True
speed = 1
turn_speed = math.pi / 180 * 3

class Boid(pygame.sprite.Sprite):
    def __init__(self, game, pos, *groups: pygame.sprite.Group):
        super().__init__(*groups)

        self.game = game

        self.pos = pygame.Vector2(pos)

        self.angle = math.radians(random.randint(0, 360))

        self.image = pygame.Surface((10, 10))
        self.image.fill("red")
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.pos += pygame.Vector2(math.cos(self.angle), math.sin(self.angle)) * speed
        self.rect.center = self.pos

        for boid in self.game.boids:
            if boid == self:
                continue
            if self.pos.distance_to(boid.pos) < 60:
                # average their angles
                average = (self.angle + boid.angle) / 2
                if self.angle < average - turn_speed:
                    self.angle += 0.01
                elif self.angle > average + turn_speed:
                    self.angle -= 0.01

            # turn away from walls
            if self.pos.x < 0 or self.pos.x > 800 or self.pos.y < 0 or self.pos.y > 600:
                self.angle += 0.01


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))

        self.boids = pygame.sprite.Group()

    def render(self):
        self.screen.fill((255, 255, 255))

        self.boids.draw(self.screen)
        if debug:
            for boid in self.boids:
                pygame.draw.line(self.screen, "black", boid.pos, boid.pos + pygame.Vector2(math.cos(boid.angle), math.sin(boid.angle)) * 50)

        pygame.display.update()

    def update(self):
        self.boids.update()

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    Boid(self, pygame.mouse.get_pos(), self.boids)

            self.update()
            self.render()
            self.clock.tick(60)

Game().start()