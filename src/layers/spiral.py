import cv2
import numpy as np
import math
import matplotlib.pyplot as plt
from layers.layer import Layer

class Spiral(Layer):

    def compute(self, current=None, params={}):

        

        fig, ax = plt.subplots()
        #Image from plot
        ax.axis('off')
        fig.tight_layout(pad=0)

        # To remove the huge white borders
        ax.margins(0)

        fig.canvas.draw()
        image_from_plot = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        image_from_plot = image_from_plot.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        current[]
        return current
