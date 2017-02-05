def pbc_image(c, Lc):
    nc = c
    if c < 0.0:
        nc += Lc

    if c >= Lc:
        nc -= Lc

    return nc 


def build_9_boxes(traj_xyz, Lx, Ly, Lz, pbc=True):
    
    new_xyz_traj = []
    for i in [-1,0,1]:
        for j in [-1, 0, 1]:
            for k in [-1,0,1]:
                for xyz_ in traj_xyz:
                    xn = xyz_[0] + i*Lx 
                    yn = xyz_[1] + j*Ly
                    zn = xyz_[2] + k*Lz
                    new_xyz_traj.append([xn, yn, zn])
    

    return new_xyz_traj

        
def cull_points(traj_xyz, Lx, Ly, Lz, epsx, epsy, epsz):
    new_xyz_traj = []
    for xyz_ in traj_xyz:
        x = xyz_[0]
        y = xyz_[1]
        z = xyz_[2]
        sc = 1.0
        if x > -sc * epsx  and x < Lx + sc * epsx:
          if y > -sc * epsy  and y < Ly + sc * epsy:
            if z > -sc * epsz  and z < Lz + sc * epsz:
              new_xyz_traj.append( [x, y, z] )


    return new_xyz_traj

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
    
    return frame_xyz, frame_xyz_image, Tot_n, box_x, box_y, box_z, Lx, Ly, Lz



def read_xyz_file_perco(file_name, eps, pbc=True):
    fin = open(file_name)
    frame_xyz = []
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

            X_dim = int(Lx / eps) + 1
            Y_dim = int(Ly / eps) + 1
            Z_dim = int(Lz / eps) + 1
            epsx = Lx / (X_dim-1)
            epsy = Ly / (Y_dim-1)
            epsz = Lz / (Z_dim-1)

        else:
            X = float(pairs[1])
            Y = float(pairs[2])
            Z = float(pairs[3])
            X += box_x
            Y += box_y
            Z += box_z
        
            Xn = pbc_image(X, Lx)
            Yn = pbc_image(Y, Ly)
            Zn = pbc_image(Z, Lz)
            
            frame_xyz.append([Xn, Yn, Zn])
         
    frame_xyz_ = build_9_boxes(frame_xyz, Lx, Ly, Lz)
    frame_xyz_ = cull_points(frame_xyz_, Lx, Ly, Lz, epsx, epsy, epsz)

    return frame_xyz_, Tot_n, box_x, box_y, box_z, Lx, Ly, Lz, X_dim, Y_dim, Z_dim, epsx, epsy, epsz
