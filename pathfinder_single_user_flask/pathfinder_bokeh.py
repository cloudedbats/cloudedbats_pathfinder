
from bokeh.embed import components
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.models.sources import AjaxDataSource
from bokeh.models import WheelZoomTool, ZoomInTool, ZoomOutTool
from bokeh.models import BoxZoomTool, PanTool, ResetTool
from EXAMPLES.examples.howto.events_app import div
# from bokeh.models import RangeTool, Range1d, DataRange1d

class PathfinderBokeh():
    """ """
    def __init__(self, data_source):
        """ """
        self.data_source = data_source
        
    def bokeh(self):
        """ """
        # Figure 1 and plot.
        fig1 = figure(plot_width=800, plot_height=200, 
                      tools='', toolbar_location='above')
        fig1.add_tools(PanTool(dimensions='width'))
        fig1.add_tools(PanTool(dimensions='height'))
        fig1.add_tools(ZoomInTool(dimensions='width'))
        fig1.add_tools(ZoomOutTool(dimensions='width'))
        fig1.add_tools(BoxZoomTool())
    #     fig1.add_tools(UndoTool())
        fig1.add_tools(ResetTool())
        fig1.y_range.start = 0.0
        fig1.y_range.end = 150.0
        fig1.x_range.follow = 'end'
        fig1.x_range.follow_interval = 20.0
        fig1.x_range.range_padding_units = 'absolute'
        fig1.x_range.range_padding = 0.5
        
        #    
        plot1 = fig1.scatter(x='x', y='y', source=self.data_source, 
                             color='navy')
        # Figure 2 and plot.
        fig2 = figure(plot_width=800, plot_height=150, 
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
        fig2.x_range.follow_interval = 200.0
        fig2.x_range.range_padding_units = 'absolute'
        fig2.x_range.range_padding = 2
        #    
        plot2 = fig2.scatter(x='x', y='y', source=self.data_source, 
                             color='navy')
        
    #     # Layout.
        layout = column(fig1, fig2, sizing_mode='scale_width')
    
        # Bokeh stuff for the web page. Static resources, etc.
        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()
        script, div = components(layout)
        #
        return js_resources, css_resources, script, div
    