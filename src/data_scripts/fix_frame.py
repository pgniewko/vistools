#! /usr/bin/env python

import sys

top_file_name = sys.argv[1]
tra_file_name = sys.argv[2]


# 1.
fin = open(top_file_name)

vertex_map = {}
reversed_vertex_map = {}
triangles_list = []

for line in fin:
    if line.startswith("VMAP"):
        pairs = line.split()
        vname = pairs[1]
        cell_id = int(pairs[2])
        v_id = int(pairs[3])
        vertex_map[vname] = [cell_id, v_id]
        reversed_vertex_map[ (cell_id, v_id) ] = vname
   
    if line.startswith("CELLTRIANG"):
        pairs = line.rstrip('\n').split()
        cellid = int(pairs[1])
        vid1 = int(pairs[3])
        vid2 = int(pairs[4])
        vid3 = int(pairs[5])
        triangles_list.append( [cellid, vid1, vid2, vid3] )

fin.close()
###########



# 2.
fin = open(tra_file_name)
line_counter = 0
x_box = 0
y_box = 0
z_box = 0
num_verts = 0
tra_xyz = {}
coords_list = []

for line in fin:
    line_counter += 1

    pairs = line.rstrip('\n').split()

    if line_counter == 1:
        num_verts = int(pairs[0])
        x_box = float(pairs[1])
        y_box = float(pairs[2])
        z_box = float(pairs[3])
 
    if line_counter > 1:
        coords_list.append( line.rstrip('\n') )
        vname = pairs[0]
        x = float(pairs[1])
        y = float(pairs[2])
        z = float(pairs[3])
        tra_xyz[vname] = [x, y, z]
fin.close()

print num_verts + len(triangles_list), x_box, y_box, z_box

for coor in coords_list:
    print coor

for triangle in triangles_list:
    tcellid = triangle[0]
    vid1    = triangle[1]
    vid2    = triangle[2]
    vid3    = triangle[3]

    vid1_name = reversed_vertex_map[ (tcellid, vid1) ]
    vid2_name = reversed_vertex_map[ (tcellid, vid2) ]
    vid3_name = reversed_vertex_map[ (tcellid, vid3) ]

    v1_xyz = tra_xyz[vid1_name] 
    v2_xyz = tra_xyz[vid2_name]
    v3_xyz = tra_xyz[vid3_name]

    X_av = ( v1_xyz[0] + v2_xyz[0] + v3_xyz[0]) / 3.0
    Y_av = ( v1_xyz[1] + v2_xyz[1] + v3_xyz[1]) / 3.0
    Z_av = ( v1_xyz[2] + v2_xyz[2] + v3_xyz[2]) / 3.0

    print "EXTR", X_av, Y_av, Z_av

