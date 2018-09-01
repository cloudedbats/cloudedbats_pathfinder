
import flask
import math
from bokeh.models.sources import AjaxDataSource
from bokeh.util.string import encode_utf8
#from .pathfinder_datastreamer import PathfinderDataStreamer
from pathfinder_datastreamer import PathfinderDataStreamer
from pathfinder_bokeh import PathfinderBokeh 

app = flask.Flask(__name__)
data_streamer = PathfinderDataStreamer()

@app.route('/')
def index():
    """ Main web page. """
    return flask.render_template('pathfinder_index.html')

@app.route('/data', methods=['POST'])
def update_data():
    """ Get data stream to AjaxDataSource object. """
    x_list, y_list = data_streamer.get_target_data()
    return flask.jsonify(x=x_list, y=y_list)

@app.route('/bokeh')
def bokeh():
    """ """
    # Bokeh AjaxDataSource for streaming data. Placed here due to url.
    data_source = AjaxDataSource(data_url="/data",
                                 polling_interval=200, mode='append', 
                                 max_size=10000, )
    # 
    pathfinder_bokeh = PathfinderBokeh(data_source)
    js_resources, css_resources, script, div = pathfinder_bokeh.bokeh()
    html = flask.render_template('pathfinder_bokeh.html', 
                                 plot_script=script, 
                                 plot_div=div, 
                                 js_resources=js_resources, 
                                 css_resources=css_resources, )
    return encode_utf8(html)

# Main.
if __name__ == '__main__':
    app.run(debug=True, port=28888)
    