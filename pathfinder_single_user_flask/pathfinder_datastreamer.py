

import math

class PathfinderDataStreamer():
    """ """
    def __init__(self):
        """ """        
        self.x = 0
        self.y = 0
        
    def get_target_data(self):
        """ """
        x_list = []
        y_list = []
        while len(x_list) < 200:
            self.x = self.x + 0.1
            self.y = math.sin(self.x) * 50.0 + 50.0
            x_list.append(self.x)
            y_list.append(self.y)
        #
        return x_list, y_list
        
