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

        self.title_font = pygame.font.SysFont("monospace", 50, bold=True)
        self.font = pygame.font.SysFont("monospace", 30, bold=True)

        self.mousePos = pygame.mouse.get_pos()

        self.overPlay, self.overQuit = False, False


    def draw(self):
        #background
        self.screen.fill(white)

        #title label
        title_label = self.title_font.render("Threes!", 1, black)
        title_rect = title_label.get_rect()
        title_rect.center = (self.width / 2, self.height / 8)
        self.screen.blit(title_label, title_rect)

        #play button
        play_label = self.font.render("play", 1, black)
        play_rect = play_label.get_rect()
        play_rect.center = (self.width / 2, self.height * 3 / 8)
        if play_rect.scale_by(1.5).collidepoint(self.mousePos):
            self.overPlay = True
            pygame.draw.rect(self.screen, dark_gray, play_rect.scale_by(1.5))
        else:
            self.overPlay = False
            pygame.draw.rect(self.screen, gray, play_rect.scale_by(1.5))
        self.screen.blit(play_label, play_rect)

        #quit button
        quit_label = self.font.render("quit", 1, black)
        quit_rect = quit_label.get_rect()
        quit_rect.center = (self.width / 2, self.height * 4 / 8)
        if quit_rect.scale_by(1.5).collidepoint(self.mousePos):
            self.overQuit = True
            pygame.draw.rect(self.screen, dark_gray, quit_rect.scale_by(1.5))
        else:
            self.overQuit = False
            pygame.draw.rect(self.screen, gray, quit_rect.scale_by(1.5))
        self.screen.blit(quit_label, quit_rect)


    def run(self):

        while True:
            #get mouse position
            self.mousePos = pygame.mouse.get_pos()

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.overQuit:
                        return 0
                    elif self.overPlay:
                        return 1



            #time control and refreshing screen
            self.clock.tick(self.fps)
            pygame.display.flip()



class GameOverView:
    def __init__(self, score: int, screen: pygame.surface.Surface = None):
        self.score = score

        self.width = 600
        self.height = 700

        self.clock = pygame.time.Clock()
        self.fps = 60

        self.screen = screen
        if self.screen == None:
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Threes -> clone")
        else:
            self.width, self.height = self.screen.get_size()

        self.title_font = pygame.font.SysFont("monospace", 50, bold=True)
        self.font = pygame.font.SysFont("monospace", 30, bold=True)

        self.mousePos = pygame.mouse.get_pos()

        self.overRetry, self.overMenu, self.overQuit = False, False, False

    
    def draw(self):
        self.screen.fill(white)

        #game over label
        game_over_label = self.title_font.render("Game Over", 1, black)
        game_over_rect = game_over_label.get_rect()
        game_over_rect.center = (self.width / 2, self.height / 8)
        self.screen.blit(game_over_label, game_over_rect)

        #retry button
        retry_label = self.font.render("retry", 1, black)
        retry_rect = retry_label.get_rect()
        retry_rect.center = (self.width / 2, self.height * 3 / 8)
        if retry_rect.scale_by(1.5).collidepoint(self.mousePos):
            self.overRetry = True
            pygame.draw.rect(self.screen, dark_gray, retry_rect.scale_by(1.5))
        else:
            self.overRetry = False
            pygame.draw.rect(self.screen, gray, retry_rect.scale_by(1.5))
        self.screen.blit(retry_label, retry_rect)

        #quit to menu button
        menu_label = self.font.render("menu", 1, black)
        menu_rect = menu_label.get_rect()
        menu_rect.center = (self.width / 2, self.height * 4 / 8)
        if menu_rect.scale_by(1.5).collidepoint(self.mousePos):
            self.overMenu = True
            pygame.draw.rect(self.screen, dark_gray, menu_rect.scale_by(1.5))
        else:
            self.overMenu = False
            pygame.draw.rect(self.screen, gray, menu_rect.scale_by(1.5))
        self.screen.blit(menu_label, menu_rect)

        #quit button
        quit_label = self.font.render("quit", 1, black)
        quit_rect = quit_label.get_rect()
        quit_rect.center = (self.width / 2, self.height * 5 / 8)
        if quit_rect.scale_by(1.5).collidepoint(self.mousePos):
            self.overQuit = True
            pygame.draw.rect(self.screen, dark_gray, quit_rect.scale_by(1.5))
        else:
            self.overQuit = False
            pygame.draw.rect(self.screen, gray, quit_rect.scale_by(1.5))
        self.screen.blit(quit_label, quit_rect)


    def run(self):
        while True:
            #get mouse position
            self.mousePos = pygame.mouse.get_pos()

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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.overQuit:
                        return 0
                    elif self.overMenu:
                        return 1
                    elif self.overRetry:
                        return 2



            #time control and refreshing screen
            self.clock.tick(self.fps)
            pygame.display.flip()










