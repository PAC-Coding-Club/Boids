import math
import random
import pygame

debug = False
speed = 1
turn_speed = math.pi / 180 * 1
vision_distance = 100
wall_offset = 100
simulation_speed = 200  # updates per second
screen_size = (1000, 1000)


class Boid(pygame.sprite.Sprite):
    def __init__(self, game, pos, *groups: pygame.sprite.Group):
        super().__init__(*groups)

        self.evadingWall = False
        self.game = game
        self.pos = pygame.Vector2(pos)
        self.angle = math.radians(random.randint(0, 360))
        self.image = pygame.Surface((10, 10))
        self.image.fill("blue")
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.pos += pygame.Vector2(math.cos(self.angle), -math.sin(self.angle)) * speed
        self.rect.center = self.pos

        for boid in self.game.boids:
            if boid == self:
                continue

            if self.pos.distance_to(boid.pos) < vision_distance and not self.evadingWall:
                # average their angles
                average = (self.angle + boid.angle) / 2
                if self.angle < average:
                    self.angle += turn_speed
                elif self.angle > average:
                    self.angle -= turn_speed

            if self.pos.distance_to(boid.pos) <= self.rect.x:
                # point angles away from each-other as to not collide
                pass

        # turn away from walls
        if self.pos.x < 0 + wall_offset:
            self.evadingWall = True
            if self.angle >= math.pi:
                self.angle += turn_speed
            elif self.angle < math.pi:
                self.angle -= turn_speed
        elif self.pos.x > self.game.screen.get_width() - wall_offset:
            self.evadingWall = True
            if self.angle <= math.pi:
                self.angle += turn_speed
            elif self.angle < math.pi * 2:
                self.angle -= turn_speed
        elif self.pos.y < 0 + wall_offset:
            self.evadingWall = True
            if self.angle >= math.pi / 2:
                self.angle += turn_speed
            elif self.angle < math.pi / 2 or self.angle >= math.pi + (
                    math.pi / 2):  # less than up, or more than right (zero is to the right)
                self.angle -= turn_speed
        elif self.pos.y > self.game.screen.get_height() - wall_offset:
            self.evadingWall = True
            if self.angle >= math.pi + (math.pi / 2) or self.angle < (
                    math.pi / 2):  # less than down, or less than up (zero is to the right)
                self.angle += turn_speed
            elif self.angle < math.pi + (math.pi / 2):
                self.angle -= turn_speed
        else:
            self.evadingWall = False

        # collide with walls
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > self.game.screen.get_width():
            self.pos.x = self.game.screen.get_width()
        if self.pos.y < 0:
            self.pos.y = 0
        if self.pos.y > self.game.screen.get_height():
            self.pos.y = self.game.screen.get_height()

        if self.angle > math.pi * 2:
            self.angle -= math.pi * 2
        if self.angle < 0:
            self.angle += math.pi * 2


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(screen_size)

        self.boids = pygame.sprite.Group()

    def render(self):
        self.screen.fill((255, 255, 255))

        if debug:
            for boid in self.boids:
                pygame.draw.circle(self.screen, "black", boid.pos, vision_distance)
                pygame.draw.line(self.screen, "red", boid.pos, boid.pos + pygame.Vector2(math.cos(boid.angle), -math.sin(boid.angle)) * 50)
        self.boids.draw(self.screen)

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
            self.clock.tick(simulation_speed)


Game().start()
