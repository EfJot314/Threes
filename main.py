from game import Game
from menu import Menu, GameOverView



#application main loop
menu = Menu()

while True:
    #get user action
    action = menu.run()

    #quit
    if action == 0:
        break
    #start game
    elif action == 1:
        game = Game(4, 4, 60, 10, menu.screen)
        score = game.run()
        if score > 0:
            game_over = GameOverView(score)
            game_over.run()

