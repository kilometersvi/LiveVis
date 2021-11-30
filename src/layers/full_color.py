from layers.layer import Layer
import cv2
import numpy as np

class FullColor(Layer):

    def compute(self, current=None, params={}):
        color = (1.0,1.0,1.0,1.0)

        if 'color' in self.config:
            color = self.config['color']

        frame = np.dstack([np.ones(self.dims, 'f')*color[0],
                               np.ones(self.dims, 'f')*color[1],
                               np.ones(self.dims, 'f')*color[2],
                               np.ones(self.dims, 'f')*color[3]
                              ])

        return frame
