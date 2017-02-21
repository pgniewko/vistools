#! /usr/bin/env python

import sys
import numpy as np
from mayavi import mlab
from scipy.ndimage import measurements, label, generate_binary_structure
from ioutils import read_xyz_file_perco
from utils import percolating_clusters


def calc_volume(labs, Nx, Ny, Nz, idx):
    volume = 0.0
    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                if labs[i][j][k] == idx:
                    volume += 1.0
    
    return volume

def calc_area(labs, Nx, Ny, Nz, idx):
    area = 0.0
    
    for i in range(Nx):
     for j in range(Ny):
      for k in range(Nz):
       for m in range(-1,0,1):
        for n in range(-1,0,1):
         for o in range(-1,0,1):
          if (i+m) >= 0 and (i+m) < Nx and (j+n) >= 0 and (j+n) < Ny and (k+o) >= 0 and (k+o) < Nz:
           if labs[i][j][k] == idx and labs[i+m][j+n][n+o] == 0:
            area += 1.0
    
    return area
    


file_name = sys.argv[1]
eps = float(sys.argv[2])

frame_xyz, Tot_n, box_x, box_y, box_z, Lx, Ly, Lz, X_dim, Y_dim, Z_dim, epsx, epsy, epsz = read_xyz_file_perco(file_name, eps)

X_real = []
Y_real = []
Z_real = []

for xyz_coor in frame_xyz:
        X_real.append(xyz_coor[0])
        Y_real.append(xyz_coor[1])
        Z_real.append(xyz_coor[2])

#mlab.points3d(X_real, Y_real, Z_real, scale_factor=0.2, opacity=1.0, color=(1,0,0))


black = (0,0,0)
mlab.plot3d([0, Lx], [0, 0], [0, 0], color=black, tube_radius=0.1)
mlab.plot3d([0, 0], [0, Ly], [0, 0], color=black, tube_radius=0.1)
mlab.plot3d([0, 0], [0, 0], [0, Lz], color=black, tube_radius=0.1)
mlab.plot3d([Lx, Lx], [0, Ly], [0, 0], color=black, tube_radius=0.1)
mlab.plot3d([0, Lx], [Ly, Ly], [0, 0], color=black, tube_radius=0.1)
mlab.plot3d([Lx, Lx], [0, 0], [0, Lz], color=black, tube_radius=0.1)
mlab.plot3d([Lx, Lx], [Ly, Ly], [0, Lz], color=black, tube_radius=0.1)
mlab.plot3d([0, 0], [Ly, Ly], [0, Lz], color=black, tube_radius=0.1)
mlab.plot3d([0, Lx], [0, 0], [Lz, Lz], color=black, tube_radius=0.1)
mlab.plot3d([Lx, Lx], [0, Ly], [Lz, Lz], color=black, tube_radius=0.1)
mlab.plot3d([0, 0], [0, Ly], [Lz, Lz], color=black, tube_radius=0.1)
mlab.plot3d([0, Lx], [Ly, Lz], [Lz, Lz], color=black, tube_radius=0.1)


# BELOW CONSTRUCT  LATTICE

lattice_3d = np.ones([X_dim, Y_dim, Z_dim])

for coor in frame_xyz:
    x_ix = int( coor[0] / epsx )
    y_ix = int( coor[1] / epsy )
    z_ix = int( coor[2] / epsz )
    lattice_3d[x_ix][y_ix][z_ix] = 0


X_3d = []
Y_3d = []
Z_3d = []

for i in range(X_dim):
    for j in range(Y_dim):
        for k in range(Z_dim):
            if lattice_3d[i][j][k] == 0:
                    X_3d.append(i*epsx)
                    Y_3d.append(j*epsy)
                    Z_3d.append(k*epsz)


s = generate_binary_structure(3,1)
labeled_array, num_features = label(lattice_3d, structure=s)

percs = percolating_clusters(labeled_array, X_dim, Y_dim, Z_dim)
#print "number of clusters=", num_features
#print percs

volumes = []
areas = []
for ix in percs:
    if ix == 0:
        continue

    volumes.append( calc_volume(labeled_array, X_dim, Y_dim, Z_dim, ix) )
    areas.append( calc_area(labeled_array, X_dim, Y_dim, Z_dim, ix) )
    
    X_3d_c = []
    Y_3d_c = []
    Z_3d_c = []
 
    R = 0.0 #np.random.rand() 
    G = 1.0 #np.random.rand() 
    B = 0.0 #np.random.rand() 

    for i in range(X_dim):
        for j in range(Y_dim):
            for k in range(Z_dim):
                if labeled_array[i][j][k] == ix:
                    X_3d_c.append(i*epsx)
                    Y_3d_c.append(j*epsy)
                    Z_3d_c.append(k*epsz)

    mlab.points3d(X_3d_c, Y_3d_c, Z_3d_c, mode='cube', scale_factor=max( max(epsx, epsy),epsz ), opacity=1.0, color=(R,G,B))

mlab.show()

print volumes[0], areas[0], volumes[0]/areas[0]
#print "VOLUMES:", volumes
#print "AREAS: ", areas
#print "V/A:", np.array(volumes)/np.array(areas)

