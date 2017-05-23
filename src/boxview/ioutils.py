def pbc_image(c, Lc):
    nc = c
    if c < 0.0:
        nc += Lc

    if c >= Lc:
        nc -= Lc

    return nc 

def scale_coords(xyz_l, bx, by, bz, size_=5.0):

    maxb = max( max(bx, by), bz)
    scale = size_/maxb
    print "Scaling factor:", scale
    for xyz in xyz_l:
        xyz[0] *= scale
        xyz[1] *= scale
        xyz[2] *= scale

    return xyz_l, scale

def read_xyz_file(file_name):
    fin = open(file_name)
    frame_xyz = []
    frame_xyz_image = []
    line_counter = 0

    for line in fin:
        line_counter += 1
        pairs = line.rstrip('\n').split()

        if line_counter == 1:
            Tot_n = int(pairs[0])
            box_x = float(pairs[1])
            box_y = float(pairs[2])
            box_z = float(pairs[3])
            Lx = 2.0 * box_x
            Ly = 2.0 * box_y
            Lz = 2.0 * box_z
            
        else:
            X = float(pairs[1])
            Y = float(pairs[2])
            Z = float(pairs[3])
            X += box_x
            Y += box_y
            Z += box_z

            frame_xyz.append([X, Y, Z])
        
            Xn = pbc_image(X, Lx)
            Yn = pbc_image(Y, Ly)
            Zn = pbc_image(Z, Lz)
        
            if Xn != X or Yn != Y or Zn != Z:
                frame_xyz_image.append([Xn, Yn, Zn])
   
    frame_xyz, sc = scale_coords(frame_xyz, box_x, box_y, box_z)
    frame_xyz_image, sc = scale_coords(frame_xyz_image, box_x, box_y, box_z)

    return frame_xyz, frame_xyz_image, Tot_n, box_x, box_y, box_z, sc* Lx, sc*Ly, sc*Lz
