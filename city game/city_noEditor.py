from time import sleep
import pygame
import os
import sys
from Button import Button
WHITE = (255, 255, 255)

class Car(pygame.sprite.Sprite):
    #This class represents a car. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(WHITE)
        self.image.set_colorkey(WHITE)

        #Initialise attributes of the car.
        self.width=width
        self.height=height
        self.color = color

        # Draw the car (a rectangle!)
        pygame.draw.rect(self.image, self.color, [0, 0, self.width, self.height])

        # Instead we could load a proper picture of a car...
        # self.image = pygame.image.load("car.png").convert_alpha()

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

######################################### i imagine we should add the same thing as wall colliding for the traffic lights
    
    def droite(self):
        sleep(0.5)
        self.rect.x += 32
        pygame.display.update()
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.right = wall.rect.left
  

    def gauche(self):
        sleep(0.5)
        self.rect.x -= 32
        pygame.display.update()
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.left = wall.rect.right

    def avancer(self):
        sleep(0.5)
        self.rect.y -= 32
        pygame.display.update()
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.top = wall.rect.bottom

    def reculer(self):
        sleep(0.5)
        self.rect.y += 32
        pygame.display.update()
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.bottom = wall.rect.top


# Nice class to hold a wall rect
class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

class TrafficLight(object):
    
    def __init__(self, pos, color="RED"):
        lights.append(self)
        self.color = color
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

instructions=[]
walls = [] # List to hold the walls
lights = [] # List to hold the lights
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
screen = pygame.display.set_mode((32*20, 32*15))
screen.fill((0, 0, 0))
player = Car((255, 0, 0),32,32) # Create the player
# Set up the display
pygame.display.set_caption("Atteindre l'objectif.")
clock = pygame.time.Clock()
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
            Wall((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, 32, 32)
        if col == "P":
            player.rect.x = x
            player.rect.y = y
        if col == "R":
            TrafficLight((x, y), "GREEN")
        x += 32
    y += 32
    x = 0

def avancer():
    instructions.append("player.avancer()")
def reculer():
    instructions.append("player.reculer()")
def gauche():
    instructions.append("player.gauche()")
def droite():
    instructions.append("player.droite()")

def refresh():
    screen = pygame.display.set_mode((32*20, 32*15))
    screen.fill((0, 0, 0))
    pygame.display.set_caption("Atteindre l'objectif.")
    clock = pygame.time.Clock()
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    for light in lights:
            if light.color == "RED":
                pygame.draw.rect(screen, (252, 50, 10), light.rect)
            elif light.color == "GREEN":
                pygame.draw.rect(screen, (93, 255, 61), light.rect)
            elif light.color == "YELLOW":
                pygame.draw.rect(screen, (255, 197, 61), light.rect)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    pygame.display.flip()
    clock.tick(360)

def startscreen():    
    # Set up the display
    pygame.display.set_caption("Atteindre l'objectif.")
    clock = pygame.time.Clock()
    refresh()
    running = True
    while running:
        refresh()
        clock.tick(360)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                running = False
    
        # Just added this to make it slightly fun ;)
        if player.rect.colliderect(end_rect):
            pygame.quit()
            sys.exit()
    
        # Draw the scene
        screen.fill((0, 0, 0))
        for wall in walls:
            pygame.draw.rect(screen, (255, 255, 255), wall.rect)
        for light in lights:
            if light.color == "RED":
                pygame.draw.rect(screen, (252, 50, 10), light.rect)
            elif light.color == "GREEN":
                pygame.draw.rect(screen, (93, 255, 61), light.rect)
            elif light.color == "YELLOW":
                pygame.draw.rect(screen, (255, 197, 61), light.rect)

        pygame.draw.rect(screen, (56, 103, 255), end_rect) #changed to blue just not to confuse with the red light
        pygame.draw.rect(screen, (255, 200, 0), player.rect)

        while len(instructions)>0:
            inst=instructions.pop(0)
            print(inst)
            exec(inst)
            
        pygame.display.flip()
        clock.tick(360)
 
    pygame.quit()
