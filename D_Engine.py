import os
import pygame 
from sys import exit
import math as m
from Geometry import *
from Physics import SceneObject,PhysicsWorld

def hex_to_rgb(hex_color):
    """
    Convert a hex color string to an RGB tuple.

    Args:
        hex_color (str): Hexadecimal color string (e.g., "#FFFFFF" or "FFFFFF").

    Returns:
        tuple: A tuple representing the RGB values (R, G, B).
    """
    hex_color = hex_color.lstrip('#')  # Remove '#' if present

    if len(hex_color) != 6:
        raise ValueError("Input should be a 6-character hex color code.")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

#Declaring Constants 
SCREEN_COLOR = (23,23,23)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN_SIZE = (SCREEN_WIDTH,SCREEN_HEIGHT)
LINE_COLOR = "#A9DDD6"
LINE_THICKNESS = 1
ROTATION_SPEED = 0.0  # Radians per second
CAMERA_VELOCITY_Y = 0
CAMERA_VELOCITY_X = 0
MAX_VELOCITY = 60.0
CAMERA_ACCELERATION = 40
CAMERA_FRICTION = 0.95
SHADOW = hex_to_rgb("#1B1767")
HIGHLIGHT = hex_to_rgb("#03C5CF")
WALKING_VELOCITY = 0
WALKING_ACCELERATION = 60
WALKING_FRICTION = 0.90
STRAFING_VELOCITY = 0
STRAFING_ACCELERATION = 40
STRAFING_FRICTION = 0.90
MOUSE_SENSITIVITY = 0.05
GRAVITY = -10
FOV = 90.0
 
#Declaring Variables
wire_render = False
yaw = 0
pitch = 0
click_pos = None

# Loading Object Data

object_folder = "objects"

objects = sorted([f for f in os.listdir(object_folder) if f.endswith('.obj')])

current_object_index = 0

Object = Mesh_3D.LoadObjFile(os.path.join(object_folder,objects[current_object_index]))

Cube = Mesh_3D.LoadObjFile(os.path.join("objects","cube.obj"))
Sphere = Mesh_3D.LoadObjFile(os.path.join("objects","sphere.obj"))
Cylinder = Mesh_3D.LoadObjFile(os.path.join("objects","cylinder.obj"))

# Creating Plane
Znear_Plane         =   Plane(normal = Vector(0,0,1.0) , point = Vector(0,0,0.1))
upper_screen_plane  =   Plane(normal = Vector(0,1.0,0) , point = Vector(0,0,0))
bottom_screen_plane =   Plane(normal = Vector(0,-1.0,0) , point = Vector(0,SCREEN_HEIGHT,0))
right_screen_plane  =   Plane(normal = Vector(-1.0,0,0) , point = Vector(SCREEN_WIDTH,0,0))
left_screen_plane   =   Plane(normal = Vector(1.0,0,0) , point = Vector(0,0,0))

Cliping_Planes = [upper_screen_plane,bottom_screen_plane,right_screen_plane,left_screen_plane]

# Creating Matrices
Proj_Mat=Matrix_3D.Projection(A=SCREEN_WIDTH/SCREEN_HEIGHT,FOV=FOV,Zn=0.1,Zf=1000.0)

# Defining Characteristic Vectors
camera_3D = Vector(0,0,0)
light_dir = Vector(0,1,-1)
light_dir.Normalize()

# Setting up the Pygame Window/Screen
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.event.set_grab(True)
pygame.display.set_caption("3D Engine")
pygame.mouse.set_visible(True)
clock=pygame.time.Clock()

tri1 = Triangle((-4,-4,0),(0,4,0),(4,-4,0))
Cube_3D = Mesh_3D((tri1,tri1))

new_world = PhysicsWorld(GRAVITY)
new_world.add_objects([SceneObject(Cube, Vector(0,4,7), Vector(1,1,1), Vector(0,0,0)),
                       SceneObject(Cube, Vector(-4,2,6), Vector(1,1,1), Vector(0,0,0)),
                       SceneObject(Cube, Vector(-4,9,6), Vector(1,1.3,1), Vector(0,0,0)),
                       SceneObject(Cylinder, Vector(3,20,20), Vector(2,3,2), Vector(0,0,3))])

# Engine Update Loop
while True:
    keys = pygame.key.get_pressed()
    elapsed_time = clock.get_time() / 1000.0 # Convert milliseconds to seconds

    # Checking keys for Key Press

    # Axis Movements
    if keys[pygame.K_DOWN]:
        CAMERA_VELOCITY_Y -= CAMERA_ACCELERATION * elapsed_time
    if keys[pygame.K_UP]:
        CAMERA_VELOCITY_Y += CAMERA_ACCELERATION * elapsed_time
    if keys[pygame.K_LEFT]:  
        CAMERA_VELOCITY_X += CAMERA_ACCELERATION * elapsed_time
    if keys[pygame.K_RIGHT]:
        CAMERA_VELOCITY_X -= CAMERA_ACCELERATION * elapsed_time

    # Vertical Movements
    if keys[pygame.K_SPACE]:
        CAMERA_VELOCITY_Y += CAMERA_ACCELERATION * elapsed_time
    if keys[pygame.K_LSHIFT]:
        CAMERA_VELOCITY_Y -= CAMERA_ACCELERATION * elapsed_time

    # FP Movements
    if keys[pygame.K_a]:
        STRAFING_VELOCITY -= STRAFING_ACCELERATION * elapsed_time
    if keys[pygame.K_d]:
        STRAFING_VELOCITY += STRAFING_ACCELERATION * elapsed_time
    if keys[pygame.K_w]:
        WALKING_VELOCITY += WALKING_ACCELERATION * elapsed_time
    if keys[pygame.K_s]:
        WALKING_VELOCITY -= WALKING_ACCELERATION * elapsed_time

    # Checking events and keys for KEYDOWN
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEMOTION:
            yaw -= event.rel[0] * MOUSE_SENSITIVITY * elapsed_time
            pitch += event.rel[1] * MOUSE_SENSITIVITY * elapsed_time

            pitch = max(min(pitch, m.pi/2 - 0.1), -m.pi/2 + 0.1)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click_pos = event.pos

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit() 
                exit()

            if event.key == pygame.K_e:
                current_object_index = (current_object_index + 1) % len(objects)
                Object = Mesh_3D.LoadObjFile(os.path.join(object_folder,objects[current_object_index]))
            
            if event.key == pygame.K_q:
                current_object_index = (current_object_index - 1) % len(objects)
                Object = Mesh_3D.LoadObjFile(os.path.join(object_folder,objects[current_object_index]))
        
            if event.key == pygame.K_HOME:
                camera_3D = Vector(0,0,0)
                CAMERA_VELOCITY_Y = 0
                CAMERA_VELOCITY_X = 0
                yaw , pitch = 0 , 0
        
            if event.key == pygame.K_TAB: 
                wire_render = not wire_render
            
            if wire_render:
                if event.key == pygame.K_j and LINE_THICKNESS != 1:
                    LINE_THICKNESS -= 1
                
                if event.key == pygame.K_k:
                    LINE_THICKNESS += 1

    # Apply velocity to camera position
    camera_3D.y += CAMERA_VELOCITY_Y * elapsed_time
    camera_3D.x += CAMERA_VELOCITY_X * elapsed_time

    # Apply friction to slow down the camera when no keys are pressed
    CAMERA_VELOCITY_Y *= CAMERA_FRICTION
    CAMERA_VELOCITY_X *= CAMERA_FRICTION
    

    # Optional: Clamp velocity to prevent excessive speed
    CAMERA_VELOCITY_Y = max(min(CAMERA_VELOCITY_Y, MAX_VELOCITY), -MAX_VELOCITY)
    CAMERA_VELOCITY_X = max(min(CAMERA_VELOCITY_X, MAX_VELOCITY), -MAX_VELOCITY)

    look_dir = Vector(0,0,1)
    up = Vector(0,1,0)
    up.Normalize()
    Yaw_Mat = Matrix_3D.Y_Rotation(yaw)
    Pitch_Mat = Matrix_3D.X_Rotation(pitch)
    Mouse_Rot_Mat = Yaw_Mat @ Pitch_Mat
    look_dir = Matrix_3D.MatVectorMul(look_dir,Mouse_Rot_Mat)
    look_dir.Normalize()
    target = camera_3D + look_dir
    # light_dir = look_dir * -1

    View_Mat , right = Matrix_3D.View_for_CameraPointAt(camera_3D,target,up)

    new_world.step(elapsed_time)

    WALKING_DISPLACEMENT = look_dir * (WALKING_VELOCITY * elapsed_time)
    STRAFING_DISPLACEMENT = right * (STRAFING_VELOCITY * elapsed_time)
    # print("displacement : ", STRAFING_DISPLACEMENT)
    camera_3D += WALKING_DISPLACEMENT + STRAFING_DISPLACEMENT
    # print("Camera3D : ",camera_3D)

    WALKING_VELOCITY *= WALKING_FRICTION
    STRAFING_VELOCITY *= STRAFING_FRICTION
    

    # Processing Objects 

    screen.fill(SCREEN_COLOR) # Reset Screen

    world_tris = []
    for obj in new_world.objects:
        world_tris.extend(obj.world_triangles())

    # Rasterization Pipeline
    if click_pos is not None:
        position,direction = screen_to_ray(click_pos[0],click_pos[1],
                                           SCREEN_WIDTH,SCREEN_HEIGHT,
                                           camera_3D,look_dir,right,up,FOV)
        
        closest_t = float('inf')
        hit_tri = None

        for tri in world_tris:
            t = ray_triangle_intersect(position,direction,tri)
            
            if t is not None and t < closest_t:
                closest_t = t
                hit_tri = tri
        if hit_tri:
            print("Hit Triangle at : ", position + direction * closest_t)
        click_pos = None

    # Rasterization Pipeline
   
    Triangles = []
    for tri in world_tris:
                  
        #Calculating Culling conditon
        view_direction = tri.v0 - camera_3D
        dot_product = tri.normal ** view_direction

        if dot_product < 0.0:  #backface culling condition

            #Lighting
            Illumination_dp = tri.normal ** light_dir
            if Illumination_dp < 0 : Illumination_dp = 0
            tri.GetColor(SHADOW,HIGHLIGHT,Illumination_dp)

            View_tri = Matrix_3D.MatTriMul(tri,View_Mat)
            View_tri.color = tri.color

            for Clip_tri in Znear_Plane.clip_triangle(View_tri):

                #Projecting the Triangles
                Projected_tri = Matrix_3D.MatTriMul(Clip_tri,Proj_Mat)
                Projected_tri.color = Clip_tri.color

                #Scaling the triangles
                Projected_tri.v0.x += 1.0
                Projected_tri.v1.x += 1.0
                Projected_tri.v2.x += 1.0
                Projected_tri.v0.y += 1.0
                Projected_tri.v1.y += 1.0
                Projected_tri.v2.y += 1.0

                Projected_tri.v0.x *= 0.5 * SCREEN_HEIGHT
                Projected_tri.v0.y *= 0.5 * SCREEN_WIDTH
                Projected_tri.v1.x *= 0.5 * SCREEN_HEIGHT
                Projected_tri.v1.y *= 0.5 * SCREEN_WIDTH
                Projected_tri.v2.x *= 0.5 * SCREEN_HEIGHT
                Projected_tri.v2.y *= 0.5 * SCREEN_WIDTH
                
                Triangles.append(Projected_tri)  
        
    for plane in Cliping_Planes:
        clipped_triangles = []
        for tri in Triangles:
            clipped_triangles.extend(plane.clip_triangle(tri))
        Triangles = clipped_triangles  # Update the list with the clipped triangles so that they can be clipped against remaining planes
             
    for tri in Triangles:
        tri.order = (tri.v0.z + tri.v1.z +tri.v2.z)/3
        tri.v0.y = SCREEN_HEIGHT - tri.v0.y
        tri.v1.y = SCREEN_HEIGHT - tri.v1.y
        tri.v2.y = SCREEN_HEIGHT - tri.v2.y

    Triangles.sort(key=lambda tri: tri.order , reverse=True)

    for tri in Triangles:
    #Drawing the Triangles on the Screen
        if wire_render == False:    
            pygame.draw.polygon(screen,  tri.color,
                                ((tri.v0.x,tri.v0.y),
                                (tri.v1.x,tri.v1.y),
                                (tri.v2.x,tri.v2.y)))
        else:
            pygame.draw.polygon(screen,  LINE_COLOR,
                                ((tri.v0.x,tri.v0.y),
                                (tri.v1.x,tri.v1.y),
                                (tri.v2.x,tri.v2.y)),LINE_THICKNESS)
                
            
    pygame.display.update()
    
    # Setting Max FPS
    clock.tick(120)