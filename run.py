from convertor import PBR_Convertor as PBRC

import PySimpleGUI as sg

input_dir=""    
output_dir=""



temp_n="image"
temp_s="image"


import PySimpleGUI as sg

# 定义布局
layout = [
    [sg.Text('欢迎使用PySimpleGUI示例')],
    [sg.InputText()],
    [sg.Button('OK'), sg.Button('取消')]
]

# 创建窗口
window = sg.Window('示例窗口', layout)

# 事件循环
while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, '取消'):
        break
    if event == 'OK':
        input_text = values[0]
        sg.popup(f'您输入的内容是：{input_text}')

# 关闭窗口
window.close()

#after commit path
''' for f in input_dir:
    if f.name=="json的textture_set":
        
        json_path="prefix"+f.name
        with open(json_path) as texture_sets_file:
            convertor=PBRC.Be2Je(texture_sets_file)
            try:
                temp_n=convertor.get_normal_maps()
                temp_s=convertor.get_specular_maps()
            except Exception as e:
                pass
         '''