#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

from bokeh.embed import components
from bokeh.layouts import column, widgetbox
from bokeh.models.widgets import Slider
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.models.sources import AjaxDataSource
from bokeh.models import WheelZoomTool, ZoomInTool, ZoomOutTool
from bokeh.models import BoxZoomTool, PanTool, ResetTool
# from EXAMPLES.examples.howto.events_app import div
# from bokeh.models import RangeTool, Range1d, DataRange1d

# def update_data(attrname, old, new):
#     print('DEBUG: ')


class PathfinderBokeh():
    """ """
    def __init__(self):
        """ """
    def bokeh(self, data_source, bokeh_document):
        """ """
        # Figure 1 and plot.
        fig1 = figure(plot_width=800, plot_height=200, 
                      tools='', toolbar_location='above')
        fig1.add_tools(PanTool(dimensions='width'))
        fig1.add_tools(PanTool(dimensions='height'))
        fig1.add_tools(ZoomInTool(dimensions='width'))
        fig1.add_tools(ZoomOutTool(dimensions='width'))
        fig1.add_tools(BoxZoomTool())
        fig1.add_tools(ResetTool())
    #     fig1.add_tools(UndoTool())
#         fig1.add_tools(ResetTool())
        fig1.y_range.start = 0.0
        fig1.y_range.end = 150.0
        fig1.x_range.follow = 'end'
        fig1.x_range.follow_interval = 60.0
        fig1.x_range.range_padding_units = 'absolute'
        fig1.x_range.range_padding = 0.1
        #    
        plot1 = fig1.scatter(x='x', y='y', source=data_source, 
                             size=1, # 'amp', 
                             color='navy')
        
        # Figure 2 and plot.
        fig2 = figure(plot_width=800, plot_height=200, 
                      tools='', toolbar_location='above')
        fig2.add_tools(PanTool(dimensions='width'))
        fig2.add_tools(PanTool(dimensions='height'))
        fig2.add_tools(ZoomInTool(dimensions='width'))
        fig2.add_tools(ZoomOutTool(dimensions='width'))
    #     fig2.add_tools(WheelZoomTool(dimensions='width'))
    #     fig2.add_tools(WheelZoomTool(dimensions='height'))
        fig2.add_tools(BoxZoomTool())
    #     fig2.add_tools(UndoTool())
        fig2.add_tools(ResetTool())
        fig2.y_range.start = 0.0
        fig2.y_range.end = 150.0
        fig2.x_range.follow = 'end'
        fig2.x_range.follow_interval = 5.0
        fig2.x_range.range_padding_units = 'absolute'
        fig2.x_range.range_padding = 0.1
        #    
        plot2 = fig2.scatter(x='x', y='y', source=data_source, 
                             size=1, #'amp', 
                             color='navy')

        # Figure 3 and plot.
        fig3 = figure(plot_width=800, plot_height=200, 
                      tools='', toolbar_location='above')
        fig3.add_tools(PanTool(dimensions='width'))
        fig3.add_tools(PanTool(dimensions='height'))
        fig3.add_tools(ZoomInTool(dimensions='width'))
        fig3.add_tools(ZoomOutTool(dimensions='width'))
    #     fig3.add_tools(WheelZoomTool(dimensions='width'))
    #     fig3.add_tools(WheelZoomTool(dimensions='height'))
        fig3.add_tools(BoxZoomTool())
    #     fig3.add_tools(UndoTool())
        fig3.add_tools(ResetTool())
        fig3.y_range.start = 0.0
        fig3.y_range.end = 150.0
        fig3.x_range.follow = 'end'
        fig3.x_range.follow_interval = 0.25
        fig3.x_range.range_padding_units = 'absolute'
        fig3.x_range.range_padding = 0.01
        #    
        plot3 = fig3.scatter(x='ix', y='y', source=data_source, 
                             size=1, #'amp', 
                             color='navy')

        # Slider test. Bug in this bokeh version, slider not used...
#         def callback(attr, old, new):
#             """ """
#             print('Slider callback...', new)            
#             fig1.y_range.end = new
#     
#         slider = Slider(start=100, end=200, value=150, step=1, title="Max freq. (kHz)")
#         slider.on_change('value', callback)
#         inputs = widgetbox(slider)

        # Layout.
        layout = column(fig1, fig2, fig3, sizing_mode='stretch_both')
#         layout = column(fig1, fig2, fig3, inputs, sizing_mode='stretch_both')

        bokeh_document.add_root(layout)
    
        