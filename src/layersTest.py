from layer_controller import LayerHandler
from layers.full_color import FullColor
from layers.color_mix_2split import ColorMix2Split
from layers.split4 import Split4
from layers.checker import Checkerboard
from layers.moving import Move
import time
import cv2
import random

if __name__=="__main__":

    n = 0

    possibleLayers = [
        Checkerboard(config={'useTime':True}),
        Checkerboard(config={'useTime':True, 'numSquares':8, 'thickness':2, 'colorRand':True}),
        Checkerboard(config={'useTime':True, 'numSquares':20, 'colorRand':True}),
        Move(config={'vertical':'down'}),
        Move(config={'horizontal':'left'}),
        ColorMix2Split()
    ]
    weights = [
        2,
        1,
        1,
        1,
        1,
        2
    ]

    layers = [FullColor(config={'color':(0,0,0,1.0)}),
              Checkerboard(config={'useTime':True}),
              Move(config={'vertical':'down'})]
              #ColorMix2Split()]

    current = []

    while True:
        #print(f"{n}: {layers}")
        current = LayerHandler.combineLayers(layers,params={'n':n})


        LayerHandler.Show(current, cv2Show=True)
        n+=1
        usesplit4 = 0
        if n%100==0:
            usesplit4 = random.randint(0,10)

        if usesplit4 > 7 and n%25==0:
            layers.append(Split4())

        if (n%100==0):
            layers = LayerHandler.randomLayers(possibleLayers, weights, reduceBy=0)



        time.sleep(0.01)
        if cv2.waitKey(1) & 0xFF == ord( 'x' ):
            break

    input.release()
    cv2.destroyAllWindows()
