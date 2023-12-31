from math import sqrt
from PIL import Image
import os
import numpy as np
import json
from pylab import *
from scipy.ndimage import gaussian_filter


class Be2Je: # BedrockToJavaTextureConverter
    '''一个方块面的所有纹理(textureset以及对应的各种纹理),是一个待转换对象'''
    def __init__(self,textureSetPath:str):
        
        with open(textureSetPath) as textureSetFile:
                textureSet=json.load(textureSetFile)
                    
        pathPrefix=os.path.split(textureSetPath)[0]
        
        self.be_base_color=Image.open(os.path.join(pathPrefix,textureSet["minecraft:texture_set"]["color"]+".png"))
        
        self.be_pbr_mer_map=Image.open(os.path.join(pathPrefix,textureSet["minecraft:texture_set"]["metalness_emissive_roughness"]+".png"))
        
        try:
            self.be_heightmap=Image.open(os.path.join(pathPrefix,textureSet["minecraft:texture_set"]["heightmap"]+".png"))
        except Exception as e:
            self.be_normalmap=Image.open(os.path.join(pathPrefix,textureSet["minecraft:texture_set"]["normal"]+".png"))
          
        self.labPBR_specular= None
        self.labPBR_normal= None

        self.lightPos=np.array([3.0,4.0,5.0])
       
        
    
    def edit_light_position(self,x ,y,z):
        self.lightPos=np.array([x,y,z])
    
    
    def get_specular_maps(self):
        #Using *extra allows for the,, tuple splitedImage to be unpacked correctly, 
        #regardless of the number of elements it contains'''
        if self.labPBR_specular==None:
            
            be_metallic_map,be_emissive_map,be_roughness_map=self.be_pbr_mer_map.split();
            
            je_smoothness_map=Image.eval(be_roughness_map,lambda x:255*(1-sqrt(x/255)))
            je_base_reflectance_map= self.__calculate_f0(be_metallic_map) 
            
            #bedrock edition does not support subsurface_scatterin so i set it to a const value
            je_subsurface_scatterin_map=Image.eval(be_roughness_map,lambda X:X-X+5)
            je_emissive_map=Image.eval(be_emissive_map,lambda x:0.95*x)
            
            self.labPBR_specular=Image.merge('RGBA',(je_smoothness_map,je_base_reflectance_map,je_subsurface_scatterin_map,je_emissive_map))
            
        return self.labPBR_specular
                
    def __calculate_f0(self,metallic_map):
        
        gray_image=self.be_base_color.convert('L')
        
        image_size=gray_image.size
        image_width=image_size[0]
        image_height=image_size[1]
        gray_image_array=array(gray_image)
        
        matelic_map_array=array(metallic_map)
        je_F0_map=np.zeros((image_height,image_width))
           
        SpecularScale=0.5  #that tutorial said the default value is 0.5 but i do not know why
        DielectricSpecular = 0.08 * SpecularScale;
        
        for v in range(0,image_height-1):
            for u in range(0,image_width-1):
                je_F0_map[v][u] = 255*DielectricSpecular * (255 - matelic_map_array[v][u]) + 255*(gray_image_array[v][u] * matelic_map_array[v][u])
               
        return Image.fromarray(je_F0_map,mode="L")


    def get_normal_ao_maps(self):
        if self.labPBR_normal == None:
            normalmaps=self.__calculate_normal()
            
            normalmaps_normalize = np.array(normalmaps)
            normalmaps_normalize = (normalmaps_normalize/128-1)
            
            normalmapslist=normalmaps.split()
            AOmap=self.__calculate_ao(normalmaps_normalize)
            
            self.labPBR_normal=Image.merge('RGBA',(normalmapslist[0],normalmapslist[1],AOmap,self.be_heightmap))
        
        return self.labPBR_normal
        
        
    
    def __calculate_normal(self,strength=0):
        '''accecpt an be_heightmap,the strength para determined the strength of normal'''
        
        image_width,image_height=self.be_heightmap.size #create vector
        be_heightmap_array=np.array(self.be_heightmap)
        je_n_map_array=np.zeros((image_height,image_width,4), dtype=np.uint8)#分别为法线的xy[对应RG](另外的分量通过模长为1计算出来)和B—AO和alpha-heightmap
        x_tangent_vector_martrix=np.zeros((image_height,image_width,3), dtype=np.float16)
        y_tangent_vector_martrix= np.zeros((image_height,image_width,3), dtype=np.float16)
        
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
                
                normal_vector_martrix[u,v]=normal_vector_martrix[u,v]/np.linalg.norm(normal_vector_martrix[u,v]) #norlmalize vector
               
                je_n_map_array[u,v,:3]=((normal_vector_martrix[u,v,:3]+1)*128)  #valued normal to je_n_map_array
                
                
        
        return Image.fromarray(je_n_map_array)


    def __calculate_ao(self,normals:np.ndarray,intensity=1.0, radius=1.0):
        '''Calculate   '''
        # 计算光源相对于高度图中每个点的方向
        light_dir = self.lightPos - normals[:,:,:3]
        light_dir /= np.linalg.norm(light_dir) #归一化
        
        #print("\nlight_dir",light_dir)
        # 计算法线和光照方向的点积
        ao_map_array = ( 
                        (normals[:,:,:3] * light_dir)**intensity /
                        np.linalg.norm((normals[:,:,:3] * light_dir)**intensity) )
        
        # 应用环境光遮蔽效果
        #print("\nao_map",ao_map_array)
        # 使用高斯滤波器模糊结果，模拟软阴影效果
        ao_map_array = gaussian_filter(ao_map_array, radius)
        
        #print("\nao_map",ao_map_array)
        ao_map=Image.fromarray(((ao_map_array+1)*128).astype(np.int8),mode='RGB').convert('L')
               
        return ao_map
    
    