from math import sqrt
from PIL import Image
import os
import numpy as np
import json
from pylab import *
from scipy.ndimage import gaussian_filter
#由于python的变量均是通过引用的方式进行传递的,所以可以随意"赋值"
input_filePath="D:/Code resource/Python/image cover/preconver/"
output_filePath="D:/Code resource/Python/image cover/convered/"
fileList = os.listdir(input_filePath)
#一个方块面的所有纹理(textureset以及对应的各种纹理),是一个待转换对象
class Be2Je:
    ''''''
    def __init__(self,textureSetPath:json):
            textureSet=json.load(textureSetPath)
            self.be_base_color_map=textureSet["minecraft:texture_set"].color
            self.be_pbr_mer_map=textureSet["minecraft:texture_set"].mer
            
            try:
                self.be_heightmap=textureSet["minecraft:texture_set"].heightmap
            except Exception as e:
                self.be_normalmap=textureSet["minecraft:texture_set"].normal
                
            self.image=None
            self.labPBR_smoothness=None
            self.labPBR_specular= self.BePbr2Specular()
            self.labPBR_normal=None

            
    def __F0calculator(be_base_color,be_metallic_map):
        gray_image=be_base_color
        image_size=gray_image.size()
        image_width=image_size[1]
        image_height=image_size[0]
        gray_image_array=array(gray_image)
        matelic_map_array=array(be_metallic_map)
        je_F0_map=np.zeros((image_height,image_width))
        #that tutorial said the default value is 0.5 but i do not know why
        SpecularScale=0.5
        DielectricSpecular = 0.08 * SpecularScale;
        for v in range(0,image_height-1):
            for u in range(0,image_width-1):
                je_F0_map[v][u] = 255*DielectricSpecular * (255 - matelic_map_array[v][u]) + 255*(gray_image_array[v][u] * matelic_map_array[v][u])
        return Image.fromarray(je_F0_map,mode="L")

    def BePbr2Specular(self,be_base_color,be_pbr_mer):
        #Using *extra allows for the tuple splitedImage to be unpacked correctly, 
        #regardless of the number of elements it contains'''
        be_base_color=be_base_color
        be_metallic_map,be_emissive_map,be_roughness_map=Image.split(be_pbr_mer);
        
        self.je_smoothness_map=Image.eval(be_roughness_map,lambda x:255*(1-sqrt(x/255)))
        self.je_base_reflectance_map= self.__F0calculator(be_base_color,be_metallic_map) 
        #bedrock edition does not support subsurface_scatterin so i set it to a const value
        self.je_subsurface_scatterin_map=Image.eval(be_roughness_map,lambda X:X-X+5)
        self.je_emissive_map=Image.eval(be_emissive_map,lambda x:0.95*x)
        
        self.labPBR_specular=Image.merge('RGBA',(self.je_smoothness_map,self.je_base_reflectance_map,self.je_subsurface_scatterin_map,self.je_emissive_map))
        return 1 
    
    def __mergeNormal():
        pass
    
    def BeHeightmap2Normal(be_heightmap,strength=0):
        '''accecpt an be_heightmap,the strength para determined the strength of normal'''
        image_height,image_width=be_heightmap.size()
        be_heightmap_array=np.array(be_heightmap)
        je_n_map_array=np.zeros((image_height,image_width,4), dtype=np.uint8)#分别为法线的xy[对应RG](另外的分量通过模长为1计算出来)和B—AO和alpha-heightmap
        x_tangent_vector_martrix=np.zeros((image_height,image_width,3), dtype=np.float32)
        y_tangent_vector_martrix= np.zeros((image_height,image_width,3), dtype=np.float32)
        #init obove vector
        x_tangent_vector_martrix[:,:,1]=1
        y_tangent_vector_martrix[:,:,0]=1
        #process non-edge pixel
        x_tangent_vector_martrix[:,1:-1,2]=(be_heightmap_array[:,2:]/255 - be_heightmap_array[:,:-2]/255) / min(100.0,max(1,100-strength))#dz/dx
        y_tangent_vector_martrix[1:-1,:,2]=(be_heightmap_array[2:,:]/255 - be_heightmap_array[:-2,:]/255) / min(100.0,max(1,100-strength))#dz/dy
        #process edge
        #leftANDRight
        x_tangent_vector_martrix[:,0,2]=(be_heightmap_array[:,1]/255 - be_heightmap_array[:,0]/255) / min(100.0,max(1,100-strength))
        x_tangent_vector_martrix[:,-1,2]=(be_heightmap_array[:,-1]/255 - be_heightmap_array[:,-2]/255) / min(100.0,max(1,100-strength))
        #topANDbottom
        y_tangent_vector_martrix[0,:,2]=(be_heightmap_array[1,:]/255 - be_heightmap_array[0,:]/255) / min(100.0,max(1,100-strength))
        y_tangent_vector_martrix[-1,:,2]=(be_heightmap_array[-1,:]/255 - be_heightmap_array[-2,:]/255) / min(100.0,max(1,100-strength))
        normal_vector_martrix=np.cross(y_tangent_vector_martrix[:,:],x_tangent_vector_martrix[:,:])
          
        for v in range(image_width):
            for u in range(image_height):
                #norlmalize vector
                normal_vector_martrix[u,v]=normal_vector_martrix[u,v]/np.linalg.norm(normal_vector_martrix[u,v])
                #valued normal to je_n_map_array
                je_n_map_array[u,v,:2]=((normal_vector_martrix[u,v,:2]+1)*128)
                #valued heightmap to je_n_map Alpha channel
                je_n_map_array[u,v,3]=be_heightmap[u,v]
        
        return je_n_map_array


def BeheightMap2AO(self,height_map, light_pos, scale=1.0, intensity=1.0, radius=1.0):
    '''投影法计算阴影方向/长度'''
    # 从高度图计算法线图
    normals = self.BeHeightmap2Normal(height_map)
    
    # 计算光源相对于高度图中每个点的方向
    light_dir = light_pos - np.indices(normals.shape[:2]).transpose((1, 2, 0))
    light_dir /= np.sqrt(np.sum(light_dir**2, axis=2))[..., np.newaxis]
    
    # 计算法线和光照方向的点积
    dot_product = np.sum(normals * light_dir, axis=2)
    
    # 应用环境光遮蔽效果
    ao_map = np.clip(dot_product, 0, 1)**intensity
    
    # 使用高斯滤波器模糊结果，模拟软阴影效果
    ao_map = gaussian_filter(ao_map, radius)
    
    return ao_map
 
        