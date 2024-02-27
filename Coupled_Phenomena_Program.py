## SATELLITE VISUALIZER
# V5.0
# João Bispo, Sara Sousa, Francisca Branco, Diogo Pereira, Tomás Pinho, Joao Rodrigues, Catarina Sá, João Francisco Brazão, M.ª Eduarda Carvalho, Vasco Lopes
# 7-1-2023
# A satellite visualization tool that establishes a correspondence between a satellite's pitch-roll-yaw stability and its' moments of inertia
# Input: moments of inertia or stability region. Output: image, stability region or moments of inertia 
# This program requires tkinter, PIL, sympy, numpy, matplotlib and Poly3DCollection
# Python 3

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from sympy import *
import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# OOP, create Satellite class for an object
class Satellite: 
    
    def __init__(self):

        self.Ix = None
        self.Iy = None
        self.Iz = None
        self.Rx = None
        self.Ry = None
        self.Rz = None

# Function to make the main menu work
def control_function(case, main_window):
    global control
    if case == 1:
        control = True
        main_window.destroy()
    elif case == 2:
        control = False
        main_window.destroy()

# Function to go back to main menu
def break_function(window):
    global main_window, control, stability_value, canvas, boolean
    window.destroy()
    control = None
    stability_value = None
    canvas = None
    boolean = None
    
# Function to quit the program
def quit_program(window):
    global program
    program = False
    break_function(window)
    return None

# Function to get the inertia moments from user input
def get_inertia_moments():

    global sat

    sat.Ix = float(entry1.get())
    sat.Iy = float(entry2.get())
    sat.Iz = float(entry3.get())

# Function to get the inertia moment for use in the Design Satellite Window computations
def get_inertia_moments_2():

    global sat2

    #Reset the moments of inertia. This happens so that we can delete the previous user input and correct a bug.
    sat2.Ix = ""
    sat2.Iy = ""
    sat2.Iz = ""

    if entry1.get() != "": # Find out which I parameter was input by the user
        sat2.Ix = float(entry1.get())
        sat2.Iy = None
        sat2.Iz = None
    elif entry2.get() != "":
        sat2.Iy = float(entry2.get())
        sat2.Ix = None
        sat2.Iz = None
    elif entry3.get() != "":
        sat2.Iz = float(entry3.get())
        sat2.Iy = None
        sat2.Ix = None
    else:
        print('ERROR')

#Check the stability of the satellite
def check_stability():

    global sat, stability_value, boolean

    if sat.Rx >= sat.Ry and (3*sat.Rx + sat.Rx*sat.Ry + 1)**2 >= 16*sat.Rx*sat.Ry and -1<sat.Rx<1 and -1<sat.Ry<1 and sat.Rx*sat.Ry >=0:
        stability_value.set('Satellite is Stable.')
        boolean = True
    else:
        stability_value.set('Satellite is not Stable.')
        boolean = False

# Function to compute the inertia functions
def compute_inertia_functions():
    global sat

    sat.Rx = (sat.Iz - sat.Iy) / sat.Ix
    sat.Ry = (sat.Iz - sat.Ix) / sat.Iy
    sat.Rz = (sat.Ix - sat.Iy) / sat.Iz

    Rx_label.config(text=f"Rx: {sat.Rx}")
    Ry_label.config(text=f"Ry: {sat.Ry}")
    Rz_label.config(text=f"Rz: {sat.Rz}")

# Function to compute the inertia moments from the inertia functions Rx and Ry
def compute_inertia_moments_2():
    global sat2

    Ix, Iy, Iz = symbols('Ix Iy Iz') # Declaring the necessary symbols, according to sympy

    # Next, we have 3 different cases, according to which moment of inertia was input by the user
    if sat2.Ix != None and sat2.Iy == None and sat2.Iz == None:
        equation1 = Eq((Iz - Iy)/sat2.Ix - sat2.Rx, 0)
        equation2 = Eq((Iz - sat2.Ix)/Iy - sat2.Ry, 0)
        equation3 = Eq((sat2.Ix - Iy)/Iz - sat2.Rz, 0)

        solution = solve((equation1, equation2), (Iy, Iz)) # Solve the equation and pass the values to the satellite
        sat2.Iy = solution[Iy]
        sat2.Iz = solution[Iz]
    
    elif sat2.Iy != None and sat2.Ix == None and sat2.Iz == None:
        equation1 = Eq((Iz - sat2.Iy)/Ix - sat2.Rx, 0)
        equation2 = Eq((Iz - Ix)/sat2.Iy - sat2.Ry, 0)
        equation3 = Eq((Ix - sat2.Iy)/Iz - sat2.Rz, 0)

        solution = solve((equation1, equation2), (Ix, Iz)) # Solve the equation and pass the values to the satellite
        sat2.Ix = solution[Ix]
        sat2.Iz = solution[Iz]

    elif sat2.Iz != None and sat2.Ix == None and sat2.Iy == None:
        equation1 = Eq((sat2.Iz - Iy)/Ix - sat2.Rx, 0)
        equation2 = Eq((sat2.Iz - Ix)/Iy - sat2.Ry, 0)
        equation3 = Eq((Ix - Iy)/sat2.Iz - sat2.Rz, 0)

        solution = solve((equation1, equation2), (Ix, Iy)) # Solve the equation and pass the values to the satellite
        sat2.Ix = solution[Ix]
        sat2.Iy = solution[Iy]

    Ix2_label.config(text=f"Ix: {sat2.Ix}")
    Iy2_label.config(text=f"Iy: {sat2.Iy}")
    Iz2_label.config(text=f"Iz: {sat2.Iz}")

# Function to draw the stability point on the Rx/Ry graph
def draw_point():

    global sat, canvas

    #Delete any previous point, if necessary
    if canvas is not None:
        canvas.destroy()

    # Set the canvas size
    canvas = tk.Canvas(window, width=300, height=300, highlightthickness=0)
    canvas.place(x=(325*sat.Rx+550.5), y=(-332*sat.Ry+385))
    canvas_width = 10
    canvas_height = 10
    canvas.config(width=canvas_width, height=canvas_height)

    # Calculate the canvas coordinates based on the graph coordinates
    canvas_x = canvas.winfo_reqwidth() / 2 + (canvas.winfo_reqwidth() / 2)
    canvas_y = canvas.winfo_reqheight() / 2 - (canvas.winfo_reqheight() / 2)

    # Draw a small circle (oval) at the specified canvas coordinates
    canvas.create_oval(canvas_x - 300, canvas_y - 300, canvas_x + 300, canvas_y + 300, fill="red", outline="red")

# Function to draw the main paralelipiped body of the satellite on matplotlib
def draw_sat_body(ax,point,dimensions,color):
    dimensions = np.array(dimensions)
    point = np.array(point)
    x_len,y_len,z_len = dimensions
    v = [point + (-x_len/2,y_len/2,0),point + (x_len/2,y_len/2,0),point + (x_len/2,-y_len/2,0),point + (-x_len/2,-y_len/2,0),
         point + (-x_len/2,y_len/2,z_len),point + (x_len/2,y_len/2,z_len),point + (x_len/2,-y_len/2,z_len),point + (-x_len/2,-y_len/2,z_len)
    ]
    faces = [ 
        [v[0],v[1],v[2],v[3]],
        [v[0],v[1],v[5],v[4]],
        [v[6],v[7],v[3],v[2]],
        [v[4],v[5],v[6],v[7]],
        [v[0],v[3],v[7],v[4]],
        [v[1],v[2],v[6],v[5]]
    ]
    box = Poly3DCollection(verts = faces,facecolors = color)
    ax.add_collection3d(box)

# Function to draw the satellite dish on matplotlib
def draw_sat_dish_surface(ax,center, radius,color):
    theta = np.linspace(0,np.pi/2,num = 100)
    phi = np.linspace(0,2*np.pi,num=100)
    theta,phi = np.meshgrid(theta,phi)
    x = center[0] + radius*np.sin(theta)*np.cos(phi)
    y = center[1] + radius*np.sin(theta)*np.sin(phi)
    z = center[2] + radius*np.cos(theta)
    ax.plot_surface(x , y , z ,color = color)

# Function that calls previous draw functions to draw the 3d representation of the satellite
def draw_sat():
    global fig
    # Create a 3D axis
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    fig.set_facecolor("black")
    ax.set_facecolor("black")
    plt.axis('off')

    sat_color = "gray"
    # satellite body with dimensions 3x9x1
    if sat_mode == "LAM":
        draw_sat_body(ax,point = (0,0,2), dimensions = (3,1,9), color = sat_color)
    elif sat_mode == "SAM":
        draw_sat_body(ax,point = (0,0,2), dimensions = (9,3,1), color = sat_color)
    elif sat_mode == "AXI_LAM":
        draw_sat_body(ax,point = (0,0,2), dimensions = (3,3,9), color = sat_color)
    elif sat_mode == "AXI_SAM":
        draw_sat_body(ax,point = (0,0,2), dimensions = (3,3,1), color = sat_color)
    # satellite dish
    draw_sat_dish_surface(ax, center = (0, 0, 0), radius = 2, color = sat_color)

    # orbit line
    x = np.linspace(-100,100,100)
    y = np.zeros(100)
    z = [2.5]*100
    ax.plot(x,y,z,linestyle = "--",color = "white")

    # Set axis limits
    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])
    ax.set_zlim([-4, 12])

# Fucntion to save the matplotlib plot in png format
def plot_matplotlib_figure():
    fig = draw_sat() 
    current_path = os.getcwd()
    sat_disp_name = "satellite_display.png"
    plt.savefig(sat_disp_name,transparent=False)
    sat_disp_path = os.path.join(current_path,sat_disp_name)
    sat_disp = Image.open(sat_disp_path)
    # cropping the png file
    width,height = sat_disp.size
    left = 140
    top = 0
    right = 660
    bottom = 600
    sat_disp_crop = sat_disp.crop((left,top,right,bottom))
    # displaying the photo
    sat_disp_photo = ImageTk.PhotoImage(sat_disp_crop)
    sat_disp_label = tk.Label(window,image=sat_disp_photo)
    sat_disp_label.image = sat_disp_photo
    sat_disp_label.grid(row=0, column=20, rowspan=1000, padx=10, pady=10)

# Function to implement satellite images using matplotlib
def satellite_configuration():

    global sat, stability_value, boolean, sat_mode
    if boolean == True:
        if sat.Rx < 0 and sat.Ix != sat.Iy: # satellite on LAM
            sat_mode = "LAM"
            plot_matplotlib_figure()
        elif sat.Rx > 0 and sat.Ix != sat.Iy: # satellite on SAM
            sat_mode = "SAM"
            plot_matplotlib_figure()
        elif sat.Rx < 0 and sat.Ix == sat.Iy: # axissymetric satellite on LAM
            sat_mode = "AXI_LAM"
            plot_matplotlib_figure()
        elif sat.Rx > 0: # axissymetric satellite on SAM
            sat_mode = "AXI_SAM"
            plot_matplotlib_figure()
        else:
            pass
    if stability_value == 'Satellite is not Stable.':
        if (3*sat.Rx + sat.Rx*sat.Ry + 1)**2 < 16*sat.Rx*sat.Ry:
            #Yaw-Roll instability
            pass
        else:
            # Pitch instability
            pass

# Function to obtain Rx and Ry from user input
def image_click(event):

    global sat2, Rx_label, Ry_label, Rz_label

    # Get the coordinates of the click event
    x = event.x
    y = event.y

    # Transform the image coordinates in Rx and Ry coordinates
    sat2.Rx = (x-358)/323
    sat2.Ry = -(y-379)/330 
    sat2.Rz = (sat2.Rx-sat2.Ry)/(1-sat2.Rx*sat2.Ry)

    # Delete previous values
    
    if Rx_label and Ry_label and Rz_label:
        Rx_label.destroy()
        Ry_label.destroy()
        Rz_label.destroy()

    # Present inertia funtions on screen
    Rx_label = ttk.Label(window, text=f"Rx: {sat2.Rx}", width = 30)
    Rx_label.grid(row=4, column=0, columnspan=2, padx = 20, pady=10)
    Ry_label = ttk.Label(window, text=f"Ry: {sat2.Ry}", width = 30)
    Ry_label.grid(row=5, column=0, columnspan=2, padx = 20, pady=10)
    Rz_label = ttk.Label(window, text=f"Rz: {sat2.Rz}", width = 30)
    Rz_label.grid(row=6, column=0, columnspan=2, padx = 20, pady=10)


# Declaration of necessary variables for functions
stability_value = None
canvas = None
boolean = None
control = None
program = True

while program == True:

    # Create the main window
    main_window = tk.Tk()
    main_window.title("Welcome!")

    #Define font
    style = ttk.Style()
    style.configure("TButton", font=('Helvetica', 20))

    # Create a button to evaluate a satellite
    button_evaluate = ttk.Button(main_window, text="Evaluate Satellite", width = 20, padding = (5,20), command=lambda: [control_function(1, main_window)])
    button_evaluate.grid(row=1, column=0, rowspan = 1, columnspan=1, padx = 50, pady=100)

    # Create a button to design a satellite
    button_evaluate = ttk.Button(main_window, text="Design Satellite", width = 20, padding = (5,20), command=lambda: [control_function(2, main_window)])
    button_evaluate.grid(row=1, column=2, rowspan = 1, columnspan=1, padx = 50, pady=100)

    # Create a button to quit
    button_evaluate = ttk.Button(main_window, text="Quit program", width = 20, padding = (5,10), command=lambda: [quit_program(main_window)])
    button_evaluate.grid(row=2, column=1, rowspan = 1, columnspan=1, padx = 50, pady=100)

    main_window.mainloop() #Loop for a window

    if program == False: #Necessary to break the program immediately if the Quit button is pressed
        break

    if control == True:
        
        # Create the window
        window = tk.Tk()
        window.title("Evaluate Satellite")
        sat = Satellite()

        #Create a button to go back
        wayback = ttk.Button(window, text="Go Back", command=lambda: [break_function(window)])
        wayback.grid(row=25, column=0, columnspan=2, pady=10)

        #Create a button to quit the program
        quit_now = ttk.Button(window, text="Quit program", command=lambda: [quit_program(window)])
        quit_now.grid(row=26, column=0, columnspan=2, pady=10)

        #Load Rx and Ry graph
        current_path = os.getcwd()
        image_name = "RxRygraph.png"
        image_path = os.path.join(current_path, image_name)
        image = tk.PhotoImage(file = image_path)

        # Create a label to display the Rx and Ry graph
        image_label = ttk.Label(window, image=image)
        image_label.grid(row=0, column=15, rowspan=1000, padx=10, pady=10)

        # Create labels and entry widgets for each number
        label1 = ttk.Label(window, text="I_x:")
        label1.grid(row=0, column=0, padx=10, pady=10)
        entry1 = ttk.Entry(window)
        entry1.grid(row=0, column=1, padx=10, pady=10)

        label2 = ttk.Label(window, text="I_y:")
        label2.grid(row=1, column=0, padx=10, pady=10)
        entry2 = ttk.Entry(window)
        entry2.grid(row=1, column=1, padx=10, pady=10)

        label3 = ttk.Label(window, text="I_z:")
        label3.grid(row=2, column=0, padx=10, pady=10)
        entry3 = ttk.Entry(window)
        entry3.grid(row=2, column=1, padx=10, pady=10)

        # Create a button to get the values
        button = ttk.Button(window, text="Calculate R's", command=lambda: [get_inertia_moments(), compute_inertia_functions(), check_stability()])
        button.grid(row=3, column=0, columnspan=2, pady=10)

        # Present inertia funtions on screen
        Rx_label = ttk.Label(window, text=f"Rx: {sat.Rx}")
        Rx_label.grid(row=4, column=0, columnspan=2, pady=10)
        Ry_label = ttk.Label(window, text=f"Ry: {sat.Ry}")
        Ry_label.grid(row=5, column=0, columnspan=2, pady=10)
        Rz_label = ttk.Label(window, text=f"Rz: {sat.Rz}")
        Rz_label.grid(row=6, column=0, columnspan=2, pady=10)

        # Create a label for displaying stability status
        stability_value = tk.StringVar()
        stability_value.set('Waiting for Values.')
        stability_label = ttk.Label(window, textvariable=stability_value)
        stability_label.grid(row=8, column=0, columnspan=3)

        # Button to draw a point on the graph
        draw_point_button = ttk.Button(window, text="Draw Point", command=lambda: draw_point())
        draw_point_button.grid(row=9, column=0, columnspan=2, pady=10)

        #Stability configuration
        draw_image_button = ttk.Button(window, text="Display Image", command=lambda: satellite_configuration())
        draw_image_button.grid(row=10, column=0, columnspan=2, pady=10)

        # Run the Tkinter event loop
        window.mainloop()

    if control == False:

        # Create the window
        window = tk.Tk()
        window.title("Design Satellite")
        sat2 = Satellite() #Design Satellite case

        #Create a button to go back
        wayback = ttk.Button(window, text="Go Back", command=lambda: [break_function(window)])
        wayback.grid(row=25, column=0, columnspan=2, pady=10)

        #Load Rx and Ry graph
        current_path = os.getcwd()
        image_name = "RxRygraph.png"
        image_path = os.path.join(current_path, image_name)
        image = tk.PhotoImage(file = image_path)

        # Create a label to display the Rx and Ry graph
        image_label = ttk.Label(window, image=image)
        image_label.grid(row=0, column=15, rowspan=1000, padx=30, pady=10)

        # Bind the mouse click to the graph, to get coordinates
        image_label.bind("<Button-1>", image_click)

        label_instructions = ttk.Label(window, text="Please click on the graph in the desired section.\n\nThen, input ONE moment of inertia ONLY, and leave the others blank.\n\nWhen everything is set, press 'Calculate I's'\n\n")
        label_instructions.grid(row=0, column=0, columnspan= 3, padx=10, pady=10)

        # Present inertia funtions on screen
        Rx_label = ttk.Label(window, text=f"Rx: {sat2.Rx}", width = 30)
        Rx_label.grid(row=4, column=0, columnspan=2, padx = 20, pady=10)
        Ry_label = ttk.Label(window, text=f"Ry: {sat2.Ry}", width = 30)
        Ry_label.grid(row=5, column=0, columnspan=2, padx = 20, pady=10)
        Rz_label = ttk.Label(window, text=f"Rz: {sat2.Rz}", width = 30)
        Rz_label.grid(row=6, column=0, columnspan=2, padx = 20, pady=10)

        # Create labels and entry widgets for each number
        label1 = ttk.Label(window, text="I_x:")
        label1.grid(row=7, column=0, padx=10, pady=10)
        entry1 = ttk.Entry(window)
        entry1.grid(row=7, column=1, padx=10, pady=10)

        label2 = ttk.Label(window, text="I_y:")
        label2.grid(row=8, column=0, padx=10, pady=10)
        entry2 = ttk.Entry(window)
        entry2.grid(row=8, column=1, padx=10, pady=10)

        label3 = ttk.Label(window, text="I_z:")
        label3.grid(row=9, column=0, padx=10, pady=10)
        entry3 = ttk.Entry(window)
        entry3.grid(row=9, column=1, padx=10, pady=10)

        # Create a button to get a single I value, see functions for more info
        button_inertia_moments_2 = ttk.Button(window, text="Calculate I's", command=lambda: [get_inertia_moments_2(), compute_inertia_moments_2()])
        button_inertia_moments_2.grid(row=10, column=0, columnspan=2, pady=10)

        # Present moments of inertia on screen
        Ix2_label = ttk.Label(window, text=f"Ix: {sat2.Ix}", width = 30)
        Ix2_label.grid(row=11, column=0, columnspan=2, padx = 20, pady=10)
        Iy2_label = ttk.Label(window, text=f"Iy: {sat2.Iy}", width = 30)
        Iy2_label.grid(row=12, column=0, columnspan=2, padx = 20, pady=10)
        Iz2_label = ttk.Label(window, text=f"Iz: {sat2.Iz}", width = 30)
        Iz2_label.grid(row=13, column=0, columnspan=2, padx = 20, pady=10)
        
        # Run the Tkinter event loop
        window.mainloop()