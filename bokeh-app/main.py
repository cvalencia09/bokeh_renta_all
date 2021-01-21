import os
import pathlib

import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import layout
from bokeh.models import (Button, CategoricalColorMapper, ColumnDataSource,
                          HoverTool, Label, SingleIntervalTicker, Slider)
from bokeh.palettes import Spectral6
from bokeh.plotting import figure


# Define paths.
dir_path = os.path.dirname(os.path.realpath(__file__))
PATH_DATA = pathlib.Path(os.path.join(dir_path, 'renta'))
all_df_dict = np.load(PATH_DATA/'my_file.npy', allow_pickle='TRUE').item()

data = {}


source = ColumnDataSource(data=all_df_dict['0']) 
TOOLS = 'save,pan,box_zoom,reset,wheel_zoom'
p = figure(x_range=(1, 16), y_range=(0, 30),title="Kernel de distribución de renta", y_axis_type="linear", plot_height = 400,
           tools = TOOLS, plot_width = 800)

p.vbar(x = 'x', top = 'y', color = 'grey', width = np.min(np.abs(np.array(source.data['x'])[0:-2] - np.array(source.data['x'])[1:-1]))          , visible  = True, source = source)

p.add_tools(HoverTool(tooltips=[("Renta", "@x"), ("Densidad", "@y")]))

#p.xaxis.ticker = SingleIntervalTicker(interval=0)
p.xaxis.axis_label = 'Renta'
#p.yaxis.ticker = SingleIntervalTicker(interval=0)
p.yaxis.axis_label = 'Densidad'

def slider_update(attrname, old, new):
    year = slider.value
    # label.text = str(year)
    source.data = all_df_dict[str(year)]

slider = Slider(start=0, end=len(all_df_dict) - 1, value=0, step=1, title="Date")
slider.on_change('value', slider_update)

callback_id = None


def animate_update():
    year = slider.value + 1
    if year > len(all_df_dict):
        year = 0
    slider.value = year

def animate():
    global callback_id
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        callback_id = curdoc().add_periodic_callback(animate_update, 200)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(callback_id)

button = Button(label='► Play', width=60)
button.on_click(animate)

layout = layout([
    [p],
    [slider, button],
], sizing_mode='fixed')


curdoc().add_root(layout)
curdoc().title = "renta"

"""
in terminal use: bokeh serve --show myapp.py

"""