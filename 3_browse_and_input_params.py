from simgen import Simgen
import PySimpleGUI as sg

# Add a touch of color
sg.theme('DarkAmber')   

# All the stuff inside your window.
layout = [  [sg.Text("Choose your alignment: ")], 
             [sg.FileBrowse()],
             [sg.Text("window"), sg.Input()],
             [sg.Text("step"), sg.Input()],
             
             [sg.Button("create plot")],
             [sg.Output(size=(100,50), key='-OUTPUT-')],
             [sg.MLine(key='-ML-'+sg.WRITE_ONLY_KEY, size=(600, 10))]
            ]

# Create the Window
window = sg.Window('recan', layout, resizable=True)

#output to multiline
print = lambda *args, **kwargs: window['-ML-'+ sg.WRITE_ONLY_KEY].print(*args, **kwargs)




# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED: # if user closes window or clicks cancel
        break
    
    
    elif event == "create plot":
        print(values)
        print(values["Browse"])
        
        sim_obj = Simgen(values["Browse"])
        print(sim_obj)
        
        #print(sim_obj.get_info())
        
        
    
    
    
    
    
    
    
    

window.close()




