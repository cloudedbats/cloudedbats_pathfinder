# # from bokeh.embed import server_document
# # from bokeh.server.server import Server
# # from tornado.ioloop import IOLoop
# # # Bokeh plotting.
# from bokeh.layouts import column
# # from bokeh.plotting import figure
# from bokeh.models import ColumnDataSource
# # from bokeh.models import WheelZoomTool, ZoomInTool, ZoomOutTool
# # from bokeh.models import BoxZoomTool, PanTool, ResetTool
# # from bokeh.models import Slider
# # from bokeh.themes import Theme
# # # Pathfinder.

from bokeh.plotting import curdoc
from bokeh.models import ColumnDataSource
# Pathfinder.
import pathfinder_datastreamer
import pathfinder_bokeh

sound_stream = None
print('###################### sound_stream = None')

# def set_sound_stream(soundstream):
#     global sound_stream
#     sound_stream = soundstream
#     print('###################### sound_stream = set_sound_stream()')

sound_stream = pathfinder_datastreamer.PathfinderDataStreamer()
sound_stream.start_streaming()
print('--- STREAMING STARTED ---')
    
data_source = ColumnDataSource({'x': [], 'y': [], 'ix': [], 'amp': []})

def data_source_update():
    """ """
    global sound_stream
#     print('######################-A')    
    if sound_stream:
        x_list, y_list, index_list, amp_list = sound_stream.get_target_data()
        new = {'x': x_list, 'y': y_list, 'ix': index_list, 'amp': amp_list}
        print('--- data_source_update, length: ', len(x_list))
        data_source.stream(new, rollover=5000)
#     else:
#         print('sound_stream MISSING')
#         sound_stream = pathfinder_datastreamer.PathfinderDataStreamer()
#         sound_stream.start_streaming()
#         print('--- STREAMING STARTED ---')

#
curdoc().add_periodic_callback(data_source_update, 300)

# Bokeh plotting.
pathfinder_bokeh.PathfinderBokeh().bokeh(data_source, curdoc())

print('######################-B')    


# # from pathfinder_single_user_flask import pathfinder_datastreamer
# # from pathfinder_single_user_flask import pathfinder_bokeh
# 
# from bokeh.plotting import curdoc, figure
# 
# i = 0
# 
# data_source = ColumnDataSource({'x': [], 'y': []})
# 
# def data_source_update():
#     """ """
#     global i
#     i += 1
#     new = {'x': [i], 'y': [i]}
#     data_source.stream(new, rollover=100)
# #
# curdoc().add_periodic_callback(data_source_update, 500)
# 
# fig1 = figure(plot_width=800, plot_height=200, 
#               toolbar_location='above')
# 
# plot1 = fig1.scatter(x='x', y='y', source=data_source, 
#                      size=1, # 'amp', 
#                      color='navy')
# 
# 
# # put the button and plot in a layout and add to the document
# curdoc().add_root(column(fig1))


# from functools import partial
# import time
#  
# from concurrent.futures import ThreadPoolExecutor
# from tornado import gen
#  
# from bokeh.document import without_document_lock
# from bokeh.models import ColumnDataSource
# from bokeh.plotting import curdoc, figure
#  
# source = ColumnDataSource(data=dict(x=[0], y=[0], color=["blue"]))
#  
# i = 0
#  
# doc = curdoc()
#  
# executor = ThreadPoolExecutor(max_workers=2)
#  
# def blocking_task(i):
#     time.sleep(1)
#     return i
#  
# # the unlocked callback uses this locked callback to safely update
# @gen.coroutine
# def locked_update(i):
#     source.stream(dict(x=[source.data['x'][-1]+1], y=[i], color=["blue"]))
#  
# # this unclocked callback will not prevent other session callbacks from
# # executing while it is in flight
# @gen.coroutine
# @without_document_lock
# def unlocked_task():
#     global i
#     i += 1
#     res = yield executor.submit(blocking_task, i)
#     doc.add_next_tick_callback(partial(locked_update, i=res))
#  
# @gen.coroutine
# def update():
#     source.stream(dict(x=[source.data['x'][-1]+1], y=[i], color=["red"]))
#  
# p = figure(x_range=[0, 100], y_range=[0,20])
# l = p.circle(x='x', y='y', color='color', source=source)
#  
# doc.add_periodic_callback(unlocked_task, 1000)
# doc.add_periodic_callback(update, 200)
# doc.add_root(p)
