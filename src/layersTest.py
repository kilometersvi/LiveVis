from layer_controller import LayerHandler
from layers.full_color import FullColor
from layers.color_mix_2split import ColorMix2Split
from layers.split4 import Split4
from layers.checker import Checkerboard
import time
import cv2

if __name__=="__main__":

    timeout = 1000
    n = 0

    #ColorMix2Split()

    layers = [FullColor(config={'color':(0,0,0,1.0)}),
              Checkerboard()]
              #ColorMix2Split()]

    current = []

    while True:
        current = LayerHandler.combineLayers(layers,params={'n':n})


        LayerHandler.Show(current, cv2Show=True)
        n+=1

        '''
        if n%100==0:
            layers.append(Split4())
        '''
        time.sleep(0.01)
        if cv2.waitKey(1) & 0xFF == ord( 'x' ):
            break
        if n > timeout:
            break

    input.release()
    cv2.destroyAllWindows()
