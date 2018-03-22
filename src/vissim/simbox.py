#! /usr/bin/env python
"""
DOCUMENTATION
"""

_version__ = '0.0.2'
__date__   = '2018/12/03'

import sys

from Frame import Frame
from utils import *
import config as cfg

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print "OpenGL wrapper for python not found"


def read_frames(file_name, L):
    cfg.FRAMES

    fin = open(file_name,'rU')
    
    x = []
    y = []
    d = []
    c = []
    N = 0
    phi = 0

    for line in fin:
        pairs = line.split()
        if len(pairs) == 2:
            frame = Frame(N,phi,x,y,d,c,L_=L)
            x = []
            y = []
            d = []
            c = []
            N   = int(pairs[0])
            phi = float(pairs[1])
          
            cfg.FRAMES.append(frame)

        elif len(pairs) == 4:
            xi = float(pairs[0])
            yi = float(pairs[1])
            di = 0.5*float(pairs[2])
            ci = int(pairs[3])
            
            x.append(xi)
            y.append(yi)
            d.append(di)
            c.append(ci)

    cfg.FRAMES = cfg.FRAMES[1:]
    print( str( len( cfg.FRAMES ) ) + " FRAMES ARE READ")


def display_sim(sizex_=720,sizey_=720,initx=-1,inity=-1):
    cfg.SIZEX = sizex_
    cfg.SIZEY = sizey_
    # Initialize the OpenGL pipeline
    glutInit(sys.argv)

    # Set OpenGL display mode
    glutInitDisplayMode (GLUT_SINGLE | GLUT_RGB)

    # Set the Window size and position
    glutInitWindowSize(cfg.SIZEX,cfg.SIZEY)
    glutInitWindowPosition(initx,inity)


    # Create the window with given title
    glutCreateWindow("*** PRESS 'w' TO GRAB SCREENSHOT ***")


   
    glutDisplayFunc(DisplayCallback)
    glutReshapeFunc(ReshapeCallback)
    glutKeyboardFunc(KeyboardCallback)
    glutSpecialFunc(SpecialCallback)
    glutMouseFunc(MouseCallback)
    glutIdleFunc(SpinCallback)

    glutMainLoop()

def init():
    glClearColor (0.0, 0.0, 0.0, 0.0)
    glShadeModel (GL_FLAT)

if __name__ == "__main__":
    fname = sys.argv[1]
    L = float(sys.argv[2])
    if len(sys.argv) > 3:
        cfg.DGAMMA = float(sys.argv[3])


    read_frames(fname, L)
    display_sim()


