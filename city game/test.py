# from noeditor_city_yasmine import startscreen,avancer,reculer,gauche,droite, init, refresh, thread_test, fresh_start
# import threading 
# from time import sleep
# init()
# # refresh()
# global game_thread
# game_thread = threading.Thread(target = refresh)
# game_thread.start()
# # sleep(1)
# # for i in range (3):
# #     avancer()

from concurrent.futures import thread
from noeditor_city_yasmine import city_game
import threading
from multiprocessing import Process
from time import sleep

mygame = city_game()
game_thread = Process(target = mygame.ville)
game_thread.start()

print("we are past the thread")
# sleep(1)
# for i in range (3):
#     mygame.avancer()
mygame.see_instructions()
