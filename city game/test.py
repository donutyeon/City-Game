from city_lab import city_game
game=city_game(1)

#Distance at the start of the game
print('Euclidean distance: ',game.euclidean_distance())
print('Manhattan distance: ',game.manhattan_distance())
print('XY distance: ',game.XY_distance())

#run this to show the map 
#game.afficher()

#Run this to win the game
for i in range (3):
    game.avancer()
game.gauche()
for i in range (7):
    game.avancer()
game.droite()
for i in range (3):
    game.avancer()
game.gauche()
for i in range (2):
    game.avancer()
if game.isRedLight():
    print("light is red")
    for i in range (2):
        game.droite()
    for i in range (2):
        game.avancer()
    game.gauche()
    for i in range(4):
        game.avancer()
    game.gauche()
    print('Euclidean distance: ',game.euclidean_distance())
    print('Manhattan distance: ',game.manhattan_distance())
    print('XY distance: ',game.XY_distance())
    for i in range(5):
        game.avancer()

game.start()

#run this to collide into a wall
for i in range (4):
    game.avancer()
game.start()

#Run this to lose the game (not getting to the destination)
while game.isWall()==False:
    game.avancer()
game.droite()
for i in range (2):
    game.avancer()
game.start()

#Run this to run a red light
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
game.start()