from convertor import PBR_Convertor as PBRC
import PySimpleGUI as sg
import os

input_dir=""    
output_dir=""

#after commit path

def converter(input_dir,output_dir):
    import glob
    
    pattern = os.path.join(input_dir, f"*.texture_set.json")
    patterned_list=glob.glob(pattern)
    
    for file_path in patterned_list:
            block_name=file_path.split(".")[0]
            with open(file_path) as texture_sets_file:
                
                convertor=PBRC.Be2Je(texture_sets_file)
    
                try:
                    temp_n=convertor.get_normal_maps()
                    temp_n.save(os.join(output_dir,block_name+"_n.png"))
                    
                    temp_s=convertor.get_specular_maps()
                    temp_s.save(os.join(output_dir,block_name+"_s.png"))
                    
                except Exception as e:
                    pass
            