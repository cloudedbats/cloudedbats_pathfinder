#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Project: http://cloudedbats.org
# Copyright (c) 2018 Arnold Andreasson 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).

import flask
# Bokeh embedded server.
from bokeh.embed import server_document
from bokeh.server.server import Server
from tornado.ioloop import IOLoop
# Bokeh plotting.
from bokeh.layouts import column
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.models import WheelZoomTool, ZoomInTool, ZoomOutTool
from bokeh.models import BoxZoomTool, PanTool, ResetTool
from bokeh.models import Slider
from bokeh.themes import Theme
# Pathfinder.
from pathfinder_single_user_flask import pathfinder_datastreamer
from pathfinder_single_user_flask import pathfinder_bokeh

# Flask.
flask_app = flask.Flask(__name__)

def modify_bokeh_document(bokeh_document):
    """ """
    sound_stream = pathfinder_datastreamer.PathfinderDataStreamer()
    sound_stream.start_streaming()
    print('--- STREAMING STARTED ---')
        
    data_source = ColumnDataSource({'x': [], 'y': [], 'ix': [], 'amp': []})
    
    def data_source_update():
        """ """
        x_list, y_list, index_list, amp_list = sound_stream.get_target_data()
        new = {'x': x_list, 'y': y_list, 'ix': index_list, 'amp': amp_list}
        print('--- data_source_update, length: ', len(x_list))
        data_source.stream(new, rollover=50000)
    #
    bokeh_document.add_periodic_callback(data_source_update, 300)
    
    # Bokeh plotting.
    pathfinder_bokeh.PathfinderBokeh().bokeh(data_source, bokeh_document)
    # Style.
#     bokeh_document.theme = Theme(filename="theme.yaml")


@flask_app.route('/', methods=['GET'])
def bkapp_page():
    script = server_document('http://localhost:5006/bkapp')
    return flask.render_template("pathfinder_bokeh.html", script=script, template="Flask")


def bk_worker():
    server = Server({'/bkapp': modify_bokeh_document}, 
                    io_loop=IOLoop(), 
                    allow_websocket_origin=["localhost:5000"])
    server.start()
    server.io_loop.start()

from threading import Thread
Thread(target=bk_worker).start()

if __name__ == '__main__':
    """ """
    print('CloudedBats - Pathfinder. Open web browser at http://localhost:5000/')
    print('Note: Single user only.')

    flask_app.run(debug=False, host='0.0.0.0', port=5000)
    
    