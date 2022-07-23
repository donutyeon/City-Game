import pygame
import os
import sys
import random
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
    
    def moveRight(self, pixels):
        self.rect.x += pixels
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if pixels > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if pixels < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right

    def moveLeft(self, pixels):
        pixels=-pixels
        self.rect.x += pixels
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if pixels > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                if pixels < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right

    def moveForward(self, pixels):
        pixels=-pixels
        self.rect.y += pixels
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if pixels > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if pixels < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom

    def moveBackward(self, pixels):
        self.rect.y += pixels
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if pixels > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                if pixels < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom


# Nice class to hold a wall rect
class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
 
# Set up the display
pygame.display.set_caption("Atteindre l'objectif.")
screen = pygame.display.set_mode((320, 240))
 
clock = pygame.time.Clock()
walls = [] # List to hold the walls
player = Car((255, 0, 0),16,16) # Create the player
level = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W WWW WWW WW WW WW W",
    "W WWW WWW    WW WW W",
    "W    E             W",
    "W WWW WWW WWW WWW WW",
    "W WWW WWW WWW WWW WW",
    "W WWW WWW     WWW  W",
    "W                  W",
    "W WWW WWW WW WW WW W",
    "W WWW WWW WW WW WW W",
    "W                  W",
    "W WWW WWW WW WWW WWW",
    "W         WW WWW WWW",
    "W               P  W",
    "WWWWWWWWWWWWWWWWWWWW",
]

# Parse the level string above. W = wall, E = exit
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            end_rect = pygame.Rect(x, y, 16, 16)
        if col == "P":
            player.rect.x = x
            player.rect.y = y
        x += 16
    y += 16
    x = 0

running = True
while running:
    
    clock.tick(60)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
 
    # Move the player if an arrow key is pressed
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT]:
        player.moveLeft(16)
    if key[pygame.K_RIGHT]:
        player.moveRight(16)
    if key[pygame.K_UP]:
        player.moveForward(16)
    if key[pygame.K_DOWN]:
        player.moveBackward(16)
 
    # Just added this to make it slightly fun ;)
    if player.rect.colliderect(end_rect):
        pygame.quit()
        sys.exit()
 
    # Draw the scene
    screen.fill((0, 0, 0))
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
    pygame.draw.rect(screen, (255, 0, 0), end_rect)
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,0))
    pygame.display.flip()
    clock.tick(360)
 
pygame.quit()