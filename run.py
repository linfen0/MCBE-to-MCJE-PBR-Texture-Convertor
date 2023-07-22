from Convertor import PBR_Convertor as PBRC
import PySimpleGUI as sg

layout = [[sg.Text('A custom progress meter')],
          [sg.ProgressBar(1000, orientation='h', size=(20, 20), key='progressbar')],
          [sg.Cancel()]]

window = sg.Window('Custom Progress Meter', layout)
progress_bar = window['progressbar']
# loop that would normally do something useful
for i in range(1000):
    # check to see if the cancel button was clicked and exit loop if clicked
    event, values = window.read(timeout=10)
    if event == 'Cancel'  or event is None:
        break
  # update bar with loop value +1 so that bar eventually reaches the maximum
    progress_bar.UpdateBar(i + 1)
# done with loop... need to destroy the window as it's still open
window.close()


window = sg.Window("Windows-like program",layout)
window.disappear() # 窗口隐藏
window.reappear() # 窗口展示
window = sg.Window('My window with tabs', layout, font=("宋体", 15),default_element_size=(50,1)) 


