import pygame 
from sys import exit
import math as m

#Declaring Constants 

SCREEN_COLOR ="#171717"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
LINE_COLOR = "#A9DDD6"
LINE_THICKNESS = 2
FACE_COLOR = "#DDDDDD"
A = SCREEN_WIDTH/SCREEN_HEIGHT
FOV = 90.0 # in Degrees
Zn = 0.1
Zf = 1000.0
P = 1/m.tan(m.radians(FOV)/2)
T = Zf/(Zf-Zn)

#Declaring Variables

theta1,theta2 = 0,0

# Defining Matrices

Mat_Proj = [P/A,0,0,0
            ,0,P,0,0
            ,0,0,T,-Zf*T
            ,0,0,1,0 ]


# Defining Functions and Objects

class Vector():
    def __init__(self,x,y,z) -> None:
        self.x = float(x) 
        self.y = float(y) 
        self.z = float(z)

class Triangle():
    def __init__(self,vectors) -> None:

        self.v = list(vectors)

class Object_3D():
    def __init__(self,triangles) -> None:
        self.triangles = triangles

def MatVectorMul(i,m,o) -> None:# i is input vector , m is 4x4 matrix to be multiplied , o is the output vector
    
    o.x = i.x * m[0] + i.y * m[1] + i.z * m[2] + m[3]
    o.y = i.x * m[4] + i.y * m[5] + i.z * m[6] + m[7]
    o.z = i.x * m[8] + i.y * m[9] + i.z * m[10] + m[11]
    w = float(i.x * m[12] + i.y * m[13] + i.z * m[14] + m[15])
    
    if w != 0:
        o.x /= w ; o.y /= w ; o.z /= w

# Setting up the Pygame Window/Screen

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("3D Engine")
clock=pygame.time.Clock()

# Engine Update Loop

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
                pass
                

    # Loading Object Data

    tri1 = Triangle((Vector(0,0,0),Vector(0,1,0),Vector(1,1,0)))
    tri2 = Triangle((Vector(0,0,0),Vector(1,1,0),Vector(1,0,0)))
    tri3 = Triangle((Vector(1,0,0),Vector(1,1,0),Vector(1,1,1)))
    tri4 = Triangle((Vector(1,0,0),Vector(1,1,1),Vector(1,0,1)))
    tri5 = Triangle((Vector(1,0,1),Vector(1,1,1),Vector(0,1,1)))
    tri6 = Triangle((Vector(1,0,1),Vector(0,1,1),Vector(0,0,1)))
    tri7 = Triangle((Vector(0,0,1),Vector(0,1,1),Vector(0,1,0)))
    tri8 = Triangle((Vector(0,0,1),Vector(0,1,0),Vector(0,0,0)))
    tri9 = Triangle((Vector(0,1,0),Vector(0,1,1),Vector(1,1,1)))
    tri10 = Triangle((Vector(0,1,0),Vector(1,1,1),Vector(1,1,0)))
    tri11 = Triangle((Vector(1,0,1),Vector(0,0,1),Vector(0,0,0)))
    tri12 = Triangle((Vector(1,0,1),Vector(0,0,0),Vector(1,0,0)))

    Cube_3D = Object_3D((tri1,tri2,tri3,tri4,tri5,tri6,tri7,tri8,tri9,tri10,tri11,tri12))

    # Updating Rotation Matrices

    theta1 += 0.03  
    theta2 += 0.01

    Mat_X_Rot = [1,0,0,0
            ,0,m.cos(theta1),-m.sin(theta1),0
            ,0,m.sin(theta1),m.cos(theta1),0
            ,0,0,0,1 ]

    Mat_Y_Rot = [
                m.cos(theta2),0,m.sin(theta2),0
                ,0,1,0,0
                ,-m.sin(theta2),0,m.cos(theta2),0
                ,0,0,0,1 ]
        
    Mat_Z_Rot = [m.cos(theta2),-m.sin(theta2),0,0
                ,m.sin(theta2),m.cos(theta2),0,0
                ,0,0,1,0
                ,0,0,0,1 ]
        
    # Applying Transformations

    screen.fill(SCREEN_COLOR) # Reset Screen

    for tri in Cube_3D.triangles:
        
        # Creating Triangle objects
        Projected_tri = Triangle((Vector(1,0,0),Vector(0,1,0),Vector(0,0,1)))
        X_Rotated_tri = Triangle((Vector(1,0,0),Vector(0,1,0),Vector(0,0,1)))
        ZX_Rotated_tri = Triangle((Vector(1,0,0),Vector(0,1,0),Vector(0,0,1)))
        YZX_Rotated_tri = Triangle((Vector(1,0,0),Vector(0,1,0),Vector(0,0,1)))
        
        # Appling multiplications for rotation
        MatVectorMul(tri.v[0],Mat_Z_Rot,X_Rotated_tri.v[0])
        MatVectorMul(tri.v[1],Mat_Z_Rot,X_Rotated_tri.v[1])
        MatVectorMul(tri.v[2],Mat_Z_Rot,X_Rotated_tri.v[2])

        MatVectorMul(X_Rotated_tri.v[0],Mat_X_Rot,ZX_Rotated_tri.v[0])
        MatVectorMul(X_Rotated_tri.v[1],Mat_X_Rot,ZX_Rotated_tri.v[1])
        MatVectorMul(X_Rotated_tri.v[2],Mat_X_Rot,ZX_Rotated_tri.v[2])

        MatVectorMul(ZX_Rotated_tri.v[0],Mat_Y_Rot,YZX_Rotated_tri.v[0])
        MatVectorMul(ZX_Rotated_tri.v[1],Mat_Y_Rot,YZX_Rotated_tri.v[1])
        MatVectorMul(ZX_Rotated_tri.v[2],Mat_Y_Rot,YZX_Rotated_tri.v[2])

        Translated_tri = YZX_Rotated_tri

        #Translating Triangles along the Z-axis
        Translated_tri.v[0].z += 3.0
        Translated_tri.v[1].z += 3.0
        Translated_tri.v[2].z += 3.0

        #Projecting the Triangles
        MatVectorMul(Translated_tri.v[0],Mat_Proj,Projected_tri.v[0])
        MatVectorMul(Translated_tri.v[1],Mat_Proj,Projected_tri.v[1])
        MatVectorMul(Translated_tri.v[2],Mat_Proj,Projected_tri.v[2])

        #Scaling the triangles
        Projected_tri.v[0].x += 1.0
        Projected_tri.v[0].y += 1.0
        Projected_tri.v[1].x += 1.0
        Projected_tri.v[1].y += 1.0
        Projected_tri.v[2].x += 1.0
        Projected_tri.v[2].y += 1.0

        Projected_tri.v[0].x *= 0.5 * SCREEN_HEIGHT
        Projected_tri.v[0].y *= 0.5 * SCREEN_WIDTH
        Projected_tri.v[1].x *= 0.5 * SCREEN_HEIGHT
        Projected_tri.v[1].y *= 0.5 * SCREEN_WIDTH
        Projected_tri.v[2].x *= 0.5 * SCREEN_HEIGHT
        Projected_tri.v[2].y *= 0.5 * SCREEN_WIDTH

        #Drawing the Triangles on the Screen
        
        # pygame.draw.polygon(screen,FACE_COLOR,
        #                     ((Projected_tri.v[0].x,Projected_tri.v[0].y),
        #                         (Projected_tri.v[1].x,Projected_tri.v[1].y),
        #                         (Projected_tri.v[2].x,Projected_tri.v[2].y)))
                  
        pygame.draw.polygon(screen,LINE_COLOR,
                            ((Projected_tri.v[0].x,Projected_tri.v[0].y),
                                (Projected_tri.v[1].x,Projected_tri.v[1].y),
                                (Projected_tri.v[2].x,Projected_tri.v[2].y)),LINE_THICKNESS)
        
    pygame.display.update()
    
    # Setting Max FPS
    clock.tick(60)