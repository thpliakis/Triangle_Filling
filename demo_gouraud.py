import numpy as np
from render import *
import matplotlib

# Load data
data = np.load("hw1.npy", allow_pickle=True)
verts2d = data[()]['verts2d']
vcolors = data[()]['vcolors']
faces = data[()]['faces']
depth = data[()]['depth']

# Start painting :)
shade_t = "gouraud"
X = render(verts2d,faces,vcolors,depth,shade_t)
imgplot = plt.imshow(X)
matplotlib.image.imsave('gouraud.png', X)
plt.show()