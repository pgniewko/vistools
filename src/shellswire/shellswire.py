#! /usr/bin/env python

import sys
import numpy as np
from mayavi import mlab
import networkx as nx


def draw_bonds_color(coords, bonds, scale_factor=.25, resolution=6):
    '''
    color by coordination number
    '''
    nn = bonds
    G = nx.Graph()
    G.add_edges_from(nn)
    deg = np.array([G.degree(i) for i in G.nodes()])
    idx4 = np.where(deg <= 4)
    idx5 = np.where(deg == 5)
    idx6 = np.where(deg == 6)
    idx7 = np.where(deg == 7)
    idx8 = np.where(deg >= 8)
    
    x,y,z = coords.T
    mlab.points3d(x[idx4], y[idx4], z[idx4], scale_factor=scale_factor, resolution=resolution, color = (0,0,1))
    mlab.points3d(x[idx5], y[idx5], z[idx5], scale_factor=scale_factor, resolution=resolution, color = (0,0,1))
    mlab.points3d(x[idx6], y[idx6], z[idx6], scale_factor=scale_factor, resolution=resolution, color = (.6,.6,.6))
    mlab.points3d(x[idx7], y[idx7], z[idx7], scale_factor=scale_factor, resolution=resolution, color = (1,0,0))
    mlab.points3d(x[idx8], y[idx8], z[idx8], scale_factor=scale_factor, resolution=resolution, color = (.2,.2,.7))
    points = mlab.points3d(x, y, z, scale_factor=scale_factor/10,resolution=4, color = tuple(np.random.random(3)))
    points.mlab_source.dataset.lines = nn
    points.mlab_source.update()
    mlab.pipeline.surface(points, representation='wireframe', color=(0.2, 0.2, 0.2))
    return 


def draw_bonds(coords, bonds, scale_factor=.3, resolution=6, cc=(0.3, 0.3, 0.3)):
    '''
    unicolor
    '''
    x, y, z = coords.T
    points = mlab.points3d(x, y, z, scale_mode='none', scale_factor=scale_factor, resolution=resolution, color=cc)
    
    points.mlab_source.dataset.lines = bonds
    points.mlab_source.update()
    mlab.pipeline.surface(points, representation='wireframe', color=(0.5, 0.5, 0.5))
    return 


def pbc_image(c, Lc):
     nc = c
     if c < 0.0:
         nc += Lc
 
     if c >= Lc:
         nc -= Lc
 
     return nc


def scale_coords(xyz_l, bx, by, bz, size_=5.0):

    maxb = max( max(bx, by), bz)
    scale = size_ / maxb
    print "Scaling factor:", scale
    for xyz in xyz_l:
        xyz[0] *= scale
        xyz[1] *= scale
        xyz[2] *= scale
        
    return xyz_l, scale


def get_registered_verts(filename):
    fin = open(filename)    
    vertex_map = {}
    reversed_vertex_map = {}
    
    for line in fin:
        if line.startswith("VMAP"):
            pairs = line.split()
            vname = pairs[1]
            cell_id = int(pairs[2])
            v_id = int(pairs[3])
            vertex_map[vname] = [cell_id, v_id]
            reversed_vertex_map[ (cell_id, v_id) ] = vname

    fin.close()
    
    return vertex_map, reversed_vertex_map


def get_triangles(filename):
    fin = open(filename)
    triangles_list = []
    
    for line in fin:
        if line.startswith("CELLTRIANG"):
            pairs = line.rstrip('\n').split()
            cellid = int(pairs[1])
            vid1 = int(pairs[3])
            vid2 = int(pairs[4])
            vid3 = int(pairs[5])
            triangles_list.append( [cellid, vid1, vid2, vid3] )

    fin.close()

    return triangles_list


def get_coord_hash(fname):
    fin = open(fname)
    tra_xyz = []
    tra_xyz_hash = {}
    line_counter = 0
    x_box = 0
    y_box = 0
    z_box = 0

    cc = 0

    for line in fin:
        line_counter += 1

        pairs = line.rstrip('\n').split()

        if line_counter == 1:
            num_verts = int(pairs[0])
            x_box = float(pairs[1])
            y_box = float(pairs[2])
            z_box = float(pairs[3])
            Lx = 2.0 * x_box
            Ly = 2.0 * y_box
            Lz = 2.0 * z_box

        if line_counter > 1:
            vname = pairs[0]
            x = float(pairs[1])
            y = float(pairs[2])
            z = float(pairs[3])
            x += x_box
            y += y_box
            z += z_box
            
            tra_xyz.append( [x, y, z] )
            tra_xyz_hash[vname] = cc
            cc += 1

    fin.close()

    return tra_xyz_hash, tra_xyz, Lx, Ly, Lz


def get_xyz_bds_fcts(triangles_list, reversed_vertex_map, tra_xyz, tra_hash, cell_ids):
    x = []
    y = []
    z = []
    
    cells_xyz = []
    cells_bds = []
    cells_tri = []

    for triangle in triangles_list:
        tcellid = triangle[0]
        vid1 = triangle[1]
        vid2 = triangle[2]
        vid3 = triangle[3]

        vid1_name = reversed_vertex_map[ (tcellid, vid1) ]
        vid2_name = reversed_vertex_map[ (tcellid, vid2) ]
        vid3_name = reversed_vertex_map[ (tcellid, vid3) ]

        vix1 = tra_hash[vid1_name] 
        vix2 = tra_hash[vid2_name]
        vix3 = tra_hash[vid3_name]
     
        cells_tri.append( [vix1, vix2, vix3] )
        cells_bds.append( (min(vix1, vix2), max(vix1, vix2)) )
        cells_bds.append( (min(vix1, vix3), max(vix1, vix3)) )
        cells_bds.append( (min(vix2, vix3), max(vix2, vix3)) )

    cells_bds = list( set(cells_bds) )
    return cells_bds, cells_tri


file_name = sys.argv[1]
top_fname = sys.argv[2]
color_flag = int(sys.argv[3])

tra_hash, tra_xyz, Lx, Ly, Lz = get_coord_hash(file_name)
tra_xyz, sc = scale_coords(tra_xyz, 0.5*Lx, 0.5*Ly, 0.5*Lz)
Lx *= sc
Ly *= sc
Lz *= sc
vertex_map, reversed_vertex_map = get_registered_verts(top_fname)
triangles_list = get_triangles(top_fname)
cells_bds, cells_tri = get_xyz_bds_fcts(triangles_list, reversed_vertex_map, tra_xyz, tra_hash, [1])

bds = []
for el in cells_bds:
     bds.append(el)

bds = np.array(bds, dtype=int)

fct = []
for el in cells_tri:
    fct.append(el)

fct = np.array(fct, dtype=int)

ar = []
for xyz in tra_xyz:
    ar.append(xyz)

ar = np.array(ar)
x, y, z = ar.T


f = mlab.figure(0, size=(600, 600), bgcolor=(1, 1, 1))
mesh = mlab.triangular_mesh(x, y, z, fct, color=(.8, .8, .8))


if color_flag == 1:    
    draw_bonds_color(ar, bds, scale_factor=.1, resolution=8)
else:
    draw_bonds(ar, bds, scale_factor=.1, resolution=8)

eps=0.1
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
mlab.plot3d([0, Lx], [Ly, Ly], [Lz, Lz], color=black, tube_radius=eps)


mlab.show()


