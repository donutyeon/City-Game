from city_lab_fr import city_game
game=city_game(1)

print(game.distance_euclidienne)
print(game.distance_manhattan)
print(game.distance_XY)

game.gauche()
for i in range(4):
        game.avancer()
game.droite()
for i in range(6):
        print(i)
        game.avancer()
        if game.estFeuRouge():
                game.gauche()
                game.gauche()
game.gauche()
for i in range(10):
        game.avancer()
        if game.estFeuRouge():
                game.gauche()
                game.gauche()
game.lancer()
