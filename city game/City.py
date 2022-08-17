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
        startscreen()
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.right = wall.rect.left
  

    def gauche(self):
        sleep(0.5)
        self.rect.x -= 32
        startscreen()
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.left = wall.rect.right

    def avancer(self):
        sleep(0.5)
        self.rect.y -= 32
        startscreen()
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.top = wall.rect.bottom

    def reculer(self):
        sleep(0.5)
        self.rect.y += 32
        startscreen()
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


def startscreen():
    screen = pygame.display.set_mode((32*20, 32*15))
    screen.fill((0, 0, 0))
    pygame.display.set_caption("Atteindre l'objectif.")
    write_button = Button(0,0,pygame.image.load('write_button2.png').convert_alpha(),0.5)
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

    pygame.draw.rect(screen, (56, 103, 255), end_rect) #changed to blue just not to confuse with the red light
    pygame.draw.rect(screen, (255, 200, 0), player.rect)
    write_button.draw(screen)
    pygame.display.flip()
    clock.tick(360)

def writingscreen():
    screen = pygame.display.set_mode((500,500))
    bgc = [128, 137, 150]
    color = pygame.Color('black')
    input_box = pygame.Rect(10,10,480,480)
    font = pygame.font.Font(None, 32)
    clock = pygame.time.Clock()
    pygame.display.set_caption("text editor")
    screen.fill(bgc)
    pygame.display.flip()

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    max_width -= 7
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
 
# Set up the display
pygame.display.set_caption("Atteindre l'objectif.")
screen = pygame.display.set_mode((32*20, 32*15))
write_button = Button(0,0,pygame.image.load('write_button2.png').convert_alpha(),0.5)
run_button = Button(450,450,pygame.image.load('run_button.png').convert_alpha(),1)
clock = pygame.time.Clock()
walls = [] # List to hold the walls
lights = [] # List to hold the lights
player = Car((255, 0, 0),32,32) # Create the player
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

running = True

while running:
    startscreen()
    clock.tick(60)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
            running = False
        if write_button.draw(screen):
            writing= True
            print("game button")
            screen = pygame.display.set_mode((500,500))
            bgc = [128, 137, 150]
            color = pygame.Color('black')
            input_box = pygame.Rect(10,10,480,480)
            font = pygame.font.Font(None, 32)
            clock = pygame.time.Clock()
            pygame.display.set_caption("text editor")
            screen.fill(bgc)
            pygame.display.flip()
            text = ''
            while writing:
                screen.fill(bgc)
                run_button.draw(screen)
                for event in pygame.event.get():
                    if run_button.draw(screen):
                        try:
                            compile(text+' ', 'test', 'exec')
                        except Exception as e:
                            print ("Problem: %s" % e)
                        else:
                            writing=False 
                            startscreen()
                            exec(compile(text +' ', 'test', 'exec'))
                    if event.type == pygame.QUIT:
                        writing=False
                        running = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            text += '\n'
                        elif event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        elif event.key == pygame.K_TAB:
                            text += '    '
                        else:
                            text += event.unicode
                    # Render the current text.
                txt_surface = font.render(text, True, color)
                # text_rect = txt_surface.get_rect()
                # Resize the box if the text is too long.

                # width = max(200, txt_surface.get_width()+10)
                # input_box.w = width
                # Blit the text.
                blit_text(screen, text,(input_box.x+5, input_box.y+5), font)
                #screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
                # Blit the input_box rect.
                pygame.draw.rect(screen, color, input_box, 2)
                pygame.display.flip()
 
    # Just added this to make it slightly fun ;)
    if player.rect.colliderect(end_rect):
        pygame.quit()
        sys.exit()
 
    clock.tick(360)
 
pygame.quit()
