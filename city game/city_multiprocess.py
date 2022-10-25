import os
import sys
import pygame
from time import sleep
import threading
WHITE = (255, 255, 255)
import ctypes
import random
buildings=[pygame.image.load("game_sprites\_building1.png"),pygame.image.load("game_sprites\_building2.png"),pygame.image.load("game_sprites\_building3.png"),pygame.image.load("game_sprites\_building4.png")]
class Car(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height, lock):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        #Initialise attributes of the car.
        self.width=width
        self.height=height
        self.color = color
        self.lock=lock
        self.collided=False
        self.ran=False
        # Draw the car (a rectangle!)
        #pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])

        # Instead we could load a proper picture of a car...
        self.image = pygame.image.load("game_sprites\car_up.png")

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()
    
    def set_walls_lights(self,walls,lights):
        self.walls=walls
        self.lights=lights
######################################### i imagine we should add the same thing as wall colliding for the traffic lights
    ## moving functions
    def droite(self):
        #change the sprite
        self.image = pygame.image.load("game_sprites\car_right.png")
        sleep(0.5)
        with self.lock:
            self.rect.x += 32
            pygame.display.update()
        for wall in self.walls:
            #checking collision with a wall
            if self.rect.colliderect(wall.rect):
                self.rect.right = wall.rect.left
                self.image = pygame.transform.scale(pygame.image.load("game_sprites\explosion.png").convert_alpha(), (int(64 * 0.5), int(64 * 0.5)))
                self.collided=True
                ctypes.windll.user32.MessageBoxW(0, "you ran into a wall, game over.", "Game Over", 0)
        for light in self.lights:
            #checking if we ran a red light
            if (self.rect.colliderect(light.rect) and light.color == "RED"):
                self.rect.right = light.rect.left
                self.ran=True

  
    #same thing as right but with a different direction
    def gauche(self):
        self.image = pygame.image.load("game_sprites\car_left.png")
        sleep(0.5)
        with self.lock: #we change the coordinates of the player, one tile is 32x32 px, so we move by 32px in the desired direction
            self.rect.x -= 32
            pygame.display.update()
        for wall in self.walls: #we check everytime if we have collided with a wall during our move
            if self.rect.colliderect(wall.rect):
                self.rect.left = wall.rect.right
                self.image = pygame.transform.scale(pygame.image.load("game_sprites\explosion.png").convert_alpha(), (int(64 * 0.5), int(64 * 0.5)))
                self.collided=True          
                ctypes.windll.user32.MessageBoxW(0, "you ran into a wall, game over.", "Game Over", 0) #if we did collide, then it's game over
        for light in self.lights: #checking if we ran a red light
            if (self.rect.colliderect(light.rect) and light.color == "RED"): 
                self.rect.left = light.rect.right
                self.ran=True # we set the boolean to true
                
                

    def avancer(self):
        self.image = pygame.image.load("game_sprites\car_up.png")
        sleep(0.5)
        with self.lock:
            self.rect.y -= 32
            pygame.display.update()
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                self.rect.top = wall.rect.bottom
                self.image = pygame.transform.scale(pygame.image.load("game_sprites\explosion.png").convert_alpha(), (int(64 * 0.5), int(64 * 0.5)))
                self.collided=True              
                ctypes.windll.user32.MessageBoxW(0, "you ran into a wall, game over.", "Game Over", 0)
        for light in self.lights:
            if (self.rect.colliderect(light.rect) and light.color == "RED"):
                self.rect.top = light.rect.bottom
                self.ran=True

    def reculer(self):
        self.image = pygame.image.load("game_sprites\car_down.png")
        sleep(0.5)
        with self.lock:
            self.rect.y += 32
            pygame.display.update()
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                self.rect.bottom = wall.rect.top
                self.image = pygame.transform.scale(pygame.image.load("game_sprites\explosion.png").convert_alpha(), (int(64 * 0.5), int(64 * 0.5)))
                self.collided=True                
                ctypes.windll.user32.MessageBoxW(0, "you ran into a wall, game over.", "Game Over", 0)
        for light in self.lights:
            if (self.rect.colliderect(light.rect) and light.color == "RED"):
                self.rect.bottom = light.rect.top
                self.ran=True
                

## the following are objects in the game such as walls and traffic lights
# Nice class to hold a wall rect
class Wall(object):
    
    def __init__(self, pos,walls,image):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
        self.image=image

class TrafficLight(object):
    
    def __init__(self, pos,lights, color):
        lights.append(self)
        self.color = color
        self.x=int(pos[0])
        self.y=int(pos[1])
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)
        if color=="RED":
            self.image=pygame.image.load("game_sprites\lights_red.png")
        if color=="YELLOW":
            self.image=pygame.image.load("game_sprites\lights_yellow.png")
        if color=="GREEN":
            self.image=pygame.image.load("game_sprites\lights_green.png")

# the tiles is basically the floor in order to have road sprites
class Tiles(object):
    def __init__(self,pos,tiles,image):
        tiles.append(self)
        self.image=pygame.image.load(image)
        self.rect=pygame.Rect(pos[0],pos[1],32,32)

class city_logic:
    #make the game run with the instruction list and thread
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
                sleep(0.01)
                if (self.player.collided or self.player.ran):
                    self.instructions.clear()


    def start_loop(self):
        # We spawn a new thread using our _loop method, the loop has no additional arguments,
        # We call daemon=True so that the thread dies when main dies
        threading.Thread(target=self._loop,args=(),daemon=True).start()

# the actual class of the game that the user will instenciate, and will generate the city
class city_game:
    def __init__(self):
        self.arrive=False
        self.screen = pygame.display.set_mode((32*20, 32*15))
        self.screen.fill((0, 0, 0))
        self.logic= city_logic()        
        self.walls = [] # List to hold the walls
        self.lights = [] # List to hold the lights
        self.tiles=[] # list to hold the tiles
        # Set up the display
        pygame.display.set_caption("Atteindre l'objectif.")
        self.clock = pygame.time.Clock()
        level = [
            "WWWWWWWWWWWWWWWWWWWW",
            "W WWW WWW WW WW WW W",
            "W WWW WWW    WW WW W",
            "W----E-------------W",
            "W WWW WWW WWWYWWW WW",
            "W WWW WWW WWW WWW WW",
            "W WWW WWW WWW WWW WW",
            "W-----R------------W",
            "W WWW WWW WW WW WW W",
            "W WWW WWW WW WW WW W",
            "W------------------W",
            "W WWWWWWW WWGWWW WWW",
            "W         WW WWW WWW",
            "W---------------P--W",
            "WWWWWWWWWWWWWWWWWWWW",
        ]
        ##################################### add an R for red light
        # Parse the level string above. W = wall, E = exit, -=horizontal route , space=vertical route
        x = y = 0
        for row in level:
            for col in row:
                if col == "W":
                    rand=random.randint(0,3)
                    Wall((x, y), self.walls,buildings[rand])
                if col == "E":
                    self.end_rect = pygame.Rect(x, y, 32, 32)
                    self.end_image= pygame.image.load("game_sprites\end.png")
                if col == "P":
                    self.logic.player.rect.x = x
                    self.logic.player.rect.y = y
                if col == "R":
                    TrafficLight((x, y),self.lights ,"RED")
                if col == "G":
                    TrafficLight((x, y),self.lights ,"GREEN")
                if col == "Y":
                    TrafficLight((x, y),self.lights ,"YELLOW")
                if col==' ':
                    Tiles((x,y),self.tiles,"game_sprites\_route_straight.png")
                if col=='-':
                    Tiles((x,y),self.tiles,"game_sprites\_route_side.png")
                x += 32
            y += 32
            x = 0
        self.logic.player.set_walls_lights(self.walls,self.lights)
        pygame.init()
        self.window=pygame.display.set_mode((32*20, 32*15))
        self.running=True
    #this is to clean the code on the user's end, so they can just call the instance of the class and use this method directly
    #it will add the instruction to the list
    def avancer(self):
        self.logic.instructions.append("self.player.avancer()")
    def reculer(self):
        self.logic.instructions.append("self.player.reculer()")
    def gauche(self): 
        self.logic.instructions.append("self.player.gauche()")
    def droite(self):
        self.logic.instructions.append("self.player.droite()")

    #check if the player is currently on a red light
    def isRedLight(self):
        playerX=self.logic.player.rect.x
        playerY=self.logic.player.rect.y
        # in this part, in order to know whether the player reached a red light or not in the goal of checking it and returning a boolean
        # we have to virtually run all the instructions in the list, in order to perform a simulation, and get the exact coordinates of the player
        # at that given time.
        directions=self.logic.instructions.copy()
        # getting the instructions and counting the X and Y coordinates of the player
        for direct in directions:
            if direct=="self.player.avancer()":
                playerY-=32
            elif direct=="self.player.reculer()":
                playerY+=32
            elif direct=="self.player.gauche()":
                playerX-=32
            else:
                playerX+=32
        # now that we have the exact coordinates of the player in that given moment, and check if there is a red light in the same coordinates
        for light in self.lights:
            if (light.color=="RED" and ((playerX+32==light.x) or (playerX-32==light.x) or (playerY+32==light.y) or (playerY-32==light.y))):
                print ("light adjacent")
                #we can return the boolean, true if there is a red light, and false if there is not
                return True            
        return False

    def afficher(self):
        pygame.display.update()
        self.logic.start_loop()
        #starting the infinite loop
        while self.running:
            for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        self.running = False
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                        self.running = False
            #generate the game screen and city
            with self.logic.lock:
                self.window.fill((84,90,94))
                #generate the walls
                for wall in self.walls:
                    self.screen.blit(wall.image,wall.rect)
                #generate the lights (with a road sprite underneath the light using layering)
                for light in self.lights:
                    self.screen.blit(light.image,light.rect)
                #draw the road sprites
                for tile in self.tiles:
                    self.screen.blit(tile.image,tile.rect)
                #pygame.display.update()   <---- this update was causing flickering and the game runs fine/even better without
                self.screen.blit(self.end_image,self.end_rect) #goal tile
                self.screen.blit(self.logic.player.image,self.logic.player.rect)
                pygame.display.flip()
                self.clock.tick(60)
                
    # run the actual game
    def start(self):
        pygame.display.update()
        self.logic.start_loop()
        #starting the infinite loop
        while self.running:
            for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        self.running = False
                    if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                        self.running = False
            #generate the game screen and city
            with self.logic.lock:
                self.window.fill((84,90,94))
                #generate the walls
                for wall in self.walls:
                    self.screen.blit(wall.image,wall.rect)
                #generate the lights (with a road sprite underneath the light using layering)
                for light in self.lights:
                    self.screen.blit(light.image,light.rect)
                #draw the road sprites
                for tile in self.tiles:
                    self.screen.blit(tile.image,tile.rect)
                #pygame.display.update()   <---- this update was causing flickering and the game runs fine/even better without
                self.screen.blit(self.end_image,self.end_rect) #goal tile
                self.screen.blit(self.logic.player.image,self.logic.player.rect)
                pygame.display.flip()
                self.clock.tick(60)
            #check if player arrived to goal, if yes congratulate them and quit the game
            if self.logic.player.rect.colliderect(self.end_rect):
                self.arrive=True
                ctypes.windll.user32.MessageBoxW(0, "Congratulations ! you got to your destination.", "Game Won", 0)
                pygame.quit()
                sys.exit()
            #if all the instructions have been used up and didn't arrive to destinationn
            if ( len(self.logic.instructions) == 0 and  self.arrive == False ):
                sleep(0.5)
                
                if self.logic.player.collided: #check if player has collided with a wall, the message box has been coded with the collided function so there is no need to repeat it here
                    pygame.quit()
                    sys.exit()
                elif self.logic.player.ran:   #check if player ran a red light
                    ctypes.windll.user32.MessageBoxW(0, "you cannot run a red light, game over.", "Game Over", 0)
                    pygame.quit()
                    sys.exit()
                else: #if player didn't collide with anything, but still didn't reach the goal
                    ctypes.windll.user32.MessageBoxW(0, "You did not get to your destination.", "Game Over", 0)
                    pygame.quit()
                    sys.exit()
                #quit the game when there is a game over
if __name__ == '__main__':
    game = city_game()
    game.start()
        