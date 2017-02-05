
def x_percs(latt, Lx, Ly, Lz):
    first_wall = []
    second_wall = []

    percs = []

    for i in range(Ly):
        for j in range(Lz):
            if latt[0][i][j] != 0:
               first_wall.append(latt[0][i][j])

    first_wall = sorted(set( first_wall ))

    for i in range(Ly):
        for j in range(Lz):
            if latt[Lx-1][i][j] != 0:
                second_wall.append(latt[Lx-1][i][j])

    second_wall = sorted(set( second_wall ))

            
    for i in range( len(first_wall) ):
        for j in range( len(second_wall) ):
            if first_wall[i] == second_wall[j]:
                percs.append( int(first_wall[i]) )

    return percs


def y_percs(latt, Lx, Ly, Lz):
    first_wall = []
    second_wall = []

    percs = []

    for i in range(Lx):
        for j in range(Lz):
            if latt[i][0][j] != 0:
               first_wall.append(latt[i][0][j])

    first_wall = sorted(set( first_wall ))

    for i in range(Lx):
        for j in range(Lz):
            if latt[i][Ly-1][j] != 0:
                second_wall.append(latt[i][Ly-1][j])

    second_wall = sorted(set( second_wall ))

            
    for i in range( len(first_wall) ):
        for j in range( len(second_wall) ):
            if first_wall[i] == second_wall[j]:
                percs.append( int(first_wall[i]) )

    return percs

def z_percs(latt, Lx, Ly, Lz):
    first_wall = []
    second_wall = []

    percs = []

    for i in range(Lx):
        for j in range(Ly):
            if latt[i][j][0] != 0:
               first_wall.append(latt[i][j][0])

    first_wall = sorted(set( first_wall ))

    for i in range(Lx):
        for j in range(Ly):
            if latt[i][j][Lz-1] != 0:
                second_wall.append(latt[i][j][Lz-1])


    second_wall = sorted(set( second_wall ))

            
    for i in range( len(first_wall) ):
        for j in range( len(second_wall) ):
            if first_wall[i] == second_wall[j]:
                percs.append( int(first_wall[i]) )

    return percs

def percolating_clusters(latt, Lx, Ly, Lz):
    xlist = x_percs( latt, Lx, Ly, Lz )
    ylist = y_percs( latt, Lx, Ly, Lz )
    zlist = z_percs( latt, Lx, Ly, Lz )

    clusters_ids = [] 
    for xe in xlist:
        clusters_ids.append(xe)
    
    for ye in ylist:
        clusters_ids.append(ye)
    
    for ze in zlist:
        clusters_ids.append(ze)
 
    clusters_ids = sorted(set( clusters_ids ))
    return clusters_ids    





