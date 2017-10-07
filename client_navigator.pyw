'''
This module is an exemplifying client of the game_level_generator module.
The user is prompted to choose the algorithm parameters (the defaults are shown).
After confirming the parameters, a new map is requested, and the current grid of the map is shown using matplotlib.pyplot.
The user may continuously navigate to neighboring grids using the arrow keys.
'''
import game_level_generator
import matplotlib.colors
import matplotlib.pyplot
import numpy
import tkinter

def new_field(input_box, row, desc, default):
    tkinter.Label(input_box, text = desc).grid(row = row, sticky = "w")
    field = tkinter.Entry(input_box)
    field.insert(tkinter.END, str(default))
    field.grid(row = row, column = 1)
    return field

def input_parameters():
    input_box = tkinter.Tk()
    input_box.title("Game Level Generator Parameters")
    index = iter(range(999))
    r = new_field(input_box, next(index), "Rock cells rate", game_level_generator.R)
    n = new_field(input_box, next(index), "Number of CA iterations", game_level_generator.N)
    t = new_field(input_box, next(index), "Rock expansion threshold", game_level_generator.T)
    m = new_field(input_box, next(index), "Moore neighborhood range", game_level_generator.M)
    s = new_field(input_box, next(index), "Grid side length", game_level_generator.S)
    tkinter.Button(input_box, text = "Start", command = lambda: start(r, n, t, m, s, input_box)).grid(row = next(index), columnspan = 2)
    tkinter.mainloop()

def plot_data(map_, cmap):
    image = numpy.array(game_level_generator.get_current_grid(map_))
    matplotlib.pyplot.figure(1).add_subplot(111).matshow(image, cmap = cmap)

def start(r, n, t, m, s, input_box):
    game_level_generator.R = float(r.get())
    game_level_generator.N = int(n.get())
    game_level_generator.T = int(t.get())
    game_level_generator.M = int(m.get())
    game_level_generator.S = int(s.get())
    input_box.destroy()
    map_ = game_level_generator.get_new_map()
    cmap = matplotlib.colors.ListedColormap(["w", "k"])
    plot_data(map_, cmap)
    matplotlib.pyplot.figure(1).canvas.set_window_title("Game Level Generator")
    matplotlib.pyplot.figure(1).canvas.mpl_connect("key_press_event", lambda event: key_press_event_handler(event, map_, cmap))
    matplotlib.pyplot.show()

def key_press_event_handler(event, map_, cmap):
    directions = ("up", "down", "left", "right")
    if event.key in directions:
        game_level_generator.go_to(map_, directions.index(event.key) + 1)
        plot_data(map_, cmap)
        matplotlib.pyplot.draw()

input_parameters()
