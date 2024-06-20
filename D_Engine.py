import pygame  # type: ignore
from sys import exit
import math as m
from Geometry import *

#Declaring Constants 
SCREEN_COLOR = "#171717"
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
LINE_COLOR = "#A9DDD6"
LINE_THICKNESS = 1

#Declaring Variables
theta1,theta2 = 0,0

# Creating Matrices
Mat_Proj=Matrix_3D
Mat_Proj=Matrix_3D.Projection(A=SCREEN_WIDTH/SCREEN_HEIGHT,FOV=120.0,Zn=0.01,Zf=1000.0)

# Defining Characteristic Vectors
Camera_3D = Vector(0,0,0)
Light_dir = Vector(0,0,-1)
Light_dir.Normalize()

# Setting up the Pygame Window/Screen
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("3D Engine")
clock=pygame.time.Clock()

# Loading Object Data

Monkey = Mesh_3D.LoadObjFile("monkey.obj")

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
                
    # Updating Rotation Matrices

    theta1 += 0.03  
    theta2 += 0.01
    
    Mat_X_Rot = Matrix_3D.X_Rotation(theta1)
    Mat_Y_Rot = Matrix_3D.Y_Rotation(theta2)
    Mat_Z_Rot = Matrix_3D.Z_Rotation(theta1)

    # Applying Transformations
    TriangleToRasterList=[]

    screen.fill(SCREEN_COLOR) # Reset Screen

    for tri in Monkey.triangles:
        
        # Creating Triangle objects
        # Projected_tri = Triangle()
        # X_Rotated_tri = Triangle()
        # ZX_Rotated_tri = Triangle()
        # YZX_Rotated_tri = Triangle()
        
        # Appling multiplications for rotation
        # Rotate in X-axis
        X_Rotated_tri=Matrix_3D.MatTriMul(tri,Mat_X_Rot)

        # Rotate in Z-axis
        ZX_Rotated_tri=Matrix_3D.MatTriMul(X_Rotated_tri,Mat_Z_Rot)

        # Rotate in Y-axis
        YZX_Rotated_tri=Matrix_3D.MatTriMul(ZX_Rotated_tri,Mat_Y_Rot)

        #Translating Triangles along the Z-axis
        Translated_tri = YZX_Rotated_tri
        Translated_tri.v0.z += 2.0
        Translated_tri.v1.z += 2.0
        Translated_tri.v2.z += 2.0

        # Calculating Normals
        line1 = Vector(Translated_tri.v1.x - Translated_tri.v0.x, 
                       Translated_tri.v1.y - Translated_tri.v0.y, 
                       Translated_tri.v1.z - Translated_tri.v0.z)

        line2 = Vector(Translated_tri.v2.x - Translated_tri.v0.x, 
                       Translated_tri.v2.y - Translated_tri.v0.y, 
                       Translated_tri.v2.z - Translated_tri.v0.z)

        normal = line1 @ line2

        normal.Normalize()
        
        #Calculating Culling conditon
        view_direction = Vector(Translated_tri.v0.x - Camera_3D.x,
                        Translated_tri.v0.y - Camera_3D.y,
                        Translated_tri.v0.z - Camera_3D.z)

        dot_product = normal ** view_direction

        if dot_product < 0.0:  #backface culling condition

            #Lighting
            Illumination_dp = normal.x * Light_dir.x + normal.y * Light_dir.y + normal.z * Light_dir.z
            if Illumination_dp < 0 : Illumination_dp = 0
            Translated_tri.GetColor(Illumination_dp)

            #Projecting the Triangles
            Projected_tri = Matrix_3D.MatTriMul(Translated_tri,Mat_Proj)
            Projected_tri.color = Translated_tri.color

            #Scaling the triangles
            Projected_tri.v0.x += 1.0
            Projected_tri.v0.y += 1.0
            Projected_tri.v1.x += 1.0
            Projected_tri.v1.y += 1.0
            Projected_tri.v2.x += 1.0
            Projected_tri.v2.y += 1.0

            Projected_tri.v0.x *= 0.5 * SCREEN_HEIGHT
            Projected_tri.v0.y *= 0.5 * SCREEN_WIDTH
            Projected_tri.v1.x *= 0.5 * SCREEN_HEIGHT
            Projected_tri.v1.y *= 0.5 * SCREEN_WIDTH
            Projected_tri.v2.x *= 0.5 * SCREEN_HEIGHT
            Projected_tri.v2.y *= 0.5 * SCREEN_WIDTH

            TriangleToRasterList.append(Projected_tri)
        
    for tri in TriangleToRasterList:
        tri.order = (tri.v0.z + tri.v1.z +tri.v2.z)/3
    
    TriangleToRasterList.sort(key=lambda tri: tri.order, reverse=True)
    
    for tri in TriangleToRasterList:
        #Drawing the Triangles on the Screen
        pygame.draw.polygon(screen,tri.color,
                            ((tri.v0.x,tri.v0.y),
                            (tri.v1.x,tri.v1.y),
                            (tri.v2.x,tri.v2.y)))

    pygame.display.update()
    
    # Setting Max FPS
    clock.tick(60)