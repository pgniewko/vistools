#! /usr/bin/env python

import sys
import numpy as np
from mayavi import mlab

eps = 0.001
phi = ( 1.0 + np.sqrt(5.0) ) / 2.0

def fct_center(vts):
    xyz = [0.0, 0.0, 0.0]

    for vt in vts:
        xyz[0] += vt[0]
        xyz[1] += vt[1]
        xyz[2] += vt[2]

    xyz[0] /= len(vts)
    xyz[1] /= len(vts)
    xyz[2] /= len(vts)

    return xyz

def f_1(vt, a, b):
    fv = phi*vt[0] + a*vt[1] + b * phi * phi
    if abs(fv) < eps:
        return True
    else:
        return False


def f_2(vt, a, b):
    fv = phi*vt[1] + a*vt[2] + b * phi * phi
    if abs(fv) < eps:
        return True
    else:
        return False


def f_3(vt, a, b):
    fv = phi*vt[2] + a*vt[0] + b * phi * phi
    if abs(fv) < eps:
        return True
    else:
        return False

def edge(v1, v2):
    dx = v1[0] - v2[0]
    dy = v1[1] - v2[1]
    dz = v1[2] - v2[2]

    dr = dx*dx + dy*dy + dz*dz
    dr = np.sqrt(dr)

    if abs(dr - 2.0/phi) < eps:
        return True

    return False

verts = []
verts.append( [ 1, 1, 1] )
verts.append( [ 1, 1,-1] )
verts.append( [ 1,-1, 1] )
verts.append( [-1, 1, 1] )

verts.append( [ 1,-1,-1] )
verts.append( [-1, 1,-1] )
verts.append( [-1,-1, 1] )
verts.append( [-1,-1,-1] )


verts.append( [ 1/phi, phi, 0] )
verts.append( [-1/phi, phi, 0] )
verts.append( [ 1/phi,-phi, 0] )
verts.append( [-1/phi,-phi, 0] )

verts.append( [ phi, 0, 1/phi] )
verts.append( [-phi, 0, 1/phi] )
verts.append( [ phi, 0,-1/phi] )
verts.append( [-phi, 0,-1/phi] )

verts.append( [ 0, 1/phi, phi] )
verts.append( [ 0,-1/phi, phi] )
verts.append( [ 0, 1/phi,-phi] )
verts.append( [ 0,-1/phi,-phi] )
################################


XYZ = np.array(verts).T
mlab.points3d(XYZ[0], XYZ[1], XYZ[2], scale_factor=0.1, opacity=1.0, color=(0,0,1))

fcts = []

fct = []
for row in verts:
    if f_1(row, 1.0, 1.0):
        fct.append(row)
fcts.append(fct)

fct = []
for row in verts:
    if f_1(row, 1.0,-1.0):
        fct.append(row)
fcts.append(fct)

fct = []
for row in verts:
    if f_1(row,-1.0, 1.0):
        fct.append(row)
fcts.append(fct)

fct = []
for row in verts:
    if f_1(row,-1.0,-1.0):
        fct.append(row)
fcts.append(fct)

######
fct = []
for row in verts:
    if f_2(row, 1.0, 1.0):
        fct.append(row)
fcts.append(fct)

fct = []
for row in verts:
    if f_2(row, 1.0,-1.0):
        fct.append(row)
fcts.append(fct)

fct = []
for row in verts:
    if f_2(row,-1.0, 1.0):
        fct.append(row)
fcts.append(fct)

fct = []
for row in verts:
    if f_2(row,-1.0,-1.0):
        fct.append(row)
fcts.append(fct)

#########
fct = []
for row in verts:
    if f_3(row, 1.0, 1.0):
        fct.append(row)
fcts.append(fct)

fct = []
for row in verts:
    if f_3(row, 1.0,-1.0):
        fct.append(row)
fcts.append(fct)

fct = []
for row in verts:
    if f_3(row,-1.0, 1.0):
        fct.append(row)
fcts.append(fct)

fct = []
for row in verts:
    if f_3(row,-1.0,-1.0):
        fct.append(row)
fcts.append(fct)
        
for i in range(len(verts)):
    for j in range(len(verts)):
        v1 = verts[i]
        v2 = verts[j]
        if edge(v1, v2) and i > j:
            x1 = v1[0]
            x2 = v2[0]
            y1 = v1[1]
            y2 = v2[1]
            z1 = v1[2]
            z2 = v2[2]
            mlab.plot3d([x1, x2], [y1, y2], [z1, z2], color=(0,0,0), tube_radius=0.025)

for fct in fcts:
    v = fct_center(fct)
    mlab.points3d( v[0], v[1], v[2], scale_factor=0.10, opacity=1.0, color=(1,0,0))
    s='{ %10.8f, %10.8f, %10.8f },' % (v[0], v[1], v[2])
    print s



mlab.show()
