import os
import pathlib

import pandas as pd
import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import layout, row, column

from bokeh.models import (Button, CategoricalColorMapper, ColumnDataSource,
                          HoverTool, Label, SingleIntervalTicker, Slider, Div)
from bokeh.palettes import Spectral6
from bokeh.plotting import figure
from bokeh.transform import factor_cmap

import datetime



# Define paths.
dir_path = os.path.dirname(os.path.realpath(__file__))
PATH_DATA = pathlib.Path(os.path.join(dir_path, 'raw_data'))

# all data
all_df_dict = np.load(PATH_DATA/'my_file_all.npy', allow_pickle='TRUE').item()

# by sex 
all_df_dict_0 = np.load(PATH_DATA/'my_file_all0.npy', allow_pickle='TRUE').item()
all_df_dict_1 = np.load(PATH_DATA/'my_file_all1.npy', allow_pickle='TRUE').item()
all_df_bySex =  {} 
for ii in range(0,len(all_df_dict),1):
    df0 = all_df_dict_0[str(ii)]
    df1 = all_df_dict_1[str(ii)]
    df = df0
    df = df.append(df1,ignore_index=True)
    all_df_bySex.update({str(ii): df})

data = {}
#date start 2002m12

# Date 
dates = []
dates_all = []
years = range(2002,2021,1)
months = range(1, 13, 1)
for year in years: 
    for month in months: 
        dates_all.append(str(month)+'-'+str(year))
dates_all = dates_all[11:]

source_all = ColumnDataSource(data=all_df_dict['0']) 
source_all_bySex = ColumnDataSource(data=all_df_bySex['0'])

dates = dates_all[0]
TOOLS = 'save,pan,box_zoom,reset,wheel_zoom'
p = figure(x_range=(1, 16), y_range=(0, 30), y_axis_type="linear",
           tools = TOOLS, sizing_mode="fixed", width = 800, height = 300)

p.vbar(x = 'x', top = 'y', 
       color = 'grey', 
       width = np.median(np.abs(np.array(source_all.data['x'])[0:-2] - np.array(source_all.data['x'])[1:-1])),
       visible  = True, 
       source = source_all,
       fill_alpha  = 0.5)

p.add_tools(HoverTool(tooltips=[("Renta", "@x"), ("Densidad", "@y")]))
p.title.text = "Distribución de renta: " + dates
#p.xaxis.ticker = SingleIntervalTicker(interval=0)
p.xaxis.axis_label = 'log(Renta)'
#p.yaxis.ticker = SingleIntervalTicker(interval=0)
p.yaxis.axis_label = 'Densidad'


# by sex
p_bySex = figure(x_range=(1, 16), y_range=(0, 30), y_axis_type="linear",
           tools = TOOLS, sizing_mode="fixed", width = 800, height = 300)

p_bySex.vbar(x = 'x', top = 'y', 
       width = np.median(np.abs(np.array(source_all.data['x'])[0:-2] - np.array(source_all.data['x'])[1:-1])),
       visible  = True, 
       source = source_all_bySex,
       fill_alpha  = 0.5,
       fill_color = factor_cmap('sex', palette=Spectral6, factors=['0','1'], start=1),
       legend_field = 'sex'
       )
p_bySex.legend.location = "top_left"
p_bySex.legend.click_policy="hide"

p_bySex.add_tools(HoverTool(tooltips=[("Renta", "@x"), ("Densidad", "@y")]))
p_bySex.title.text = "Distribución de renta de hombres y mujeres: " + dates
#p.xaxis.ticker = SingleIntervalTicker(interval=0)
p_bySex.xaxis.axis_label = 'log(Renta)'
#p.yaxis.ticker = SingleIntervalTicker(interval=0)
p_bySex.yaxis.axis_label = 'Densidad'


def slider_update(attrname, old, new):
    year = slider.value
    # label.text = str(year)
    
    source_all.data = all_df_dict[str(year)]
    source_all_bySex.data = all_df_bySex[str(year)]
    
    dates = dates_all[year]
    
    p.title.text = "Distribución de renta: " + dates
    p_bySex.title.text = "Distribución de renta de hombres y mujeres: " + dates

slider = Slider(start=0, end=len(all_df_dict) - 1, value=0, step=1, title="Date",
                sizing_mode="stretch_both")
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

button = Button(label='► Play',sizing_mode="stretch_both")
button.on_click(animate)

widgets = column([slider, button], sizing_mode="fixed", height=80, width=260)
# heading fills available width
#heading = Div(..., height=80, sizing_mode="stretch_width")

#layout = column(heading, row(widgets,p, p_bySex), sizing_mode="stretch_both")
layout = layout([
    p,
    p_bySex,
    widgets,
], sizing_mode="stretch_both")

curdoc().add_root(layout)
curdoc().title = "renta"

"""
in terminal use: bokeh serve --show myapp.py

"""