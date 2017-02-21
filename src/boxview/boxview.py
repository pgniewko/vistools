#! /usr/bin/env python

import sys
from mayavi import mlab
from ioutils import read_xyz_file

#

file_name = sys.argv[1]
eps = float(sys.argv[2])

frame_xyz, frame_xyz_image, Tot_n, box_x, box_y, box_z, Lx, Ly, Lz = read_xyz_file(file_name)

X_real = []
Y_real = []
Z_real = []

X_image = []
Y_image = []
Z_image = []
for xyz_coor in frame_xyz:
        X_real.append(xyz_coor[0])
        Y_real.append(xyz_coor[1])
        Z_real.append(xyz_coor[2])

for xyz_coor in frame_xyz_image:
        X_image.append(xyz_coor[0])
        Y_image.append(xyz_coor[1])
        Z_image.append(xyz_coor[2])

mlab.points3d(X_real, Y_real, Z_real, scale_factor=2.0*eps, opacity=1.0, color=(0,0,1))
mlab.points3d(X_image, Y_image, Z_image, scale_factor=2.0*eps, opacity=1.0, color=(0,1,0))

black = (0,0,0)
white = (1,1,1)
mlab.plot3d([0, Lx], [0, 0], [0, 0], color=black, tube_radius=eps)
mlab.plot3d([0, 0], [0, Ly], [0, 0], color=black, tube_radius=eps)
mlab.plot3d([0, 0], [0, 0], [0, Lz], color=black, tube_radius=eps)
mlab.plot3d([Lx, Lx], [0, Ly], [0, 0], color=black, tube_radius=eps)
mlab.plot3d([0, Lx], [Ly, Ly], [0, 0], color=black, tube_radius=eps)
mlab.plot3d([Lx, Lx], [0, 0], [0, Lz], color=black, tube_radius=eps)
mlab.plot3d([Lx, Lx], [Ly, Ly], [0, Lz], color=black, tube_radius=eps)
mlab.plot3d([0, 0], [Ly, Ly], [0, Lz], color=black, tube_radius=eps)
mlab.plot3d([0, Lx], [0, 0], [Lz, Lz], color=black, tube_radius=eps)
mlab.plot3d([Lx, Lx], [0, Ly], [Lz, Lz], color=black, tube_radius=eps)
mlab.plot3d([0, 0], [0, Ly], [Lz, Lz], color=black, tube_radius=eps)
mlab.plot3d([0, Lx], [Ly, Lz], [Lz, Lz], color=black, tube_radius=eps)

mlab.show()
