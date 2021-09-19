import PySimpleGUI as sg
from simgen import Simgen


sg.theme('DarkAmber')  


"""
    Embedding the Matplotlib toolbar into your application
"""

# ------------------------------- This is to include a matplotlib figure in a Tkinter canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


def draw_figure_w_toolbar(canvas, fig, canvas_toolbar):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    if canvas_toolbar.children:
        for child in canvas_toolbar.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    toolbar = Toolbar(figure_canvas_agg, canvas_toolbar)
    toolbar.update()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)

class Toolbar(NavigationToolbar2Tk):
    def __init__(self, *args, **kwargs):
        super(Toolbar, self).__init__(*args, **kwargs)


# ------------------------------- PySimpleGUI CODE

layout = [
    [sg.FileBrowse()], 
    
    [sg.Frame("list of sequences", [ [sg.T()] ], key="-list_of_seq-")],
    
    [sg.Text("sliding window size"), sg.Input()],
    [sg.Text("window shift (nuc)"), sg.Input()],
    [sg.Text("potential recombinant number"), sg.Input()],
    [sg.B('Plot')],
    [sg.T('Controls:')],
    [sg.Canvas(key='controls_cv')],
    [sg.Column(
        layout=[
            [sg.Canvas(key='fig_cv',
                       # it's important that you set this size
                       size=(400 * 2, 400)
                       )]
        ],
        background_color='#DAE0E6',
        pad=(0, 0)
    )],
    [sg.MLine(key='-ML-'+sg.WRITE_ONLY_KEY, size=(150, 10))]
]


window = sg.Window('6_simgen_separate', layout, resizable=True)

#output to multiline
print = lambda *args, **kwargs: window['-ML-'+ sg.WRITE_ONLY_KEY].print(*args, **kwargs)

while True:
    
    try: 
        event, values = window.read()
        print(event, values)
        if event in (sg.WIN_CLOSED, 'Exit'):  # always,  always give a way out!
            break
        elif event == 'Plot':
           
            # create sim obj which inherets from multiple alignment from biopython
            sim_obj = Simgen(values["Browse"])
            
            # #############################
            # RETRIEVE THE DATA FROM ALIGNMENT
            # get alignment length
            print("alignment length: ", sim_obj.get_alignment_length())
            ##################################
            # get seq ids
            counter = 0
            for record in sim_obj:
                print(record.id)
                counter += 1
            print("total number of seq in alignment: ", counter)
            
            #########################################################
            # ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE
            plt.close()
            plt.figure(1)
            fig = plt.gcf()
            DPI = fig.get_dpi()
            # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
            fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
            # -------------------------------
            
            # taking data from user input
            #sim_obj = Simgen(values["Browse"])
            sliding_window_size= int(values[0])
            window_shift = int(values[1])
            pot_rec_index = int(values[2])
            
            sim_obj.simgen(pot_rec=pot_rec_index, window=sliding_window_size, shift=window_shift)
            
            #x = np.linspace(0, 2 * np.pi)
            #y = np.sin(x)
            #plt.plot(x, y)
            plt.title("")
            plt.xlabel('alignment position')
            plt.ylabel('distance')
            plt.grid()
    
            # ------------------------------- Instead of plt.show()
            draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)
    except Exception as ex:
            print(ex, "\n", "-" * 50)

window.close()
