import numpy as np
from shade_triangle import *

def render(verts2d,faces,vcolors,depth,shade_t):
    
    # Initialize of the matrix X-image 
    X = np.ones((512,512,3))
    Dm = np.zeros(faces.shape[0])
    V1 = np.zeros((3,2))
    C1 = np.zeros((3,3))
    D_sorted = np.zeros(faces.shape[0])
    D_order = np.zeros(faces.shape[0])

    # Calculation of the average depth of each triangle 
    for i in range(0,faces.shape[0]):
        for j in range(0,3):
            Dm[i] = depth[faces[i,j]]+Dm[i]
        Dm[i] = Dm[i]/3
        
    # Sort of the Dm and the faces in descending order 
    # In D_order is the indexes osrted the same way as Dm and faces
    D_order  = np.flip(np.argsort(Dm))
    D_sorted = np.flip(np.sort(Dm))
    faces = faces[D_order,:]
    Dm = D_sorted

    for i in range(0,faces.shape[0]):
        for j in range(0,3):
            # V1 is an 3x2 array with th coordinates of the triangle
            # C1 is an 3x3 array with the color of each peak
            V1[j,0] = verts2d[faces[i,j],0]
            V1[j,1] = verts2d[faces[i,j],1]
            C1[j,:] = vcolors[faces[i,j],:]
        
        # 'flat' for flat  and 'gouraud' for the Gouraud
        if shade_t == "flat" or shade_t == "gouraud":
            X = shade_triangle(X,V1,C1,shade_t)
        else:
            print("wrong input")
            break

    return X