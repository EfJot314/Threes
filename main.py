import pygame, sys

from game import Game
from menu import Menu, GameOverView





#application main loop
menu = Menu()
running = True
while running:
    #get user action
    action = menu.run()

    #quit
    if action == 0:
        break
    #start game
    elif action == 1:
        while True:
            game = Game(4, 4, 60, 10, menu.screen)
            feedback = game.run()
            #quit
            if feedback < 0:
                running = False
                break
            #game over
            elif feedback > 0:
                game_over = GameOverView(feedback)
                over_action = game_over.run()
                #quit
                if over_action == 0:
                    running = False
                    break
                #guit to menu
                elif over_action == 1:
                    break



pygame.quit()


