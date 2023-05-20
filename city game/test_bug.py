from city_lab import city_game
game=city_game(1)

game.gauche()
for i in range(4):
        game.avancer()
game.droite()
for i in range(6):
        print(i)
        game.avancer()
        if game.isRedLight():
                game.gauche()
                game.gauche()
game.gauche()
for i in range(10):
        game.avancer()
        if(game.isRedLight()):
                game.gauche()
                game.gauche()
game.start()
