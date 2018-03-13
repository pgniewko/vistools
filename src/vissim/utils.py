import config as cfg
from OpenGL._bytes import as_8_bit
from PIL import Image
from Frame import Frame

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

import numpy as np

def _triangle(r_,g_,b_,x1,x2,x3):
    glBegin(GL_TRIANGLES)
    glColor3f(r_,g_,b_)
    glVertex3f(x1[0],x1[1],x1[2])
    glVertex3f(x2[0],x2[1],x2[2])
    glVertex3f(x3[0],x3[1],x3[2])
    glEnd()

def DisplayCallback():
    """
    """
    
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT)
    glPushMatrix() 
    
    glPointSize(2); #set point size to 10 pixels
    glBegin(GL_POINTS);

    tl_    = np.linspace(0,2*np.pi,10,endpoint=True)
    dt = (tl_[1]-tl_[0])/2.0
    ratios = np.linspace(1.0,0.0,10,endpoint=True) 


    frame = cfg.FRAMES[cfg.SPIN]
    RGB_ = frame.get_RGB()
    for i in range( frame.get_N() ):
        d0 = frame.get_D(i)
        x0 = frame.get_X(i)
        y0 = frame.get_Y(i)
        #print x0, y0, cfg.SPIN, i, cfg.SPINSTEP
        c = 1.0
        s = 0.0
        #rgb = frame.get_RGB(i)
        rgb = RGB_[i]
        if cfg.BOLD:
            dr_ = Frame.dr
        else:
            dr_ = 0.0

        for t in tl_:
            for ratio in ratios:
                if ratio > (1.0-dr_):
                    glColor3f(0.5, 0.5, 0.5)
                else:
                    glColor3f(rgb[0], rgb[1], rgb[2])


                x_ = ratio * d0 * np.cos(t + dt)
                y_ = ratio * d0 * np.sin(t + dt)
                x2 = x_ * c - y_ * s + x0;
                y2 = x_ * s + y_ * c + y0;
                #x2 -= 0.5;
                #y2 -= 0.5;
                #corx = rint(x2);
                cory = int(y2)
                #y2 = y2 ;//- delry[index] * corx;
                y2 = y2 - int(y2)
                #x2 = x2 - delrx[index] * cory;
                
                #print x2, x2 - int(x2)
                x2 = x2 - int(x2)
                
                glVertex3f(x2, y2, 0.0);



    glEnd()
    glPopMatrix()
    glutSwapBuffers()

    if cfg.MOVIE:
        ScreenShot( "./frames/frame_" + str(cfg.SPIN)+".png")

    
def ReshapeCallback(w, h):
    """

    """
    glViewport(0, 0, w, h);
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)
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
    elif key == 'w':
        ScreenShot( "./frames/frame_%04d.png" % (cfg.SPIN) )
    #elif key == '\x1b':             # ESC
    elif key == as_8_bit( '\033' ):  # ESC
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


#dump back buffer to image
def ScreenShot(filename):
    """
    """
    glReadBuffer(GL_FRONT)
    pixels = glReadPixels(0,0,cfg.SIZEX,cfg.SIZEY,GL_RGB,GL_UNSIGNED_BYTE)
                            
    image = Image.fromstring("RGB", (cfg.SIZEX, cfg.SIZEY), pixels)
    image = image.transpose( Image.FLIP_TOP_BOTTOM)
    image.save(filename)



