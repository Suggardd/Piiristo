"""

SchemCanvas - a (very) small extension to allow SchemDraw to use TkInter canvas

@author Mika Oja, University of Oulu

Extension for: 
https://cdelker.bitbucket.io/SchemDraw/SchemDraw.html

Created for educational purposes.

Defines a new subclass for SchemDraw.Drawing where the draw method is replaced
by one that draws on a fixed size matplotlib canvas widget instead of a 
variable size matplotlib pyplot window. 

Tested with matplotlib TkAgg figure canvas widget.
"""

import numpy as np
import matplotlib
import SchemDraw

PAD_FACTOR = 0.2

class CanvasDrawing(SchemDraw.Drawing):
    
    def draw(self, canvas, fig, ax):

        matplotlib.rcParams['font.size'] = self.fontsize
        matplotlib.rcParams['font.family'] = self.font

        for e in self._elm_list:
            e.draw(ax)
    
        ax.autoscale_view(True)  # This autoscales all the shapes too
        # NOTE: arrows don't seem to be included in autoscale!
        
        xlim = np.array(ax.get_xlim())
        ylim = np.array(ax.get_ylim())
        dpi = fig.get_dpi()
        cw, ch = canvas.get_width_height() 
        cw, ch = cw / dpi, ch / dpi
        
        dw, dh = xlim[1]-xlim[0], ylim[1]-ylim[0]
        
        x_ratio = dw / cw
        y_ratio = dh / ch
        
        xlim[0] -= PAD_FACTOR * x_ratio
        xlim[1] += PAD_FACTOR * x_ratio
        ylim[0] -= PAD_FACTOR * y_ratio
        ylim[1] += PAD_FACTOR * y_ratio
        
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.set_frame_on(False)
        
        self.ax = ax
        self.fig = fig
        canvas.show()
        
    def clear(self):
        self.here = np.array([0, 0])
        self.theta = 0
        self._state = []
        self._elm_list = []

