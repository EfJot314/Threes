import pygame
from pygame import *

pygame.init()




#colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (220, 220, 220)
dark_gray = (180, 180, 180)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)




class Menu:
    def __init__(self):
        self.width = 600
        self.height = 700
        
        self.clock = pygame.time.Clock()
        self.fps = 60

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Threes -> clone")

        self.font = pygame.font.SysFont("monospace", 30, bold=True)


    def draw(self):
        self.screen.fill(white)

    def run(self):

        while True:

            #drawing
            self.draw()


            #event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 0
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return 0
                    elif event.key == pygame.K_SPACE:
                        return 1



            #time control and refreshing display
            self.clock.tick(self.fps)
            pygame.display.flip()













