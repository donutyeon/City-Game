from city_noEditor import startscreen,avancer,reculer,gauche,droite
import threading 
from time import sleep
global game_thread
game_thread = threading.Thread(target = startscreen)
game_thread.start()
sleep(1)
for i in range (3):
    avancer()
