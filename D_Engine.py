import pygame 
from sys import exit
import math as m

SCREEN_COLOR ="#171717"
SCREEN_SIZE = (1080,720)
LINE_COLOR = "A9DDD6"

# Defining Functions and Objects
A = SCREEN_SIZE[0]/SCREEN_SIZE[1]
FOV = 90.0 # in Degrees
Zn = 0.1
Zf = 1000.0
P = 1/m.tan(m.radians(FOV))
T = Zf/(Zf-Zn)

Mat_Proj = [P/A,0,0,0
            ,0,P,0,0
            ,0,0,T,-Zf*T
            ,0,0,1,0 ]

class Vector():
    def __init__(self,x,y,z) -> None:
        self.x = float(x) 
        self.y = float(y) 
        self.z = float(z)

class Triangle():
    def __init__(self,vectors) -> None:
        self.v = vectors

class Object_3D():
    def __init__(self,triangles) -> None:
        self.triangles = triangles

# def Mat_mul_3D(MatA,MatB,Mat_result) -> None:

#     for i in range(0,4):
#         temp=0
#         for j in range (0,4):
#            temp += MatA[4*i+j]*MatB[j]
#         Mat_result.append(temp)

def MatVectorMul(i,m,o) -> None:# i is input vector , m is 4x4 matrix to be multiplied , o is the output vector
    
    o.x = i.x * m[0] + i.y * m[1] + i.z * m[2] + m[3]
    o.y = i.x * m[4] + i.y * m[5] + i.z * m[6] + m[7]
    o.z = i.x * m[8] + i.y * m[9] + i.z * m[10] + m[11]
    w = float(i.x * m[12] + i.y * m[13] + i.z * m[14] + m[15])
    
    if w != 0:
        o.x /= w ; o.y /= w ; o.z /= w

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # print(matR)
                pass

    # Load Object Data
        vec1 = Vector(0,0,0)
        vec2 = Vector(0,0,1)
        vec3 = Vector(0,1,0)

        tri1 = Triangle((vec1,vec2,vec3))
        tri2 = Triangle((vec3,vec2,vec1))
        
        some_object = Object_3D((tri1,tri2))
     
    # Update Data
        screen.fill(SCREEN_COLOR) # Reset Screen

        for tri in some_object.triangles:
            Projected_tri,Translated_tri = Triangle
            MatVectorMul(tri.v[0],Projected_tri.v[0],Mat_Proj)
            MatVectorMul(tri.v[1],Projected_tri.v[1],Mat_Proj)
            MatVectorMul(tri.v[2],Projected_tri.v[2],Mat_Proj)


    pygame.display.update()
    # Setting Max FPS
    clock.tick(60)