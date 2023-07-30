from convertor import PBR_Convertor as PBRC
import PySimpleGUI as sg
import os

input_dir="input"
    
output_dir="output"

#after commit path

def converter(input_dir,output_dir):
    import glob
    
    pattern = os.path.join(input_dir, f"*.texture_set.json")
    patterned_list=glob.glob(pattern)
    
    for file_path in patterned_list:
           
            convertor=PBRC.Be2Je(file_path)
            
            _,block_name=os.path.split(file_path)
            block_name=block_name.split('.')[0]
            
            temp_n=convertor.get_normal_ao_maps()
            
            temp_n.save(os.path.join(output_dir,block_name+"_n.png"))
                  
            temp_s=convertor.get_specular_maps()
            temp_s.save(os.path.join(output_dir,block_name+"_s.png"))
                
            print(os.path.join(output_dir,block_name+"_s.png"))
                    
            
converter(input_dir,output_dir)