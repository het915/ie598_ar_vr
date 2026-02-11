import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import math

FOV_Y_DEG = 110.0
NEAR_Z = 0.1
FAR_Z = 20.0
ASPECT_RATIO = 1.0
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

CUBE_DEPTHS = [-2.0, -5.0, -10.0]
VISUALIZATION_MODE = 1

cam_yaw = 45.0
cam_pitch = 30.0
cam_distance = 25.0
mouse_down = False
last_mouse_pos = (0, 0)

def calculate_frustum_bounds(fov_y_deg, aspect, near):
    fov_rad = math.radians(fov_y_deg)
    top = near * math.tan(fov_rad / 2.0)
    bottom = -top
    right = top * aspect
    left = -right
    return left, right, bottom, top

def build_projection_matrix(l, r, b, t, n, f):
    X = (2.0 * n) / (r - l)
    Y = (2.0 * n) / (t - b)
    A = (r + l) / (r - l)
    B = (t + b) / (t - b)
    C = -(f + n) / (f - n)
    D = -(2.0 * f * n) / (f - n)

    P = np.array([
        [X, 0, 0, 0],
        [0, Y, 0, 0],
        [A, B, C, -1],
        [0, 0, D, 0]
    ], dtype=np.float32)
    return P

def draw_cube_at(x, y, z, size=1.0, color=(1,1,1)):
    half = size / 2.0
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(*color)
    
    vertices = [
        (-half, -half, half), (half, -half, half), 
        (half, half, half), (-half, half, half),
        (-half, -half, -half), (half, -half, -half), 
        (half, half, -half), (-half, half, -half)
    ]
    edges = [
        (0,1),(1,2),(2,3),(3,0),
        (4,5),(5,6),(6,7),(7,4),
        (0,4),(1,5),(2,6),(3,7)
    ]
    
    glBegin(GL_LINES)
    for edge in edges:
        for vertex_idx in edge:
            glVertex3fv(vertices[vertex_idx])
    glEnd()
    glPopMatrix()

def draw_frustum_visual(l, r, b, t, n, f):
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    
    nc = [(l, b, -n), (r, b, -n), (r, t, -n), (l, t, -n)]
    
    ratio_f = f / n
    fc = [
        (l*ratio_f, b*ratio_f, -f), 
        (r*ratio_f, b*ratio_f, -f), 
        (r*ratio_f, t*ratio_f, -f), 
        (l*ratio_f, t*ratio_f, -f)
    ]

    for v in nc: 
        glVertex3f(0,0,0)
        glVertex3fv(v)
    
    for i in range(4): 
        glVertex3fv(nc[i])
        glVertex3fv(fc[i])
    
    for i in range(4): 
        glVertex3fv(fc[i])
        glVertex3fv(fc[(i+1)%4])
    
    glEnd()

def main():
    global VISUALIZATION_MODE, cam_yaw, cam_pitch, cam_distance, mouse_down, last_mouse_pos
    
    pygame.init()
    display = (WINDOW_WIDTH, WINDOW_HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glEnable(GL_DEPTH_TEST)

    l, r, b, t = calculate_frustum_bounds(FOV_Y_DEG, ASPECT_RATIO, NEAR_Z)
    proj_matrix = build_projection_matrix(l, r, b, t, NEAR_Z, FAR_Z)
    colors = [(0,1,0), (0,1,1), (1,0,1)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    VISUALIZATION_MODE = (VISUALIZATION_MODE + 1) % 3
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
                    last_mouse_pos = pygame.mouse.get_pos()
                elif event.button == 4: 
                    cam_distance = max(1.0, cam_distance - 1.0)
                elif event.button == 5: 
                    cam_distance = min(50.0, cam_distance + 1.0)
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1: 
                    mouse_down = False
            elif event.type == MOUSEMOTION:
                if mouse_down:
                    cur_pos = pygame.mouse.get_pos()
                    dx = cur_pos[0] - last_mouse_pos[0]
                    dy = cur_pos[1] - last_mouse_pos[1]
                    cam_yaw -= dx * 0.5
                    cam_pitch += dy * 0.5
                    cam_pitch = max(-89.0, min(89.0, cam_pitch))
                    last_mouse_pos = cur_pos

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        rad_yaw = math.radians(cam_yaw)
        rad_pitch = math.radians(cam_pitch)
        eyeX = cam_distance * math.cos(rad_pitch) * math.sin(rad_yaw)
        eyeY = cam_distance * math.sin(rad_pitch)
        eyeZ = cam_distance * math.cos(rad_pitch) * math.cos(rad_yaw)

        if VISUALIZATION_MODE == 0:
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            glLoadMatrixf(proj_matrix) 
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            for i, z in enumerate(CUBE_DEPTHS):
                draw_cube_at(z/10.0, 0, z, size=1.0, color=colors[i])
                
        elif VISUALIZATION_MODE == 1:
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            target = (0,0,-5)
            gluLookAt(target[0]+eyeX, target[1]+eyeY, target[2]+eyeZ, *target, 0, 1, 0)
            
            draw_frustum_visual(l, r, b, t, NEAR_Z, FAR_Z)
            for i, z in enumerate(CUBE_DEPTHS):
                draw_cube_at(z/10.0, 0, z, size=1.0, color=colors[i])

        elif VISUALIZATION_MODE == 2:
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(45, (display[0]/display[1]), 0.1, 100.0)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            target = (0,0,0)
            
            ndc_dist = cam_distance / 4.0
            nEyeX = ndc_dist * math.cos(rad_pitch) * math.sin(rad_yaw)
            nEyeY = ndc_dist * math.sin(rad_pitch)
            nEyeZ = ndc_dist * math.cos(rad_pitch) * math.cos(rad_yaw)
            gluLookAt(target[0]+nEyeX, target[1]+nEyeY, target[2]+nEyeZ, *target, 0, 1, 0)
            
            draw_cube_at(0,0,0, size=2.0, color=(0.5,0.5,0.5))

            glPointSize(8.0)
            for i, z_depth in enumerate(CUBE_DEPTHS):
                point_world = np.array([(z_depth/10.0)+0.5, 0.5, z_depth+0.5, 1.0], dtype=np.float32)
                clip_coords = point_world.dot(proj_matrix.T)
                ndc_coords = clip_coords[:3] / clip_coords[3]
                
                glBegin(GL_POINTS)
                glColor3f(*colors[i])
                glVertex3fv(ndc_coords)
                glEnd()
                
                glBegin(GL_LINES)
                glVertex3fv(ndc_coords)
                glVertex3f(0, 0, ndc_coords[2])
                glEnd()

        pygame.display.flip()
        pygame.time.wait(10)
    
    pygame.quit()

if __name__ == "__main__":
    main()