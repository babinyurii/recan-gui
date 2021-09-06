

import PySimpleGUI as sg

# Add a touch of color
sg.theme('DarkAmber')   

# All the stuff inside your window.
layout = [  [sg.Text("Choose your alignment: ")], 
             [sg.FileBrowse()], 
             [sg.Button("create plot")],
             [sg.Output(size=(100,50), key='-OUTPUT-')],
             [sg.MLine(key='-ML-', size=(600, 10))]
             #sg.Output(size=(400,400), key="-OUTPUTPLOT-")]
            ]

# Create the Window
window = sg.Window('recan', layout, resizable=True)



# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break
    elif event == "create plot":
        print(values)
        # we can split the path and give the file to the 
        print(type(values))
    

window.close()



