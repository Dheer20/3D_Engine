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
ROTATION_SPEED = 0.0  # Radians per second
CAMERA_VELOCITY_Y = 0
CAMERA_VELOCITY_X = 0
MAX_VELOCITY = 20.0
CAMERA_ACCELERATION = 10
CAMERA_FRICTION = 0.95

#Declaring Variables
theta1,theta2 = 0,0
wire_render = False

# Creating Matrices
Proj_Mat=Matrix_3D
Proj_Mat=Matrix_3D.Projection(A=SCREEN_WIDTH/SCREEN_HEIGHT,FOV=45.0,Zn=0.01,Zf=1000.0)

# Defining Characteristic Vectors
camera_3D = Vector(0,0,0)
light_dir = Vector(0,0,-1)
light_dir.Normalize()

# Setting up the Pygame Window/Screen
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("3D Engine")
clock=pygame.time.Clock()

# Loading Object Data

Monkey = Mesh_3D.LoadObjFile("objects/monkey.obj")

# Engine Update Loop
while True:

    keys = pygame.key.get_pressed()
    elapsed_time = clock.get_time() / 1000.0 # Convert milliseconds to seconds

    # Apply acceleration based on key presses
    if keys[pygame.K_DOWN]:
        CAMERA_VELOCITY_Y -= CAMERA_ACCELERATION * elapsed_time
    if keys[pygame.K_UP]:
        CAMERA_VELOCITY_Y += CAMERA_ACCELERATION * elapsed_time
    if keys[pygame.K_LEFT]:
        CAMERA_VELOCITY_X += CAMERA_ACCELERATION * elapsed_time
    if keys[pygame.K_RIGHT]:
        CAMERA_VELOCITY_X -= CAMERA_ACCELERATION * elapsed_time
    

    # Apply velocity to camera position
    camera_3D.y += CAMERA_VELOCITY_Y * elapsed_time
    camera_3D.x += CAMERA_VELOCITY_X * elapsed_time

    # Apply friction to slow down the camera when no keys are pressed
    CAMERA_VELOCITY_Y *= CAMERA_FRICTION
    CAMERA_VELOCITY_X *= CAMERA_FRICTION

    # Optional: Clamp velocity to prevent excessive speed
    CAMERA_VELOCITY_Y = max(min(CAMERA_VELOCITY_Y, MAX_VELOCITY), -MAX_VELOCITY)
    CAMERA_VELOCITY_X = max(min(CAMERA_VELOCITY_X, MAX_VELOCITY), -MAX_VELOCITY)

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
                camera_3D = Vector(0,0,0)
                CAMERA_VELOCITY_Y = 0
                CAMERA_VELOCITY_X = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LSHIFT:
                wire_render = not wire_render

                
                
    # Updating Rotation and Translation Matrices

    # Calculate the rotation angle for this frame
    rotation_angle = ROTATION_SPEED * elapsed_time
    
    X_Rot_Mat = Matrix_3D.X_Rotation(theta1)
    Y_Rot_Mat = Matrix_3D.Y_Rotation(theta1)
    Z_Rot_Mat = Matrix_3D.Z_Rotation(theta1)
    Translation_Z_Mat = Matrix_3D.Translation(Z=8.0)

    # Update theta1 for the next frame
    theta1 += rotation_angle

    look_dir = Vector(0,0,1)
    up = Vector(0,1,0)
    target = camera_3D + look_dir

    View_Mat = Matrix_3D.View_for_CameraPointAt(camera_3D,target,up)

    # Applying Transformations
    TriangleToRasterList=[]

    screen.fill(SCREEN_COLOR) # Reset Screen

    for tri in Monkey.triangles:
        
        World_Mat = Matrix_3D.Identity()
        
        World_Mat = Translation_Z_Mat @ Z_Rot_Mat @ Y_Rot_Mat @ X_Rot_Mat

        Translated_tri = Matrix_3D.MatTriMul(tri,World_Mat)

        # Calculating Normals
        line1 = Vector.TwoPoint(Translated_tri.v1,Translated_tri.v0)

        line2 = Vector.TwoPoint(Translated_tri.v2,Translated_tri.v0)

        normal = line1 @ line2

        normal.Normalize()
        
        #Calculating Culling conditon
        view_direction = Translated_tri.v0 - camera_3D

        dot_product = normal ** view_direction

        if dot_product < 0.0:  #backface culling condition

            #Lighting
            Illumination_dp = normal ** light_dir
            if Illumination_dp < 0 : Illumination_dp = 0
            Translated_tri.GetColor(Illumination_dp)

            View_tri = Matrix_3D.MatTriMul(Translated_tri,View_Mat)

            #Projecting the Triangles
            Projected_tri = Matrix_3D.MatTriMul(View_tri,Proj_Mat)
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
    
    TriangleToRasterList.sort(key=lambda tri: tri.order)
    
    for tri in TriangleToRasterList:
        #Drawing the Triangles on the Screen
        if wire_render == False:
            pygame.draw.polygon(screen,tri.color,
                                ((tri.v0.x,tri.v0.y),
                                (tri.v1.x,tri.v1.y),
                                (tri.v2.x,tri.v2.y)))
        else:
            pygame.draw.polygon(screen,LINE_COLOR,
                                ((tri.v0.x,tri.v0.y),
                                (tri.v1.x,tri.v1.y),
                                (tri.v2.x,tri.v2.y)),LINE_THICKNESS)

    pygame.display.update()
    
    # Setting Max FPS
    clock.tick(60)