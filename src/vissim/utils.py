import config as cfg
from PIL import Image

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import numpy as np

def add_image_new(x0, y0):
    eps = 0.2
    new_xy = []
    for i in [-1.,0.,1.]:
        for j in [-1.,0.,1.]:
            if i != 0 or j != 0:
                x = x0 + i + j*cfg.SPIN*cfg.DGAMMA
                y = y0 + j 

                if x > -eps and x < 1.+eps:
                    if y > -eps and y < 1.+eps:
                        new_xy.append( [x,y] )

    return new_xy


def draw_disk(d0,x0,y0,rgb):
    THETAS = np.linspace(0,2*np.pi,20,endpoint=True)
    THETAS_BOLD = np.linspace(0,2*np.pi,360,endpoint=True)
    DT = (THETAS[1]-THETAS[0])
    c = 1.0
    s = 0.0

    glBegin(GL_TRIANGLES)
    for t in THETAS:
        x_ = d0 * np.cos(t + DT)
        y_ = d0 * np.sin(t + DT)
        x1 = x_ * c - y_ * s + x0;
        y1 = x_ * s + y_ * c + y0;
        x_ = d0 * np.cos(t + 2*DT)
        y_ = d0 * np.sin(t + 2*DT)
        x2 = x_ * c - y_ * s + x0;
        y2 = x_ * s + y_ * c + y0;
        
        glColor3f(rgb[0], rgb[1], rgb[2])
        glVertex3f(x0,y0,0)
        glVertex3f(x1,y1,0)
        glVertex3f(x2,y2,0)

        
    glEnd()

    if cfg.BOLD:
        glPointSize(2)
        glBegin(GL_POINTS)
        for t in THETAS_BOLD:
            x_ = d0 * np.cos(t + DT)
            y_ = d0 * np.sin(t + DT)
            x1 = x_ * c - y_ * s + x0
            y1 = x_ * s + y_ * c + y0
            if rgb[0] == 1 and rgb[1] == 1 and rgb[2] == 0:
                glColor3f(1, 0.75, 0.0)
            else:        
                glColor3f(0.5, 0.5, 0.5)
            glVertex3f(x1, y1, 0.0)
        glEnd()

def draw_contacts_bonds(contacts, bonds):
  
    glLineWidth(3.0)
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_LINES)
    
    for contact in contacts:
        x1,y1 = contact[0], contact[1]
        x2,y2 = contact[2], contact[3]
        glVertex3f(x1,y1, 0.0)
        glVertex3f(x2,y2, 0.0)
    glEnd()
    
    glLineWidth(3.0)
    glColor3f(.5, .5, .5)
    glBegin(GL_LINES)
    
    for bond in bonds:
        x1,y1 = bond[0], bond[1]
        x2,y2 = bond[2], bond[3]
        glVertex3f(x1,y1, 0.0)
        glVertex3f(x2,y2, 0.0)
    glEnd()


def DisplayCallback():
    """
    """
    try: 
        glClearColor(1.0, 1.0, 1.0, 1.0)
        glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
        glPushMatrix() 

        frame = cfg.FRAMES[cfg.SPIN]
        RGB_ = frame.get_RGB()
        outer_disks = []
        
        if cfg.UNC:
            contacts, bonds, uncs = frame.calc_contacts_bonds()
        
        for i in range( frame.get_N() ):
            d0 = frame.get_D(i)
            x0 = frame.get_X(i)
            y0 = frame.get_Y(i)
            rgb = RGB_[i]

            ll = add_image_new(x0, y0)
            
            
            if cfg.UNC:
                if uncs[i] == 0: # and i % 2 == 1:
                    rgb = [1,1,0]
            
            if len( ll ) > 0:
                for el_ll in ll: 
                    if cfg.PBC:
                        outer_disks.append([d0,el_ll[0],el_ll[1],rgb])
                    else:
                        outer_disks.append([d0,el_ll[0],el_ll[1], [0,1,0]])

            draw_disk(d0,x0,y0,rgb)
    
        for disk in outer_disks:
            draw_disk(disk[0], disk[1], disk[2], disk[3])

        if cfg.CONTACTS:
            contacts, bonds, uncs = frame.calc_contacts_bonds()
            draw_contacts_bonds(contacts, bonds)


        glPopMatrix()
        glutSwapBuffers()

        if cfg.MOVIE:
            ScreenShot( "./frames/frame_%03d.png" % (cfg.SPIN) )
 

    except KeyboardInterrupt:
        print("\n*** Pressed Ctrl-C: EXITING ***")
        import sys
        sys.exit(1)
        
    
def ReshapeCallback(w, h):
    """

    """
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    if cfg.BIGSCREEN == 1:
        glOrtho(-0.3, 1.3, -0.3, 1.3, -1.0, 1.0)
    else:
        glOrtho(0., 1., 0., 1., -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()



def KeyboardCallback(key, x, y):
    """
    """

    if key == 'm':
        cfg.MOVIE = 1 - cfg.MOVIE
        cfg.SPINSTEP = 1 # not sure it that's the best choice
    elif key == '>':
        cfg.SPINSTEP += 1
    elif key == '<':
        cfg.SPINSTEP -= 1
    elif key == '+':
        cfg.SPIN += 1
        cfg.SPINSTEP = 0;
    elif key == '-':
        cfg.SPIN -= 1
        cfg.SPINSTEP = 0;
    elif key == 's':
        cfg.SPINSTEP = 0
    elif key == 'f':
        cfg.SPIN = 0
        cfg.SPINSTEP = 0
    elif key == 'l':
        cfg.SPIN = len(cfg.FRAMES)-1
        cfg.SPINSTEP = 0
    elif key == 'b':
        cfg.BOLD = 1 - cfg.BOLD
    elif key == 'p':
        cfg.PBC = 1 - cfg.PBC
    elif key == 'u':
        cfg.UNC = 1 - cfg.UNC
    elif key == 'c':
        cfg.CONTACTS = 1 - cfg.CONTACTS
    elif key == 'w':
        ScreenShot( "./frames/frame_%03d.png" % (cfg.SPIN) )
    elif key == '\x1b':             # ESC
        import sys
        sys.exit()
    else:
        print("KEY NOT RECOGNIZED")

    glutIdleFunc(SpinCallback)


def SpecialCallback():
    """
    FOR NOW THERE IS NO SPECIAL CALLBACKS
    """
    pass


def MouseCallback(button, state, x, y):
    """
    FOR NOW THE MOUSE IS INACTIVE
    """
    pass


def SpinCallback():
    """
    """
    
    cfg.SPIN += cfg.SPINSTEP
    
    if  cfg.SPIN >= len(cfg.FRAMES):
        cfg.SPIN = 0
    
    elif cfg.SPIN < 0:
        cfg.SPIN = len(cfg.FRAMES)-1
    
    glutPostRedisplay()


def ScreenShot(filename):
    """
    """
    try:
        glReadBuffer(GL_FRONT)
        pixels = glReadPixels(0,0,cfg.SIZEX,cfg.SIZEY,GL_RGB,GL_UNSIGNED_BYTE)
                            
        image = Image.frombytes("RGB", (cfg.SIZEX, cfg.SIZEY), pixels)
        image = image.transpose( Image.FLIP_TOP_BOTTOM)
        image.save(filename)
    except IOError as err:
        print(err.args)
        print("Create a folder and then try agains.")



