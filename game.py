import numpy as np

import pygame
from pygame import *

from directions import Direction

pygame.init()


#colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (220, 220, 220)
dark_gray = (180, 180, 180)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

#images
images = {
    1: pygame.image.load("./resources/threes1.png"),
    2: pygame.image.load("./resources/threes2.png"),
    3: pygame.image.load("./resources/threes3.png"),
    6: pygame.image.load("./resources/threes6.png"),
    12: pygame.image.load("./resources/threes12.png"),
    24: pygame.image.load("./resources/threes24.png"),
    48: pygame.image.load("./resources/threes48.png"),
    96: pygame.image.load("./resources/threes96.png"),
    192: pygame.image.load("./resources/threes192.png"),
    384: pygame.image.load("./resources/threes384.png"),
    768: pygame.image.load("./resources/threes768.png"),
    1536: pygame.image.load("./resources/threes1536.png"),
    3072: pygame.image.load("./resources/threes3072.png"),
    6144: pygame.image.load("./resources/threes6144.png"),
}



class Game:
    def __init__(self, nX: int, nY: int, fps: int, speed: float = 6):
        self.nX = nX
        self.nY = nY
        self.width = 600
        self.height = 700

        self.board = np.zeros((self.nX, self.nY))
        self.tile_tabs = [
                            [1, 2, 3, 3],
                            [1, 2, 3, 3, 3, 3],
                            [1, 2, 3, 3, 3, 3, 3, 6, 6],
                            [1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 3, 3, 6, 6, 6, 12, 12, 24, 24],
                            [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 6, 6, 6, 12, 12, 24, 24, 48, 96],
                            [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 6, 6, 6, 12, 12, 24, 24, 48, 48, 96, 96, 192],
                            [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 6, 6, 6, 12, 12, 24, 24, 48, 48, 96, 96, 192, 384],
                            [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 6, 6, 6, 12, 12, 24, 24, 48, 48, 96, 96, 192, 384, 768],
                            [1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 6, 6, 6, 12, 12, 24, 24, 48, 48, 96, 96, 192, 384, 768, 1536]
                        ]
        
        self.score = 0
        
        self.next_tile = 3
        self.running = True

        self.clock = pygame.time.Clock()
        self.fps = fps
        
        self.moving = True
        self.moving_counter = 0
        self.moving_time = int(self.fps / speed)
        self.moving_board = np.zeros((self.nX+2, self.nY+2))    #+2, because I will use self.nX, self.nY and -1 as indexes
        self.board_copy = self.board.copy()

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Threes -> clone")
        self.score_font = pygame.font.SysFont("monospace", 50, bold=True)

        #first tiles
        for i in range(np.random.randint(2, 4+1)):
            self.new_tile()



    def new_tile(self, edge: Direction = None):
        #select edge
        if edge != None:
            edge = edge.value
        else:
            edge = np.random.randint(1, 4+1)
        #left - right
        while edge % 2 == 0:
            x = (edge-1) // 2
            y = np.random.randint(0, self.nY)
            if self.board[x*(self.nX-1)][y] == 0:
                self.board[x*(self.nX-1)][y] = self.next_tile
                self.moving_board[self.nX+1-x][y] = edge
                break
        #up - down
        while edge % 2 == 1:
            x = np.random.randint(0, self.nX)
            y = abs((edge-1) // 2 - 1)
            if self.board[x][y*(self.nY-1)] == 0:
                self.board[x][y*(self.nY-1)] = self.next_tile
                self.moving_board[x][self.nY+1-y] = edge
                break

        """
        scores:
        1 -> 0
        2 -> 0
        3 -> 3
        6 -> 9
        12 -> 27
        24 -> 81
        48 -> 243
        96 -> 729
        192 -> 2187
        384 -> 6561
        768 -> 19683
        1536 -> 59049
        3072 -> 177147
        6144 -> 531441
        """

        #random next tile
        index = 0
        if self.score > 3 * 9:                      # 3 x 6
            index += 1
        if self.score > 5 * 9:                      # 5 x 6
            index += 1
        if self.score > 3 * 81:                     # 3 x 24
            index += 1
        if self.score > 3 * 729:                    # 3 x 96
            index += 1
        if self.score > 3 * 2187:                   # 3 x 192
            index += 1
        if self.score > 3 * 6561:                   # 3 x 384
            index += 1
        if self.score > 3 * 19683:                  # 3 x 768
            index += 1
        if self.score > 3 * 59049:                  # 3 x 1536
            index += 1
        self.next_tile = np.random.choice(self.tile_tabs[index])

    def draw(self):
        #background
        self.screen.fill(white)

        margin = 20
        hx = self.width / 12
        hy = 1.555555555 * hx   #proportion for pretty scaled images c:
        # hy = self.height / 9

        #UI
        #score
        score_label = self.score_font.render(str(self.score), 1, dark_gray)
        score_rect = score_label.get_rect()
        score_rect.center = (self.width / 2, self.height / 8)
        self.screen.blit(score_label, score_rect)
        #next tile
        pygame.draw.rect(self.screen, dark_gray, (self.width/2-hx/2-margin/2, self.height*7/9-margin/2, hx+2*margin/2, hy+2*margin/2))
        self.screen.blit(pygame.transform.scale(images[self.next_tile], (1*hx, 1*hy)), (self.width/2-hx/2, self.height*7/9))


        #BOARD
        dx = (self.width - self.nX*hx) / 2
        dy = (self.height - self.nY*hy) / 2

        #floor (places)
        pygame.draw.rect(self.screen, gray, (dx-margin, dy-margin, self.nX*hx+2*margin, self.nY*hy+2*margin))
        for i in range(self.nX):
            for j in range(self.nY):
                xi = dx + i*hx
                yi = dy + j*hy
                pygame.draw.rect(self.screen, dark_gray, (xi, yi, 0.95*hx, 0.95*hy))
        #tiles
        for i in range(self.nX):
            for j in range(self.nY):
                xi = dx + i*hx
                yi = dy + j*hy
                #moving tiles
                if self.moving:
                    if self.board_copy[i][j] > 0:
                        if self.moving_board[i][j] == Direction.UP.value:
                            yi = dy + (j - self.moving_counter / self.moving_time) * hy
                        elif self.moving_board[i][j] == Direction.LEFT.value:
                            xi = dx + (i - self.moving_counter / self.moving_time) * hx
                        elif self.moving_board[i][j] == Direction.DOWN.value:
                            yi = dy + (j + self.moving_counter / self.moving_time) * hy
                        elif self.moving_board[i][j] == Direction.RIGHT.value:
                            xi = dx + (i + self.moving_counter / self.moving_time) * hx
                        img = pygame.transform.scale(images[self.board_copy[i][j]], (0.95*hx, 0.95*hy))
                        self.screen.blit(img, (xi, yi))
                #show static tiles
                elif self.board[i][j] > 0:
                    img = pygame.transform.scale(images[self.board[i][j]], (0.95*hx, 0.95*hy))
                    self.screen.blit(img, (xi, yi))
        #moving new tiles (up - down)
        found = False
        for i in range(self.nX):
            if self.moving_board[i][-1] > 0:
                found = True
                xi = dx + i*hx
                yi = dy + (self.moving_counter / self.moving_time - 1) * hy
                img = pygame.transform.scale(images[self.board[i][0]], (0.95*hx, 0.95*hy))
                self.screen.blit(img, (xi, yi))
                break
            elif self.moving_board[i][self.nY] > 0:
                found = True
                xi = dx + i*hx
                yi = dy + (self.nY - self.moving_counter / self.moving_time) * hy
                img = pygame.transform.scale(images[self.board[i][self.nY-1]], (0.95*hx, 0.95*hy))
                self.screen.blit(img, (xi, yi))
                break
        #moving new tiles (left - right)
        if not found:
            for j in range(self.nY):
                if self.moving_board[-1][j] > 0:
                    xi = dx + (self.moving_counter / self.moving_time - 1) * hx
                    yi = dy + j*hy
                    img = pygame.transform.scale(images[self.board[0][j]], (0.95*hx, 0.95*hy))
                    self.screen.blit(img, (xi, yi))
                    break
                elif self.moving_board[self.nX][j] > 0:
                    xi = dx + (self.nX - self.moving_counter / self.moving_time) * hx
                    yi = dy + j*hy
                    img = pygame.transform.scale(images[self.board[self.nX-1][j]], (0.95*hx, 0.95*hy))
                    self.screen.blit(img, (xi, yi))
                    break


    def check_game_over(self):
        for i in range(self.nX):
            for j in range(self.nY):
                if self.board[i][j] == 0:
                    return False
                if i > 0 and ((self.board[i-1][j] == self.board[i][j] and (self.board[i-1][j]+self.board[i][j])%3 == 0) or self.board[i-1][j]+self.board[i][j] == 3):
                    return False
                if j > 0 and ((self.board[i][j-1] == self.board[i][j] and (self.board[i][j-1]+self.board[i][j])%3 == 0) or self.board[i][j-1]+self.board[i][j] == 3):
                    return False
        return True

    def count_score(self):
        """
        scores:
        1 -> 0
        2 -> 0
        3 -> 3
        6 -> 9
        12 -> 27
        24 -> 81
        48 -> 243
        96 -> 729
        192 -> 2187
        384 -> 6561
        768 -> 19683
        1536 -> 59049
        3072 -> 177147
        6144 -> 531441
        """
        self.score = 0
        for i in range(self.nX):
            for j in range(self.nY):
                value = self.board[i][j]
                if value > 2:
                    delta_score = 1
                    while value > 1:
                        delta_score *= 3
                        value //= 3
                    self.score += delta_score

    def move(self, direction: Direction):
        def move_indexes(x: int, y: int, dx: int, dy: int):
            #cannot move empty
            if self.board[x][y] == 0:
                return False
            #empty space
            if self.board[x+dx][y+dy] == 0:
                self.board[x+dx][y+dy] = self.board[x][y]
                self.board[x][y] = 0
                self.moving_board[x][y] = direction.value
                return True
            # 1 
            if self.board[x+dx][y+dy] == 1:
                if self.board[x][y] == 2:
                    self.board[x+dx][y+dy] = 3
                    self.board[x][y] = 0
                    self.moving_board[x][y] = direction.value
                    return True
                return False
            # 2 
            if self.board[x+dx][y+dy] == 2:
                if self.board[x][y] == 1:
                    self.board[x+dx][y+dy] = 3
                    self.board[x][y] = 0
                    self.moving_board[x][y] = direction.value
                    return True
                return False
            #same value
            if self.board[x+dx][y+dy] == self.board[x][y]:
                self.board[x+dx][y+dy] *= 2
                self.board[x][y] = 0
                self.moving_board[x][y] = direction.value
                return True
            return False
        
        toReturn = False
        if direction == Direction.UP:
            for x in range(self.nX):
                for y in range(1, self.nY):
                    toReturn = move_indexes(x, y, 0, -1) or toReturn
        elif direction == Direction.RIGHT:
            for x in range(self.nX-2, -1, -1):
                for y in range(self.nY):
                    toReturn = move_indexes(x, y, 1, 0) or toReturn
        elif direction == Direction.DOWN:
            for x in range(self.nX):
                for y in range(self.nY-2, -1, -1):
                    toReturn = move_indexes(x, y, 0, 1) or toReturn
        elif direction == Direction.LEFT:
            for x in range(1, self.nX):
                for y in range(self.nY):
                    toReturn = move_indexes(x, y, -1, 0) or toReturn
        return toReturn
        
    
    def run(self):
        #main loop
        self.running = True
        while self.running:

            #get screen size
            self.width, self.height = self.screen.get_size()

            #check if game is over
            if self.check_game_over():
                self.running = False

            #moving tiles (visualization)
            if self.moving:
                self.moving_counter += 1
                if self.moving_counter >= self.moving_time:
                    self.moving = False
                    self.moving_counter = 0
                    self.moving_board = np.zeros((self.nX+2, self.nY+2))    #+2, because I will use self.nX, self.nY and -1 as indexes
            
            #score
            self.count_score()

            
            #drawing
            self.draw()


            #event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    #moving
                    elif not self.moving:
                        self.board_copy = self.board.copy()
                        if event.key == pygame.K_UP:
                            if self.move(Direction.UP):
                                self.new_tile(Direction.UP)
                                self.moving = True
                            break
                        elif event.key == pygame.K_RIGHT:
                            if self.move(Direction.RIGHT):
                                self.new_tile(Direction.RIGHT)
                                self.moving = True
                            break
                        elif event.key == pygame.K_DOWN:
                            if self.move(Direction.DOWN):
                                self.new_tile(Direction.DOWN)
                                self.moving = True
                            break
                        elif event.key == pygame.K_LEFT:
                            if self.move(Direction.LEFT):
                                self.new_tile(Direction.LEFT)
                                self.moving = True
                            break



            #time control and refreshing display
            self.clock.tick(self.fps)
            pygame.display.flip()

        
        #exit pygame
        pygame.quit()







            











