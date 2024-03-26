import numpy as np
from enum import Enum
import pygame
from pygame import *


pygame.init()


#colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (220, 220, 220)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#directions
class Direction(Enum):
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4
    






class Game:
    def __init__(self, nX: int, nY: int, fps: int):
        self.nX = nX
        self.nY = nY
        self.width = 600
        self.height = 700
        self.board = np.zeros((self.nX, self.nY))
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = fps

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("monospace", 25)

        #first tiles
        for i in range(np.random.randint(2, 4+1)):
            self.new_tile()

    def new_tile(self, edge: Direction = None):
        if edge != None:
            edge = edge.value
        else:
            edge = np.random.randint(1, 4+1)
        while True:
            if edge % 2 == 0:
                x = int((edge-2)/2 * (self.nX-1))
                y = np.random.randint(0, self.nY)
                if self.board[x][y] == 0:
                    self.board[x][y] = 3
                    break
            else:
                x = np.random.randint(0, self.nX)
                y = int((3-edge)/2 * (self.nY-1))
                if self.board[x][y] == 0:
                    self.board[x][y] = 3
                    break

    def draw(self):
        self.screen.fill(white)

        hx = self.width / 10
        hy = self.height / 10

        dx = (self.width - self.nX*hx) / 2
        dy = (self.height - self.nY*hy) / 2

        for i in range(self.nX):
            for j in range(self.nY):
                xi = dx + i*hx
                yi =dy + j*hy
                pygame.draw.rect(self.screen, gray, (xi, yi, 0.95*hx, 0.95*hy))
                if self.board[i][j] != 0:
                    color_delta = min(3 * self.board[i][j], 100)
                    pygame.draw.rect(self.screen, (200-color_delta, 200-color_delta, 200-color_delta), (xi, yi, 0.95*hx, 0.95*hy))
                    number_label = self.font.render(str(int(self.board[i][j])), 1, black)
                    label_rect = number_label.get_bounding_rect()
                    label_rect.center = (xi+hx/2, yi+hy/2)
                    self.screen.blit(number_label, label_rect)


    def move(self, direction: Direction):
        toReturn = False
        if direction == Direction.UP:
            for x in range(self.nX):
                for y in range(1, self.nY):
                    #empty space
                    if self.board[x][y-1] == 0:
                        self.board[x][y-1] = self.board[x][y]
                        self.board[x][y] = 0
                        toReturn = True
                    #same value
                    elif self.board[x][y-1] == self.board[x][y]:
                        self.board[x][y-1] *= 2
                        self.board[x][y] = 0
                        toReturn = True
        elif direction == Direction.RIGHT:
            for x in range(self.nX-2, -1, -1):
                for y in range(self.nY):
                    #empty space
                    if self.board[x+1][y] == 0:
                        self.board[x+1][y] = self.board[x][y]
                        self.board[x][y] = 0
                        toReturn = True
                    #same value
                    elif self.board[x+1][y] == self.board[x][y]:
                        self.board[x+1][y] *= 2
                        self.board[x][y] = 0
                        toReturn = True
        elif direction == Direction.DOWN:
            for x in range(self.nX):
                for y in range(self.nY-2, -1, -1):
                    #empty space
                    if self.board[x][y+1] == 0:
                        self.board[x][y+1] = self.board[x][y]
                        self.board[x][y] = 0
                        toReturn = True
                    #same value
                    elif self.board[x][y+1] == self.board[x][y]:
                        self.board[x][y+1] *= 2
                        self.board[x][y] = 0
                        toReturn = True
        elif direction == Direction.LEFT:
            for x in range(1, self.nX):
                for y in range(self.nY):
                    #empty space
                    if self.board[x-1][y] == 0:
                        self.board[x-1][y] = self.board[x][y]
                        self.board[x][y] = 0
                        toReturn = True
                    #same value
                    elif self.board[x-1][y] == self.board[x][y]:
                        self.board[x-1][y] *= 2
                        self.board[x][y] = 0
                        toReturn = True
        return toReturn
        
    
    def run(self):
        #main loop
        self.running = True
        while self.running:

            #get screen size
            self.width, self.height = self.screen.get_size()

            #drawing
            self.draw()


            #event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_UP:
                        if self.move(Direction.UP):
                            self.new_tile(Direction.UP)
                        break
                    elif event.key == pygame.K_RIGHT:
                        if self.move(Direction.RIGHT):
                            self.new_tile(Direction.RIGHT)
                        break
                    elif event.key == pygame.K_DOWN:
                        if self.move(Direction.DOWN):
                            self.new_tile(Direction.DOWN)
                        break
                    elif event.key == pygame.K_LEFT:
                        if self.move(Direction.LEFT):
                            self.new_tile(Direction.LEFT)
                        break



            #time control and refresh display
            self.clock.tick(self.fps)
            pygame.display.flip()
        
        #exit pygame
        pygame.quit()


game = Game(4, 5, 60)
game.run()

            











