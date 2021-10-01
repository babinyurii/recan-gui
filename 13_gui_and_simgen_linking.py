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
    [sg.FileBrowse(), sg.Button("get seq names", key="-get_seq_names-")], 
    
    [sg.Frame("list of sequences", [ [sg.T()] ], key="-list_of_seq-")],
    
    [sg.Text("sliding window size"), sg.Input()],
    [sg.Text("window shift (nuc)"), sg.Input()],
    [sg.Text("potential recombinant number"), sg.Input()],
    [sg.Button('Plot', key="-plot-")],
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


window = sg.Window('13', layout, resizable=True)
#output to multiline
#print = lambda *args, **kwargs: window['-ML-'+ sg.WRITE_ONLY_KEY].print(*args, **kwargs)


sequences_added = False # if data are retrieved from file path
seq_names = [] # to store ids of sequences to show them in the gui
sequences_to_draw = [] # sequences to plot
checkboxes_and_radiobuttons = [] # stores checkboxes and radiobuttons keys
pot_rec_index = None

def get_checkboxes_and_radiobuttons(values):
    
    for key in values.keys():
        if type(key) == str:
            if key.endswith("checkbox") or key.endswith("radio"):
                checkboxes_and_radiobuttons.append(key) 
    return checkboxes_and_radiobuttons



def get_pot_rec_id(checkboxes_and_radiobuttons, values):
    for seq_id in checkboxes_and_radiobuttons:
        if seq_id.endswith("radio"):
            if values[seq_id]:
                pot_rec_index = int(seq_id.rsplit("_", maxsplit=2)[1])
                pot_rec_id = seq_id.rsplit("_", maxsplit=2)[0]
                
                break
    return pot_rec_index, pot_rec_id



def get_seq_ids_to_draw(checkboxes_and_radiobuttons, values, sequences_to_draw):
    
    #for seq_id in checkboxes_and_radiobuttons:
    #    if seq_id.endswith("radio"):
    #        if values[seq_id]:
    #            sequences_to_draw.append(seq_id.rsplit("_", maxsplit=2)[0])
    #            break

    # 
    for seq_id in checkboxes_and_radiobuttons:
        if seq_id.endswith("checkbox"):
            if values[seq_id]:
                sequences_to_draw.append(seq_id.rsplit("_", maxsplit=2)[0])
       
            
    return sequences_to_draw


while True:
        
#try: 
    event, values = window.read()
    sim_obj = Simgen(values["Browse"])
    print(event, values)
    print("sim_obj:", sim_obj)
    if event in (sg.WIN_CLOSED, 'Exit'):  # always,  always give a way out!
        break
    
    elif event == "-get_seq_names-":
        # create sim obj which inherets from multiple alignment from biopython
        
        
        # #############################
        # RETRIEVE THE DATA FROM ALIGNMENT
        # get alignment length
        counter = 0
        for record in sim_obj:
            seq_names.append(record.id + "_" + str(counter))
            counter += 1
        print("total number of seq in alignment: ", counter)
        print("alignment length: ", sim_obj.get_alignment_length())
        
        if not sequences_added:
            for seq_id in seq_names:
                window.extend_layout(window['-list_of_seq-'], 
                                     [[sg.Radio("", 
                                                group_id="-potential_recombinant-", 
                                                key=seq_id + "_radio"), 
                                                                                                                                
                                       sg.Checkbox("", key=seq_id + "_checkbox"), 
                                       sg.Text(seq_id)]])
            sequences_added = True       
        print(event, values)
        print("sequences added: ", sequences_added)
        
        
        
    elif event == '-plot-':
        #potential_recombinant = None
        checkboxes_and_radiobuttons = [] # stores checkboxes and radiobuttons keys
        sequences_to_draw = [] # sequences to plot

        
        checkboxes_and_radiobuttons = get_checkboxes_and_radiobuttons(values)
        print("checkboxes and radiobuttons:")
        for i in checkboxes_and_radiobuttons:
            print(i)
        print("-" * 20)
            
        sequences_to_draw = get_seq_ids_to_draw(checkboxes_and_radiobuttons, values, 
                                                sequences_to_draw)
        print("sequences to draw: ")
        for i in sequences_to_draw:
            print(i)
        print("-" * 20)
        
        pot_rec_index, pot_rec_id = get_pot_rec_id(checkboxes_and_radiobuttons, values)
        print("potential recombinant: {0}, {1}\n".format( pot_rec_index, pot_rec_id))
        print("-" * 20)
        
        
       
        #########################################################
        # ------------------------------- PASTE YOUR MATPLOTLIB CODE HERE
        plt.close()
        plt.figure(1)
        fig = plt.gcf()
        DPI = fig.get_dpi()
        # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
        fig.set_size_inches(404 * 2 / float(DPI), 404 / float(DPI))
        # -------------------------------
        
        #sim_obj = Simgen(values["Browse"])
        sliding_window_size = int(values[0])
        window_shift = int(values[1])
        #pot_rec_index = int(values[2])
        
        
        sim_obj.simgen(pot_rec=pot_rec_index, 
                       seq_to_draw=sequences_to_draw,
                       pot_rec_id=pot_rec_id,
                       window=sliding_window_size, 
                       shift=window_shift,
                       region=False,
                       dist="pdist")
    
        plt.title("")
        plt.xlabel('alignment position')
        plt.ylabel('distance')
        plt.grid()

        # ------------------------------- Instead of plt.show()
        draw_figure_w_toolbar(window['fig_cv'].TKCanvas, fig, window['controls_cv'].TKCanvas)


#except Exception as ex:
       # print("exception : ", ex, "\n", "-" * 50)


window.close()



#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 15:54:44 2021

@author: babin
"""

