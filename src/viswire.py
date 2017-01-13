#~ from matplotlib import pylab
import numpy as np
from    mayavi import mlab
import sys
import subprocess
from subprocess import PIPE
import glob
import networkx as nx

def bondlength(pts,bond):
    dr = pts[bond[1]] - pts[bond[0]]
    return np.linalg.norm(dr)
    
def bondlengths(pts,bonds):
    drs = pts[bds[:,1]]-pts[bds[:,0]]
    return np.sqrt(np.sum(drs**2, axis=1))

def espring(pts,bonds,l0=0.0330422):
    es = -np.ones(len(pts))
    for bond in bonds:
        espring = (bondlength(pts,bond)-l0)/l0
        if es[bond[0]] <  espring:
            es[bond[0]] = espring
        if es[bond[1]] < espring:
            es[bond[1]] = espring
    return es

def get_facets_qhull(coords):
    #~ coord_str = StringIO.StringIO()
    qhullp = subprocess.Popen(['qhull','i','Qt'],stdin=PIPE,stdout=PIPE)
    qhullp.stdin.write('%d\n' % (3))
    qhullp.stdin.write('%d\n' % (len(coords)))
    for pt in coords:
        qhullp.stdin.write('%2.8f %2.8f %2.8f\n' % (pt[0],pt[1],pt[2]))
    qhullp.stdin.flush()
    resultstr = qhullp.communicate()[0]
    #~ return resultstr.partition('\n')[2]
    return np.fromstring(resultstr.partition('\n')[2],dtype=int,sep = ' ').reshape((-1,3))


def get_bonds(facets):
    bonds = []
    for facet in facets:
        bonds.append(np.sort([facet[0],facet[1]]))
        bonds.append(np.sort([facet[1],facet[2]]))
        bonds.append(np.sort([facet[2],facet[0]]))
        
    c = np.array(bonds, dtype = int)
    #~ return np.unique1d(c.view([('',c.dtype)]*c.shape[1])).view (c.dtype).reshape(-1,c.shape[1]) 
    return np.unique(c.view([('',c.dtype)]*c.shape[1])).view (c.dtype).reshape(-1,c.shape[1]) 

def get_bonds_cutoff(facets,coords,cutoff=1.1):
    bonds = []
    for facet in facets:
        if np.sqrt(np.sum((coords[facet[0]]-coords[facet[1]])**2)) < cutoff:
            bonds.append(np.sort([facet[0],facet[1]]))
        if np.sqrt(np.sum((coords[facet[1]]-coords[facet[2]])**2)) < cutoff:
            bonds.append(np.sort([facet[1],facet[2]]))
        if np.sqrt(np.sum((coords[facet[2]]-coords[facet[0]])**2)) < cutoff:
            bonds.append(np.sort([facet[2],facet[0]]))
        
    c = np.array(bonds, dtype = int)
    #~ return np.unique1d(c.view([('',c.dtype)]*c.shape[1])).view (c.dtype).reshape(-1,c.shape[1]) 
    return np.unique(c.view([('',c.dtype)]*c.shape[1])).view (c.dtype).reshape(-1,c.shape[1]) 
    

def draw_bonds_color_qhull(coords, bonds=False,scale_factor=1,resolution=15):
    '''
    color by coordination number
    '''
    nn = get_bonds(get_facets_qhull(coords))
    G = nx.Graph()
    G.add_edges_from(nn)
    deg = np.array([G.degree(i) for i in G.nodes()])
    idx4 = np.where(deg <= 4)
    idx5 = np.where(deg == 5)
    idx6 = np.where(deg == 6)
    idx7 = np.where(deg == 7)
    idx8 = np.where(deg >= 8)
    
    x,y,z = coords.T
    mlab.points3d(x[idx4],y[idx4],z[idx4], scale_factor=scale_factor,resolution=resolution,color = (0,0,1))
    mlab.points3d(x[idx5],y[idx5],z[idx5], scale_factor=scale_factor,resolution=resolution,color = (0,0,1))
    mlab.points3d(x[idx6],y[idx6],z[idx6], scale_factor=scale_factor,resolution=resolution,color = (.7,.7,.1))
    mlab.points3d(x[idx7],y[idx7],z[idx7], scale_factor=scale_factor,resolution=resolution,color = (1,0,0))
    mlab.points3d(x[idx8],y[idx8],z[idx8], scale_factor=scale_factor,resolution=resolution,color = (1,0,0))
    points = mlab.points3d(x,y,z, scale_factor=scale_factor/10,resolution=4, color = tuple(np.random.random(3)))
    if bonds==True:
        points.mlab_source.dataset.lines = nn
        points.mlab_source.update()
        mlab.pipeline.surface(points, representation='wireframe',color=(0.3,0.3,0.3))
    
def draw_bonds_color(coords, bonds,scale_factor=.25,resolution=6):
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
    mlab.points3d(x[idx4],y[idx4],z[idx4], scale_factor=scale_factor,resolution=resolution,color = (0,0,1))
    mlab.points3d(x[idx5],y[idx5],z[idx5], scale_factor=scale_factor,resolution=resolution,color = (0,0,1))
    mlab.points3d(x[idx6],y[idx6],z[idx6], scale_factor=scale_factor,resolution=resolution,color = (.6,.6,.6))
    mlab.points3d(x[idx7],y[idx7],z[idx7], scale_factor=scale_factor,resolution=resolution,color = (1,0,0))
    mlab.points3d(x[idx8],y[idx8],z[idx8], scale_factor=scale_factor,resolution=resolution,color = (.2,.2,.7))
    points = mlab.points3d(x,y,z, scale_factor=scale_factor/10,resolution=4, color = tuple(np.random.random(3)))
    points.mlab_source.dataset.lines = nn
    points.mlab_source.update()
    mlab.pipeline.surface(points, representation='wireframe',color=(0.2,0.2,0.2))
    
def draw_bonds_bl(coords, bonds=False,scale_factor=1,resolution=15):
    '''
    color by coordination number
    '''
    nn = get_bonds_cutoff(get_facets_qhull(coords),coords)
    
    G = nx.Graph()
    G.add_edges_from(nn)
    distances = [np.sqrt(np.sum((coords[i]-coords[j])**2)) for i,j in G.edges()]
    dists_by_pt = [np.average([np.sqrt(np.sum((coords[i]-coords[j])**2)) for j in G.neighbors(i)]) for i in G.nodes()]
    
    
    x,y,z = coords.T
    print len(x), len(y),len(z),len(dists_by_pt)
    points = mlab.points3d(x,y,z, dists_by_pt, scale_mode='none',scale_factor=scale_factor,resolution=resolution,vmin = 1., vmax=1.05)
    if bonds==True:
        points.mlab_source.dataset.lines = nn
        points.mlab_source.update()
        mlab.pipeline.surface(points, representation='wireframe',color=(0.2,0.2,0.2))

def draw_bonds(coords, bonds,scale_factor=.3,resolution=6):
    '''
    color by coordination number
    '''
    x,y,z = coords.T
    points = mlab.points3d(x,y,z, scale_mode='none',scale_factor=scale_factor,resolution=resolution)
    
    points.mlab_source.dataset.lines = bonds
    points.mlab_source.update()
    mlab.pipeline.surface(points, representation='wireframe',color=(0.5,0.5,0.5))


files = sys.argv[1:]
if len(files) == 0: files = ['XVertexM.txt','Bpost_test.txt'] # default files to open

# rgb color white is 1,1,1
unicol = (224./256,212./256,232./256)
unicol = (232./256,232./256,232./256)
#~ unicol = (1,1,1)

for i in range(len(files)):
    filename = files[i]
    if filename[-1] == '.': filename += 'pts'
    print filename
    ar = np.loadtxt(filename)
    print ar.shape
    
    bondfile = filename[:-4] + '.bds'
    print bondfile
    bds = np.loadtxt(bondfile,dtype=int)
    
    fctfile = filename[:-4] + '.fct'
    print fctfile
    fct = np.loadtxt(fctfile,dtype=int)

    dls = espring(ar,bds)
    
    x,y,z = ar.T
    #3D Visualization 
    f=mlab.figure(i,size=(400, 400),bgcolor=(1,1,1))
    #~ mlab.title(filename, figure=f)
    #~ edges = get_facets_qhull(ar)
    mesh=mlab.triangular_mesh(x,y,z,fct,color=(.8,.8,.8))

    draw_bonds_color(ar,bds,scale_factor=.08,resolution=8)
    #~ draw_bonds(ar,bds,scale_factor=.35)
    #~ mlab.title(filename, figure=f, height=.9,size=.5)
    mlab.figure(i)
    #~ mlab.view(-90,90,50)
    #~ mlab.roll(90)


mlab.show()
