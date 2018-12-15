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
        self.data_source = None
        self.fig1 = None
        self.fig2 = None
        self.fig3 = None
        self.plot1 = None
        self.plot2 = None
        self.plot3 = None
        self.layout = None
#         self.inputs = None
        
    def bokeh(self, data_source, bokeh_document):
        """ """
        self.data_source = data_source
        # Figure 1 and plot.
        self.fig1 = figure(plot_width=800, plot_height=200, 
                      tools='', toolbar_location='above')
        self.fig1.add_tools(PanTool(dimensions='width'))
        self.fig1.add_tools(PanTool(dimensions='height'))
        self.fig1.add_tools(ZoomInTool(dimensions='width'))
        self.fig1.add_tools(ZoomOutTool(dimensions='width'))
        self.fig1.add_tools(BoxZoomTool())
        self.fig1.add_tools(ResetTool())
    #     self.fig1.add_tools(UndoTool())
#         self.fig1.add_tools(ResetTool())
        self.fig1.y_range.start = 0.0
#         self.fig1.y_range.end = 150.0
        self.fig1.x_range.follow = 'end'
        self.fig1.x_range.follow_interval = 60.0
        self.fig1.x_range.range_padding_units = 'absolute'
        self.fig1.x_range.range_padding = 0.1
        #    
        self.plot1 = self.fig1.scatter(x='x', y='y', source=self.data_source, 
                             size=1, # 'amp', 
                             color='navy')
        
        # Figure 2 and plot.
        self.fig2 = figure(plot_width=800, plot_height=200, 
                      tools='', toolbar_location='above')
        self.fig2.add_tools(PanTool(dimensions='width'))
        self.fig2.add_tools(PanTool(dimensions='height'))
        self.fig2.add_tools(ZoomInTool(dimensions='width'))
        self.fig2.add_tools(ZoomOutTool(dimensions='width'))
    #     self.fig2.add_tools(WheelZoomTool(dimensions='width'))
    #     self.fig2.add_tools(WheelZoomTool(dimensions='height'))
        self.fig2.add_tools(BoxZoomTool())
    #     self.fig2.add_tools(UndoTool())
        self.fig2.add_tools(ResetTool())
        self.fig2.y_range.start = 0.0
        self.fig2.y_range.end = 150.0
        self.fig2.x_range.follow = 'end'
        self.fig2.x_range.follow_interval = 5.0
        self.fig2.x_range.range_padding_units = 'absolute'
        self.fig2.x_range.range_padding = 0.1
        #    
        self.plot2 = self.fig2.scatter(x='x', y='y', source=self.data_source, 
                             size=1, #'amp', 
                             color='navy')

        # Figure 3 and plot.
        self.fig3 = figure(plot_width=800, plot_height=200, 
                      tools='', toolbar_location='above')
        self.fig3.add_tools(PanTool(dimensions='width'))
        self.fig3.add_tools(PanTool(dimensions='height'))
        self.fig3.add_tools(ZoomInTool(dimensions='width'))
        self.fig3.add_tools(ZoomOutTool(dimensions='width'))
    #     self.fig3.add_tools(WheelZoomTool(dimensions='width'))
    #     self.fig3.add_tools(WheelZoomTool(dimensions='height'))
        self.fig3.add_tools(BoxZoomTool())
    #     self.fig3.add_tools(UndoTool())
        self.fig3.add_tools(ResetTool())
        self.fig3.y_range.start = 0.0
        self.fig3.y_range.end = 150.0
        self.fig3.x_range.follow = 'end'
        self.fig3.x_range.follow_interval = 0.25
        self.fig3.x_range.range_padding_units = 'absolute'
        self.fig3.x_range.range_padding = 0.01
        #    
        self.plot3 = self.fig3.scatter(x='ix', y='y', source=self.data_source, 
                             size=1, #'amp', 
                             color='navy')

        # Slider test. Bug in this bokeh version, slider not used...
        def callback(attr, old, new):
            """ """
            print('Slider callback...', new)
            try:
                            
                self.fig1 = figure(plot_width=800, plot_height=200, 
                              tools='', toolbar_location='above')
                self.fig1.add_tools(PanTool(dimensions='width'))
                self.fig1.add_tools(PanTool(dimensions='height'))
                self.fig1.add_tools(ZoomInTool(dimensions='width'))
                self.fig1.add_tools(ZoomOutTool(dimensions='width'))
                self.fig1.add_tools(BoxZoomTool())
                self.fig1.add_tools(ResetTool())
            #     self.fig1.add_tools(UndoTool())
        #         self.fig1.add_tools(ResetTool())
                self.fig1.y_range.start = 0.0
        #         self.fig1.y_range.end = 150.0
        
                self.fig1.y_range.end = int(new)
        
                self.fig1.x_range.follow = 'end'
                self.fig1.x_range.follow_interval = 60.0
                self.fig1.x_range.range_padding_units = 'absolute'
                self.fig1.x_range.range_padding = 0.1
                
                self.plot1 = self.fig1.scatter(x='x', y='y', source=self.data_source, 
                                     size=1, # 'amp', 
                                     color='navy')
                
                bokeh_document.remove_root(self.layout)
                self.layout = column(self.fig1, self.fig2, self.fig3, inputs, sizing_mode='stretch_both')        
                bokeh_document.add_root(self.layout)
                
                
            except Exception as e:
                print('Slider callback exception:e', e)
     
        slider = Slider(start=100, end=200, value=150, step=1, title="Max freq. (kHz)")
        slider.on_change('value', callback)
        inputs = widgetbox(slider)

        # Layout.
#         layout = column(self.fig1, self.fig2, self.fig3, sizing_mode='stretch_both')
        self.layout = column(self.fig1, self.fig2, self.fig3, inputs, sizing_mode='stretch_both')

        bokeh_document.add_root(self.layout)
    
        