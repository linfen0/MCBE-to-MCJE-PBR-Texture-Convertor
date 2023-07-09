from math import sqrt
from PIL import Image
import os
import numpy
import json
from pylab import *
image_height,image_width=(8,8)
be_heightmap_array=np.arange(0,640,step=10)
#print(be_heightmap_array)
strength=100
be_heightmap_array=be_heightmap_array.reshape(image_height,image_width)
print(be_heightmap_array)
je_n_map_array=np.zeros((image_height,image_width,4), dtype=np.uint8)#分别为法线的xy[对应RG](另外的分量通过模长为1计算出来)和B—AO和alpha-heightmap
x_tangent_vector_martrix=np.zeros((image_height,image_width,3), dtype=np.float32)
y_tangent_vector_martrix= np.zeros((image_height,image_width,3), dtype=np.float32)
#init obove vector
x_tangent_vector_martrix[:,:,1]=1
y_tangent_vector_martrix[:,:,0]=1
#process non-edge pixel
x_tangent_vector_martrix[:,1:-1,2]=(be_heightmap_array[:,2:]/255 - be_heightmap_array[:,:-2]/255) / min(100.0,max(1,100-strength))
y_tangent_vector_martrix[1:-1,:,2]=(be_heightmap_array[2:,:]/255 - be_heightmap_array[:-2,:]/255) / min(100.0,max(1,100-strength))
#print(y_tangent_vector_martrix,x_tangent_vector_martrix)0
#process edge
#leftANDRight
x_tangent_vector_martrix[:,0,2]=(be_heightmap_array[:,1]/255 - be_heightmap_array[:,0]/255) / min(100.0,max(1,100-strength))
x_tangent_vector_martrix[:,-1,2]=(be_heightmap_array[:,-1]/255 - be_heightmap_array[:,-2]/255) / min(100.0,max(1,100-strength))
#topANDbottom
y_tangent_vector_martrix[0,:,2]=(be_heightmap_array[1,:]/255 - be_heightmap_array[0,:]/255) / min(100.0,max(1,100-strength))
y_tangent_vector_martrix[-1,:,2]=(be_heightmap_array[-1,:]/255 - be_heightmap_array[-2,:]/255) / min(100.0,max(1,100-strength))
#

normal_vector_martrix=np.cross(y_tangent_vector_martrix[:,:],x_tangent_vector_martrix[:,:])
print(normal_vector_martrix)
for v in range(image_width):
    for u in range(image_height):
        normal_vector_martrix[u,v]=normal_vector_martrix[u,v]/np.linalg.norm(normal_vector_martrix[u,v])
        print(normal_vector_martrix[u,v,0]**2+normal_vector_martrix[u,v,1]**2+normal_vector_martrix[u,v,2]**2)
#print(normal_vector_martrix)