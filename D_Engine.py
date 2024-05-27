import pygame 
from sys import exit

SCREEN_COLOR ="#171717"
SCREEN_SIZE = (1080,720)
LINE_COLOR = "A9DDD6"

# Defining Functions and Objects

class Vector():
    def __init__(self,x,y,z) -> None:
        self.x = x 
        self.y = y 
        self.z = z
        self.w = 1

class Triangle():
    def __init__(self,v1,v2,v3) -> None:
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3

class Object_3D():
    def __init__(self,triangles) -> None:
        self.triangles = triangles


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("3D Engine")
clock=pygame.time.Clock()

# Game Update Loop
while True:

    # Checking events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit() 
                exit()

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_SPACE:
        #         print([tri1.v1])


    # Update Data
        vec1 = Vector(0,0,0)
        vec2 = Vector(0,0,1)
        vec3 = Vector(0,1,0)

        tri1 = Triangle(vec1,vec2,vec3)
        tri2 = Triangle(vec3,vec2,vec1)
        
        some_object = Object_3D(tri1,tri2)
        screen.fill(SCREEN_COLOR) # Reset Screen
         
        
         



    pygame.display.update()
    # Setting Max FPS
    clock.tick(60)