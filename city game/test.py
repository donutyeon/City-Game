from city_multiprocess import city_game
game=city_game()
for i in range (3):
    game.avancer()
for i in range (11):
    game.gauche()
for i in range (7):
    game.avancer()
game.start()