from game import Game
from menu import Menu



menu = Menu()

while True:
    action = menu.run()

    #quit
    if action == 0:
        break
    #start game
    elif action == 1:
        game = Game(4, 4, 60, 10)
        game.run()


