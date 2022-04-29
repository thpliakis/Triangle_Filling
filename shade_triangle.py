import numpy as np
import matplotlib.pyplot as plt
import random   
import matplotlib.image as mpimg
from interpolate_color import *

def shade_triangle(img,verts2d,vcolors,shade_t):

    #   The image Y=img with  the triangles in which, every time the function is called, one triangle will be colored 
    # Initialization of the matrixes
    Y = img
    c = np.zeros((1,3))                 # Here the average color of a trinagle is stored for flat mode
    Ykmin = np.zeros((3,1))      
    Xkmin = np.zeros((3,1))
    m     = np.zeros((3,1))             # m is where the gradient of every side is stored
    Ykmax = np.zeros((3,1))
    Xkmax = np.zeros((3,1))
    Xk    = np.zeros((3,1)) 
    ActiveSides = np.zeros((3,1))       #If Activesides[i] == 1 the side is active
    Xact = np.zeros(2)                  #Here the x coordinate of the Active side is stored
  
    # Extra variables for shate_t = "gouraud"
    # Indexes of the active sides, to know which of the 3 are active
    index = np.array([0,1],dtype=int)   
    # The interpolated colors are saved here
    colorx = np.zeros((3,1))            
    colorsXact = np.zeros((2,3))
    C = np.ones((2,3))
    # In indexmin and indexman the vertices that every side is between are stored  
    indexmin = np.zeros(3,dtype=int)
    indexmax = np.zeros(3,dtype=int)

    # In this loop we compare the coordinate-Y of 2 peaks for every side and we
    # save the minimum value to Ykmin and at the same time 
    # the matching X to the array Xkmin, same with the max values.
    # In addition we find the slope of every side (m) and keep the indexmin,indexmax

    for i in range(0,2):
        if verts2d[i,1]<verts2d[i+1,1]:
            Ykmin[i] = verts2d[i,1]
            Xkmin[i] = verts2d[i,0]
            Ykmax[i] = verts2d[i+1,1]
            indexmin[i]=i
            indexmax[i]=i+1
            Xkmax[i] = verts2d[i+1,0]
        else:
            Ykmin[i] = verts2d[i+1,1]
            Xkmin[i] = verts2d[i+1,0]
            Ykmax[i] = verts2d[i,1]
            indexmin[i]=i+1
            indexmax[i]=i
            Xkmax[i] = verts2d[i,0]
        if (verts2d[i+1,0]-verts2d[i,0]) == 0:
            m[i] = np.inf
        else:
            m[i]=(verts2d[i+1,1]-verts2d[i,1])/(verts2d[i+1,0]-verts2d[i,0])
    
    # Last comparison for the final side that connects the 1st with the 3rd peak and it's slope
    if verts2d[2,1]<verts2d[0,1]:
        Ykmin[2] = verts2d[2,1]
        Xkmin[2] = verts2d[2,0]
        Ykmax[2] = verts2d[0,1]
        indexmin[2]=2
        indexmax[2]=0
        Xkmax[2] = verts2d[0,0]
    else:
        Ykmin[2] = verts2d[0,1]
        Xkmin[2] = verts2d[0,0]
        Ykmax[2] = verts2d[2,1]
        indexmin[2]=0
        indexmax[2]=2
        Xkmax[2] = verts2d[2,0]
    if (verts2d[2,0]-verts2d[0,0]) == 0:
        m[2] =np.inf
    else:
        m[2] = (verts2d[2,1]-verts2d[0,1])/(verts2d[2,0]-verts2d[0,0])

    # Find the Mininum and the Maximum of all peaks for all coordinates.
    Ymin = int(np.min(Ykmin))
    Ymax = int(np.max(verts2d[:,1]))
    Xmax = int(np.max(verts2d[:,0]))
    Xmin = int(np.min(verts2d[:,0]))    
    
    # Flat or Gouraud mode
    if shade_t == "flat":

        # The color of the triangle is the average of the colors of the 3 peaks
        for i in range(0, 3):
            c = vcolors[i,:]+c
        c = c/3

        # Here for y == Ymin we initialiaze the List with the Active Sides and points
        for k in range(0,3):

            if Ykmin[k] == Ymin:
                ActiveSides[k] = 1      # When the scanline cuts the side of the triangle
            else:                       # the list takes the value 1 otherwise it takes 0.
                ActiveSides[k] = 0
            
            if m[k]==0:                 # If there's horizontal line we disable the side
                ActiveSides[k] = 0
            elif m[k] == np.inf:
                if Ykmin[k] == Ymin:    # If the side is vertical and Ykmin[k] == Ymin then it is active
                    ActiveSides[k] = 1
                else:
                    ActiveSides[k] = 0

            # Initialize ActivePoints for y==ymin for each side
            Xk[k]=Xkmin[k]
        
        # Get active points for active sides
        Xact = np.round(Xk[ActiveSides==1])

        # For every scyline
        for y in range(Ymin,Ymax+1):           
            
            #if there aren't any active points break and finish painting
            if Xact.shape==(0,) or Xact.shape == (1,):
                break
            
            cross_c=0;         #a counter to show when we are inside the triangle and when outside 
            #For a vertical line from Xmin to Xmax
            for x in range(Xmin,Xmax+1):
        
                if x == Xact[0] or x == Xact[1]:
                    cross_c=cross_c+1             # +1 if we meet a Active side
        
                if not np.mod(cross_c,2) == 0:    # When cross_c is an even number we are inside a triangle
                    if x == Xact[0] or x==Xact[1]:
                        Y[y,x,:] = c[:]          # Paint if point is active
                    else:
                        Y[y,x,:] = c[:]          # Paint if point is inside the triangle
                        if Xact[0] == Xact[1]:      
                            cross_c=cross_c+1
                    
            # Update the active sides    
            for j in range(0,3):
                if y+1==Ykmin[j]:
                    ActiveSides[j] = 1
                
                if y+1>=Ykmax[j]:
                    ActiveSides[j] = 0

            # Update the active points with the correct gradient           
            for k in range(0,3):
                
                if ActiveSides[k] == 1:  
                    if m[k] == np.inf or m[k] == 0:
                        Xk[k]=Xk[k]
                    else:
                        Xk[k]=Xk[k]+1/m[k]  
        
            Xact = np.round(Xk[ActiveSides==1])   
        return Y #return imgage with a painted triangle

    elif shade_t == "gouraud" :
        
        # Here for y == Ymin we initialiaze the List with the Active Sides and points
        p = -1  #temp variable to correnctly take the colors for Xact (active points)
        for k in range(0,3):
        
            if Ykmin[k] == Ymin:
                ActiveSides[k] = 1      # When the scanline cuts the side of the triangle
            else:                       # the list takes the value 1 otherwise it takes 0.
                ActiveSides[k] = 0
            
            if m[k]==0:                 # If there's horizontal line we disable the side
                ActiveSides[k] = 0
                Xk[k] = Xkmin[k]
            elif m[k] == np.inf:
                Xk[k]=Xkmin[k]
                if Ykmin[k] == Ymin:     # If the side is vertical and Ykmin[k] == Ymin then it is active
                    ActiveSides[k] = 1
                else:
                    ActiveSides[k] = 0
            else:
                Xk[k]=Xkmin[k]

            if verts2d[k,1] == Ymin:     # take the colors for Xact (active points)
                p=p+1
                if not p==2: #If p==2 all vertices of a triangle are on th same vertical line and we have 3 active points
                    colorsXact[index[p],:] = vcolors[k,:]
                
        if p==2:        # If p==2 all vertices of a triangle are on th same vertical line and we have 3 active points
            Xact[0] = np.min(Xkmax)
            Xact[1] = np.max(Xkmax)
        else:
            Xact = np.round(Xk[ActiveSides==1])

        # For every scyline
        for y in range(Ymin,Ymax+1):    
            
            #if there aren't any active points break and finish painting
            if Xact.shape==(0,) or Xact.shape == (1,):
                break
            
            #a counter to show when we are inside the triangle and when outside 
            cross_c = 0
            p = 0  #temp variable to correnctly index Xact points
            #For a vertical line from Xmin to Xmax
            for x in range(Xmin,Xmax+1):
                
                if x == Xact[0] or x == Xact[1]:
                    cross_c=cross_c+1               # +1 if we meet a Active side

                if not np.mod(cross_c,2) == 0:      # When cross_c is an even number we are inside a triangle
                    if x == Xact[p]:                # Paint if point is active with interpolated color from the 2 vertices
                        Y[y,x,:] = colorsXact[index[p],:]
                        p=p+1
                    else:                           # Interpolate and aint if point is inside the triangle
                        colorx = interpolate_color(Xact[0],Xact[1],x,colorsXact[index[0],:],colorsXact[index[1],:])
                        Y[y,x,:]=colorx
                    
                    if Xact[0] == Xact[1]:
                        cross_c=cross_c+1         
            
            # Update the active sides    
            for j in range(0,3):
                if y+1==Ykmin[j]:
                    ActiveSides[j] = 1
                
                if y+1>=Ykmax[j]:
                    ActiveSides[j] = 0
            
            # temp variable to correnctly keep track of Xact (active points)
            counter = 0
            # Update the active points with the correct gradient and find their interpolated color    
            for k in range(0,3):
                
                if ActiveSides[k] == 1: 
                    
                    if m[k] == np.inf or m[k] == 0:
                        Xk[k]=Xk[k]
                    else:                    
                        Xk[k]=Xk[k]+1/m[k]
                        
                    colorsXact[counter,:] = interpolate_color(verts2d[indexmin[k]],verts2d[indexmax[k]],np.array([Xk[k,0],y]),vcolors[indexmin[k],:],vcolors[indexmax[k],:])
                    
                    Xact[counter] = np.round(Xk[k])
                    
                    if not counter == 2:    #If p==2 all vertices of a triangle are on th same vertical line and we have 3 active points
                        index[counter] = counter
                    counter=counter+1
        return Y    #return imgage with a painted triangle