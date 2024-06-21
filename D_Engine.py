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

# camera_speed = 1  # Smaller value for smoother movement
# camera_velocity = 0.0

camera_velocity_y = 0
camera_velocity_x = 0
camera_acceleration = 10
camera_friction = 0.95
#Declaring Variables
theta1,theta2 = 0,0

# Creating Matrices
Mat_Proj=Matrix_3D
Mat_Proj=Matrix_3D.Projection(A=SCREEN_WIDTH/SCREEN_HEIGHT,FOV=45.0,Zn=0.01,Zf=1000.0)

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

Monkey = Mesh_3D.LoadObjFile("monkey.obj")

# Engine Update Loop
while True:

    keys = pygame.key.get_pressed()
    elapsed_time = clock.get_time() / 1000.0

    # Apply acceleration based on key presses
    if keys[pygame.K_DOWN]:
        camera_velocity_y -= camera_acceleration * elapsed_time
    if keys[pygame.K_UP]:
        camera_velocity_y += camera_acceleration * elapsed_time
    if keys[pygame.K_LEFT]:
        camera_velocity_x += camera_acceleration * elapsed_time
    if keys[pygame.K_RIGHT]:
        camera_velocity_x -= camera_acceleration * elapsed_time
    

    # Apply velocity to camera position
    camera_3D.y += camera_velocity_y * elapsed_time
    camera_3D.x += camera_velocity_x * elapsed_time

    # Apply friction to slow down the camera when no keys are pressed
    camera_velocity_y *= camera_friction
    camera_velocity_x *= camera_friction

    # Optional: Clamp velocity to prevent excessive speed
    max_velocity = 20.0
    camera_velocity_y = max(min(camera_velocity_y, max_velocity), -max_velocity)
    camera_velocity_x = max(min(camera_velocity_x, max_velocity), -max_velocity)

    # dt = clock.tick(60)  # Limit frame rate to 60 FPS (returns elapsed time in milliseconds)

    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_DOWN]:
    #     camera_velocity -= camera_speed * dt / 1000
    # elif keys[pygame.K_UP]:
    #     camera_velocity += camera_speed * dt / 1000
    # else:
    #     # Apply deceleration when no keys are pressed
    #     camera_velocity *= 0.90  # Adjust the decay factor as needed

    # # Update camera position using velocity
    # camera_3D.y += camera_velocity

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
        #     if event.key == pygame.key.get_pressed():
        #         camera_3D.y -= 0.5

        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_UP:
        #         camera_3D.y += 0.5

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass
                
    # Updating Rotation Matrices

    # theta1 += 0.03
    
    Mat_X_Rot = Matrix_3D.X_Rotation(theta1)
    Mat_Y_Rot = Matrix_3D.Y_Rotation(theta1)
    Mat_Z_Rot = Matrix_3D.Z_Rotation(theta1)

    look_dir = Vector(0,0,1)
    up = Vector(0,1,0)
    target = camera_3D + look_dir

    View_Mat = Matrix_3D.View_for_CameraPointAt(camera_3D,target,up)

    # Applying Transformations
    TriangleToRasterList=[]

    screen.fill(SCREEN_COLOR) # Reset Screen

    for tri in Monkey.triangles:
        
        # Appling multiplications for rotation
        # Rotate in X-axis
        X_Rotated_tri=Matrix_3D.MatTriMul(tri,Mat_X_Rot)

        # Rotate in Z-axis
        ZX_Rotated_tri=Matrix_3D.MatTriMul(X_Rotated_tri,Mat_Z_Rot)

        # Rotate in Y-axis
        YZX_Rotated_tri=Matrix_3D.MatTriMul(ZX_Rotated_tri,Mat_Y_Rot)

        #Translating Triangles along the Z-axis
        Translated_tri = YZX_Rotated_tri
        Translated_tri.v0.z += 8.0
        Translated_tri.v1.z += 8.0
        Translated_tri.v2.z += 8.0

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
            Projected_tri = Matrix_3D.MatTriMul(View_tri,Mat_Proj)
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
        pygame.draw.polygon(screen,tri.color,
                            ((tri.v0.x,tri.v0.y),
                             (tri.v1.x,tri.v1.y),
                             (tri.v2.x,tri.v2.y)))

    pygame.display.update()
    
    # Setting Max FPS
    clock.tick(60)