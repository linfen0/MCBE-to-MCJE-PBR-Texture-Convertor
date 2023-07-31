from convertor import PBR_Convertor as PBRC
import PySimpleGUI as sg
import os

def converter(files_number,process_folder,output_dir):
    layout = [
          [sg.Text("Converting")]
          [sg.ProgressBar(files_number, orientation='h', size=(20, 20), key='progressbar'),sg.Text(key="file_name")],
          [sg.Cancel("interupt")]
              ]
    window=sg.Window("Converting",layout)
    text=window["file_name"]
    progress_bar = window['progressbar']
    
    faild_list=[]
    
    for file_path in process_folder:
        processed_num=0
        try:
            convertor=PBRC.Be2Je(file_path)
            
            _,block_name=os.path.split(file_path)
            block_name=block_name.split('.')[0]
            
            temp_n=convertor.get_normal_ao_maps()
            
            temp_n.save(os.path.join(output_dir,block_name+"_n.png"))
            print(os.path.join(output_dir,block_name+"_n.png","converted"))
                  
            temp_s=convertor.get_specular_maps()
            temp_s.save(os.path.join(output_dir,block_name+"_s.png"))
                
            print(os.path.join(output_dir,block_name+"_s.png","converted"))
            
            text.update(file_path)
            processed_num+=1
            progress_bar.UpdateBar(processed_num)
           
        except Exception as e:
            faild_list.append(file_path)
        
        
    if len(faild_list)!=0:
        sg.popup("File belowed faild to convert !"+faild_list,no_titleba=True)
        import json
        

layout = [
              [sg.Input("Enter bedrock 'Blocks' folder",key='input'),sg.FolderBrowse(key='_BUTTON_KEY_',target='input')],
              [sg.Input("Enter output folder",key='output'),sg.FolderBrowse(key='_BUTTON_KEY_',target='output')],
              [sg.OK("Convert !",size=(40,2),pad=(40,0))]
              
              ]
window=sg.Window("MCBE2 MCJE",layout)
while True:
    event,value=window.read() #value is a directory that every elememt-value pairs was included when specific event occured
    if event=="Convert !" :
        import glob
    
        pattern = os.path.join(value["input"], f"*.texture_set.json")
        patterned_list=glob.glob(pattern)
        
        files_num=len(patterned_list)
        if files_num==0:
            sg.popup("Found no .textture_set.json file at that folder!")
        else:
            converter(files_num,patterned_list,value["output"])
            pass
        
    if event== None or event== sg.WINDOW_CLOSED:
        break
    
    #converter(input_dir,output_dir)