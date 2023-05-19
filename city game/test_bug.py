from city_lab import city_game
game=city_game(1)

#Distance at the start of the game
print('Euclidean distance: ',game.euclidean_distance())
print('Manhattan distance: ',game.manhattan_distance())
print('XY distance: ',game.XY_distance())
game.avancer()
game.afficher()
