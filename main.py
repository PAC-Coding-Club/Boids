import pygame


class Game:
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((800, 600))

        # Initilize Variables

    def render(self):
        self.screen.fill((255, 255, 255))
        # Render Variables
        pygame.display.update()

    def update(self):
        # Update Variables
        print("update")

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.update()
            self.render()
            self.clock.tick(60)


Game().start()
