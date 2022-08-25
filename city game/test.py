from city_multiprocess import city_game
import threading 
game=city_game()
threading.Thread(target=city_game,args=(),daemon=True).start()
for i in range (3):
    game.avancer()
