#----intepolate_colors------#
#   
# This function calculates the linear interpolation of the color of a point x between 2 points x1 and x2 given the colors of the the 2 points.
# Due to numpy library it can be used both if x1=(x,y), x2=(x,y) and if x1=(x), x2=(x).

import numpy as np

def interpolate_color(x1,x2,x,C1,C2):
    r1 = np.linalg.norm(x2 - x) 
    r2 = np.linalg.norm(x - x1) 
    percent = r1 / (r1 + r2)
    value = percent * C1 + (1 - percent) * C2
    return value