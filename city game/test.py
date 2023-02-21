from city_multiprocess import city_game
game=city_game()
#run this to test if Red Light
#game.afficher()

while(game.isWall() == False):
    game.avancer()
game.droite()


for i in range (3):
    game.avancer()
game.gauche()
for i in range (7):
    game.avancer()
game.droite()
for i in range (3):
    game.avancer()
game.gauche()
for i in range (3):
    game.avancer()
if game.isRedLight():
    print("light is red")
    for i in range (2):
        game.droite()
    for i in range (3):
        game.reculer()
    for i in range(4):
        game.gauche()
    for i in range(8):
        game.avancer()

game.start()

#run this to run a red light
for i in range (4):
    game.avancer()
for i in range (7):
    game.gauche()
for i in range (3):
    game.avancer()
for i in range (3):
    game.gauche()

#run this part to win the game
for i in range (3):
    game.avancer()
for i in range (11):
    game.gauche()
for i in range (8):
    game.avancer()
#game.start()

#run this to collide into a wall
for i in range (4):
    game.avancer()

#show the map without the losing messagebox
game.afficher()
