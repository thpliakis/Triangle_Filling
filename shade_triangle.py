import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from numpy import linalg
from interpolate_color import *
import matplotlib

def shade_triangle(img,verts2d,vcolors,shade_t):
    
    #   The image Y=img with  the triangles in which, every time the function is called, one triangle will be colored 
    # Initialization of the matrixes
    Y = img
    c     = np.zeros(3)   # Here the average color of a trinagle is stored for flat mode
    Ykmin = np.zeros((3,1))      
    Xkmin = np.zeros((3,1))
    m     = np.zeros((3,1))   # m is where the gradient of every side is stored
    Ykmax = np.zeros((3,1))
    Xkmax = np.zeros((3,1))
    Xk    = np.zeros((3,1))
    er  = np.zeros((3,1))
    ActiveSides = np.zeros((3,1))   #If Activesides[i] == 1 the side is active
    Xact = np.zeros(2)        #Here the x coordinate of the Active side is stored
  
    # Extra variables for shate_t = "gouraud"
    # Indexes of the active sides, to know which of the 3 are active
    Xact2 = np.zeros(2,dtype=int)
    indexAct = np.zeros((2,1),dtype=int)
    x1 = np.zeros(2)
    x2 = np.zeros(2)
    C1 = np.zeros(3)
    C2 = np.zeros(3)
    x3 = np.zeros(2)
    x4 = np.zeros(2)
    C3 = np.zeros(3)
    C4 = np.zeros(3)
    # In pairs the vertices that every side is between are stored  
    pairs = np.zeros((3,2),dtype=int)

    # The interpolated colors are saved here
    colorsXact = np.zeros((2,3))
    
    # In this loop we compare the coordinate-Y of 2 peaks for every side and we
    # save the minimum value to Ykmin and at the same time 
    # the matching X to the array Xkmin, same with the max values.
    # In addition we find the slope of every side (m) and keep the pairs
    for i in range(0,2):
        if verts2d[i,1]<verts2d[i+1,1]:
            Ykmin[i] = verts2d[i,1]
            Xkmin[i] = verts2d[i,0]
            Ykmax[i] = verts2d[i+1,1]
            Xkmax[i] = verts2d[i+1,0]
            pairs[i][0] = i
            pairs[i][1] = i+1
        else:
            Ykmin[i] = verts2d[i+1,1]
            Xkmin[i] = verts2d[i+1,0]
            Ykmax[i] = verts2d[i,1]
            Xkmax[i] = verts2d[i,0]
            pairs[i][0] = i+1
            pairs[i][1] = i
        if (verts2d[i+1,0]-verts2d[i,0]) == 0:
            m[i] = np.inf
        else:
            m[i]=(verts2d[i+1,1]-verts2d[i,1])/(verts2d[i+1,0]-verts2d[i,0])
    
    # Last comparison for the final side that connects the 1st with the 3rd peak and it's slope
    if verts2d[2,1]<verts2d[0,1]:
        Ykmin[2] = verts2d[2,1]
        Xkmin[2] = verts2d[2,0]
        Ykmax[2] = verts2d[0,1]
        Xkmax[2] = verts2d[0,0]
        pairs[2][0] = 2
        pairs[2][1] = 0
    else:
        Ykmin[2] = verts2d[0,1]
        Xkmin[2] = verts2d[0,0]
        Ykmax[2] = verts2d[2,1]
        Xkmax[2] = verts2d[2,0]
        pairs[2][0] = 0
        pairs[2][1] = 2
    if (verts2d[2,0]-verts2d[0,0]) == 0:
        m[2] =np.inf
    else:
        m[2] = (verts2d[2,1]-verts2d[0,1])/(verts2d[2,0]-verts2d[0,0])

    # Find the Mininum and the Maximum of all peaks for all coordinates.
    Ymin = int(np.min(Ykmin))
    Ymax = int(np.max(verts2d[:,1]))
    Xmax = int(np.max(verts2d[:,0]))
    Xmin = int(np.min(verts2d[:,0]))

    for i in range(0, 3):
        c = vcolors[i,:]+c
    c = c/3

    if(Ymin == Ymax): # if triangle is a point or flat line
        if(all(Xkmax[:] == Xmax)):  # if triangle is a point
            Y[Ymin,Xmax,:] = c
        else:           # if triangle is a flat line
            for x in range(Xmin,Xmax+1):
                # Update active sides
                p=0
                for k in range(0,3):
                    Min = min(Xkmin[k],Xkmax[k])
                    Max = max(Xkmin[k],Xkmax[k])
                    if(x>= Min and x<Max): 
                        Xact2[p] = k
                        ActiveSides[k] = 1
                        p+=1
                    elif(x != Xmax):
                        ActiveSides[k] = 0
                if shade_t == "gouraud":
                    Y[Ymin,x,:] = interpolate_color(verts2d[Xact2[0],0],verts2d[Xact2[1],0],x,vcolors[Xact2[0],:],vcolors[Xact2[1],:])
                elif shade_t == "flat":
                    Y[Ymin,x,:] =  c[:]
                #Y[Ymin,x,:] = interpolate_color(verts2d[Xact2[0],0],verts2d[Xact2[1],0],x,vcolors[Xact2[0],:],vcolors[Xact2[1],:])
    else:
        # Here for y == Ymin we initialiaze the List with the Active Sides and points
        for k in range(0,3):
            if Ykmin[k] == Ymin and m[k] != 0:
                ActiveSides[k] = 1          # When the scanline cuts the side of the triangle # the list takes the value 1 otherwise it takes 0.
                Xk[k] = (Ymin - verts2d[k,1]) / m[k] + verts2d[k,0]     # Initialize active points

            if Ykmax[k] == Ymin:
                ActiveSides[k] = 0

        # For every scanline
        for y in range(Ymin,Ymax+1): 
            
            # Get active points for active sides rounded
            Xact = np.round(Xk[:])

            # Keep the error from rounding and correct when necessary
            for i in range(0,3):
                er[i] = er[i] + (Xk[i] - Xact[i])
                if (er[i] > 1):    
                    Xact[i] += 1
                    er[i] = 0
                if (er[i] < -1):
                    Xact[i] -= 1
                    er[i] = 0
            
            #if there isnt any active lines or all are active we are finished
            # When the last point-vertice is painted we have all 1's to painte the whole triangle
            if(all(ActiveSides[:]==0)):
                # print("all == 0")
                break
            if(all(ActiveSides[:]==1)):
                # print("all == 1")
                break

            #temp variable to correnctly index Xact points
            p=0
            for i in range(0,3):
                if(ActiveSides[i] == 1):
                    indexAct[p] = i
                    Xact2[p] = Xact[i]
                    p += 1

            # Find min and max of a line
            Xmin = int(min(Xact[ActiveSides[:]==1]))
            Xmax = int(max(Xact[ActiveSides[:]==1]))
            
            # x1,x2,x3,x4 are the vertices that our active points lie between and their respective colors C1,C2,C3,C4
            x1 = verts2d[pairs[indexAct[0],0],:]
            x2 = verts2d[pairs[indexAct[0],1],:]
            x3 = verts2d[pairs[indexAct[1],0],:]
            x4 = verts2d[pairs[indexAct[1],1],:]
            C1 = vcolors[pairs[indexAct[0],0],:]
            C2 = vcolors[pairs[indexAct[0],1],:]
            C3 = vcolors[pairs[indexAct[1],0],:]
            C4 = vcolors[pairs[indexAct[1],1],:]
            # Calculate the colors of the active points
            colorsXact[0] = interpolate_color(x1,x2,np.array([Xact2[0],y]),C1,C2)
            colorsXact[1] = interpolate_color(x3,x4,np.array([Xact2[1],y]),C3,C4)

            # temp variable to correnctly keep track of Xact (active points)
            cross_c=0;      
            for x in range(Xmin,Xmax+1):
                
                if(Xact2[0] == Xact2[1]):
                    if shade_t == "gouraud":
                        Y[y,x,:] = colorsXact[0]
                    elif shade_t == "flat":
                        Y[y,x,:] =  c[:]
                    break

                if(Xact2[0] == x):
                    if shade_t == "gouraud":
                        Y[y,x,:] = colorsXact[0]
                    elif shade_t == "flat":
                        Y[y,x,:] =  c[:]
                    cross_c=cross_c+1 # +1 if we meet a Active side
                elif(Xact2[1] == x):
                    if shade_t == "gouraud":
                        Y[y,x,:] = colorsXact[1]
                    elif shade_t == "flat":
                        Y[y,x,:] =  c[:]
                    cross_c=cross_c+1 # +1 if we meet a Active side
            
                if np.mod(cross_c,2) == 1:  # When cross_c is an odd number we are inside a triangle
                    if shade_t == "gouraud":
                        Y[y,x,:] = interpolate_color(Xact2[0],Xact2[1],x,colorsXact[0],colorsXact[1])
                    elif shade_t == "flat":
                        Y[y,x,:] =  c[:]
                    # Interpolate and paint if point is inside the triangle
                    #Y[y,x,:] = interpolate_color(Xact2[0],Xact2[1],x,colorsXact[0],colorsXact[1])

            # Update the active points with the correct gradient
            for k in range(0,3):
                if ActiveSides[k] == 1:  
                    if m[k] == np.inf:
                        Xk[k]=Xk[k]
                    if m[k] == 0:
                        Xk[k] += 1
                    else:
                        Xk[k] = Xk[k] + 1/m[k]

            for k in range(0,3):
                if Ykmin[k] == y+1 and m[k] != 0:
                    ActiveSides[k] = 1          # When the scanline cuts the side of the triangle
                    Xk[k] = (y+1 - verts2d[k,1]) / m[k] + verts2d[k,0]

                if (Ykmax[k] == y+1) and (y+1 != Ymax):
                    ActiveSides[k] = 0

    return Y