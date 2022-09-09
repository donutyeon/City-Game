from dis import Instruction
import os
import sys
import pygame
from time import sleep
import threading
WHITE = (255, 255, 255)

class Car(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height, lock):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.image.load("car_up.png")
        #self.image.fill(WHITE)
        #self.image.set_colorkey(WHITE)

        #Initialise attributes of the car.
        self.width=width
        self.height=height
        self.color = color
        self.lock=lock
        # Draw the car (a rectangle!)
        #pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])

        # Instead we could load a proper picture of a car...
        # self.image = pygame.image.load("car.png").convert_alpha()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
    
    def set_walls_lights(self,walls,lights):
        self.walls=walls
        self.lights=lights
######################################### i imagine we should add the same thing as wall colliding for the traffic lights
    
    def droite(self):
        self.image = pygame.image.load("car_right.png")
        sleep(0.5)
        with self.lock:
            self.rect.x += 32
            pygame.display.update()
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                self.rect.right = wall.rect.left
                print("collided with a wall.")
        for light in self.lights:
            if (self.rect.colliderect(light.rect) and light.color == "RED"):
                self.rect.right = light.rect.left
                print("cannot run a red light.")

  

    def gauche(self):
        self.image = pygame.image.load("car_left.png")
        sleep(0.5)
        with self.lock:
            self.rect.x -= 32
            pygame.display.update()
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                self.rect.left = wall.rect.right
                print("collided with a wall.")
        for light in self.lights:
            if (self.rect.colliderect(light.rect) and light.color == "RED"):
                self.rect.left = light.rect.right
                print("cannot run a red light.")

    def avancer(self):
        self.image = pygame.image.load("car_up.png")
        sleep(0.5)
        with self.lock:
            self.rect.y -= 32
            pygame.display.update()
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                self.rect.top = wall.rect.bottom
                print("collided with a wall.")
        for light in self.lights:
            if (self.rect.colliderect(light.rect) and light.color == "RED"):
                self.rect.top = light.rect.bottom
                print("cannot run a red light.")

    def reculer(self):
        self.image = pygame.image.load("car_down.png")
        sleep(0.5)
        with self.lock:
            self.rect.y += 32
            pygame.display.update()
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                self.rect.bottom = wall.rect.top
                print("collided with a wall.")
        for light in self.lights:
            if (self.rect.colliderect(light.rect) and light.color == "RED"):
                self.rect.bottom = light.rect.top
                print("cannot run a red light.")


# Nice class to hold a wall rect
class Wall(object):
    
    def __init__(self, pos,walls):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

class TrafficLight(object):
    
    def __init__(self, pos,lights, color="RED"):
        lights.append(self)
        self.color = color
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

class city_logic:

    def __init__(self):
        self.instructions=[]
        self.lock = threading.Lock()
        self.player = Car((255, 0, 0),32,32,self.lock) # Create the player


    def _loop(self):
        sleep(0.5)
        while True:
            sleep(0.01)
            if len(self.instructions) > 0:
                with self.lock:
                    inst=self.instructions.pop(0)
                print(inst)
                exec(inst)

    def start_loop(self):
        # We spawn a new thread using our _loop method, the loop has no additional arguments,
        # We call daemon=True so that the thread dies when main dies
        threading.Thread(target=self._loop,args=(),daemon=True).start()

class city_game:
    def __init__(self):
        self.arrive=False
        self.screen = pygame.display.set_mode((32*20, 32*15))
        self.screen.fill((0, 0, 0))
        self.logic= city_logic()        
        self.walls = [] # List to hold the walls
        self.lights = [] # List to hold the lights
        # Set up the display
        pygame.display.set_caption("Atteindre l'objectif.")
        self.clock = pygame.time.Clock()
        level = [
            "WWWWWWWWWWWWWWWWWWWW",
            "W WWW WWW WW WW WW W",
            "W WWW WWW    WW WW W",
            "W    E             W",
            "W WWW WWW WWW WWW WW",
            "W WWW WWW WWW WWW WW",
            "W WWW WWW     WWW  W",
            "W     R            W",
            "W WWW WWW WW WW WW W",
            "W WWW WWW WW WW WW W",
            "W                  W",
            "W WWW WWW WW WWW WWW",
            "W         WW WWW WWW",
            "W               P  W",
            "WWWWWWWWWWWWWWWWWWWW",
        ]
        ##################################### add an R for red light
        # Parse the level string above. W = wall, E = exit
        x = y = 0
        for row in level:
            for col in row:
                if col == "W":
                    Wall((x, y), self.walls)
                if col == "E":
                    self.end_rect = pygame.Rect(x, y, 32, 32)
                if col == "P":
                    self.logic.player.rect.x = x
                    self.logic.player.rect.y = y
                if col == "R":
                    TrafficLight((x, y),self.lights ,"RED")
                x += 32
            y += 32
            x = 0
        self.logic.player.set_walls_lights(self.walls,self.lights)
        pygame.init()
        self.window=pygame.display.set_mode((32*20, 32*15))
        self.running=True

    def avancer(self):
        self.logic.instructions.append("self.player.avancer()")
    def reculer(self):
        self.logic.instructions.append("self.player.reculer()")
    def gauche(self):
        self.logic.instructions.append("self.player.gauche()")
    def droite(self):
        self.logic.instructions.append("self.player.droite()")

    def start(self):
        pygame.display.update()
        self.logic.start_loop()
        while self.running:
            for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        self.running = False
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                        self.running = False
            with self.logic.lock:
                self.window.fill((0, 0, 0))
                for wall in self.walls:
                    pygame.draw.rect(self.screen, (255, 255, 255), wall.rect)
                for light in self.lights:
                    if light.color == "RED":
                        pygame.draw.rect(self.screen, (252, 50, 10), light.rect)
                    elif light.color == "GREEN":
                        pygame.draw.rect(self.screen, (93, 255, 61), light.rect)
                    elif light.color == "YELLOW":
                        pygame.draw.rect(self.screen, (255, 197, 61), light.rect)
                pygame.display.update()
                pygame.draw.rect(self.screen, (56, 103, 255), self.end_rect) #changed to blue just not to confuse with the red light
                self.screen.blit(self.logic.player.image,self.logic.player.rect)
                pygame.display.flip()
                self.clock.tick(60)
            if self.logic.player.rect.colliderect(self.end_rect):
                self.arrive=True
                print("you won !")
                pygame.quit()
                sys.exit()
            if ( len(self.logic.instructions) == 0 and  self.arrive == False ):
                print("game over, you did not arrive to your destination.")
                pygame.quit()
                sys.exit()
        
if __name__ == '__main__':
    game = city_game()
    game.start()
        