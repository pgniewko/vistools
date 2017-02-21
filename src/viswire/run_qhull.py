#!/usr/bin/python

import numpy as np
from sys import argv
import subprocess
from subprocess import PIPE

def flip_normals(coords, facets):
    '''
    make sure the normals point outward from the origin
    '''
    facetsC = np.copy(facets)
    normsorig = []
    vms = []
    for i in range(len(facets)):
        f = facets[i]
        v1 = coords[f[0]]
        v2 = coords[f[1]]
        v3 = coords[f[2]]
        vc = np.cross(v2-v1,v3-v2)
        normsorig.append(vc/np.linalg.norm(vc)/10.)
        vm = (v1+v2+v3)/3.
        vms.append(vm)
        mc = np.dot(vm, vc)
        if mc < 0:
            #~ print i
            facetsC[i] = [f[1],f[0],f[2]]
    
    x,y,z = np.array(vms).T
    u,v,w = np.array(normsorig).T
    #~ mlab.quiver3d(x,y,z,u,v,w)
    
    return facetsC


def get_facets_qhull(coords):
    #~ coord_str = StringIO.StringIO()
    #~ qhullp = subprocess.Popen(['qhull','i','Qt'],stdin=PIPE,stdout=PIPE,bufsize=-1)
    if coords.shape[1] == 3:
        qhullp = subprocess.Popen(['qhull','i','Qt'],stdin=PIPE,stdout=PIPE,bufsize=-1)
        qhullp.stdin.write('%d\n' % (3))
        qhullp.stdin.write('%d\n' % (len(coords)))
        for pt in coords:
            qhullp.stdin.write('%2.8f %2.8f %2.8f\n' % (pt[0],pt[1],pt[2]))
    if coords.shape[1] == 2:
        qhullp = subprocess.Popen(['qhull','d','i','Qt'],stdin=PIPE,stdout=PIPE,bufsize=-1)
        qhullp.stdin.write('%d\n' % (2))
        qhullp.stdin.write('%d\n' % (len(coords)))
        for pt in coords:
            qhullp.stdin.write('%2.8f %2.8f\n' % (pt[0],pt[1]))
    qhullp.stdin.flush()
    resultstr = qhullp.communicate()[0]
    #~ print np.fromstring(resultstr.partition('\n')[2],dtype=int,sep = ' ')
    return np.fromstring(resultstr.partition('\n')[2],dtype=int,sep = ' ').reshape((-1,3))


def get_bonds(facets):
    bonds = []
    for facet in facets:
        bonds.append(np.sort([facet[0],facet[1]]))
        bonds.append(np.sort([facet[1],facet[2]]))
        bonds.append(np.sort([facet[2],facet[0]]))
        
    c = np.array(bonds, dtype = int)
    return np.unique(c.view([('',c.dtype)]*c.shape[1])).view (c.dtype).reshape(-1,c.shape[1]) 
   

pts = np.loadtxt(argv[1])
facets = get_facets_qhull(pts)
facets = flip_normals(pts,facets)
bonds = get_bonds(facets)
np.savetxt(argv[1][:-3]+'bds', bonds,fmt='%d')
np.savetxt(argv[1][:-3]+'fct', facets,fmt='%d')
