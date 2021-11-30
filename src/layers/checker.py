import cv2
import numpy as np
import math
import time
import random
from layers.layer import Layer, ColorTools

class Checkerboard(Layer):

    def compute(self, current=None, params={}):

        #dist between squares
        if 'padding' not in params:
            params['padding'] = 2
        #use random color fill every frame
        if 'colorRand' not in params:
            params['colorRand'] = False
        #use set color for each square (false = use random)
        if 'color' not in params:
            params['color'] = False
        #set seed so each square will be same between frames
        if 'colorSeed' not in params:
            params['colorSeed'] = 125411
        #num squares across x axis
        if 'numSquares' not in params:
            params['numSquares'] = 12
        #thickness of border (-1 = fill)
        if 'thickness' not in params:
            params['thickness'] = -1
        #random color ceiling (max 255)
        if 'randCeil' not in params:
            params['randCeil'] = 220
        #random color floor (min 50)
        if 'randFloor' not in params:
            params['randFloor'] = 80
        #adjust by n_live:
        if 'useTime' not in params:
            params['useTime'] = False
        #amount of shift by time (vector3, range 0:1):
        if 'timeVariance' not in params:
            params['timeVariance'] = 0.3
        #speed of color shift
        if 'timeSpeed' not in params:
            params['timeSpeed'] = (0.03, 0.04, 0.07)

        if params['colorRand']:
            params['colorSeed'] = (int)(time.time()//30000)

        random.seed(params['colorSeed'])

        mod = (1,1,1)
        if params['useTime']:
            mod = (0.5 + random.random()*math.sin(random.random()*self.n_l*params['timeSpeed'][0])*params['timeVariance'] ,#+ (1-params['timeVariance']),
                    0.5 + random.random()*math.cos(random.random()*self.n_l*params['timeSpeed'][1])*params['timeVariance'] ,#+ (1-params['timeVariance']),
                    0.5 + random.random()*math.sin(random.random()*self.n_l*params['timeSpeed'][2])*params['timeVariance'] #+ (1-params['timeVariance'])
                    )

        #print(mod)

        sqdim = (int)((self.dims[0]-(params['padding']*2*params['numSquares']))/params['numSquares'])
        for x in range(0,self.dims[1],sqdim+(2*params['padding'])):
            for y in range(0,self.dims[0],sqdim+(2*params['padding'])):
                color = params['color']
                if not params['color']:
                    color = ((int)(random.randint(params['randFloor'],params['randCeil'])*mod[0]),
                             (int)(random.randint(params['randFloor'],params['randCeil'])*mod[1]),
                             (int)(random.randint(params['randFloor'],params['randCeil'])*mod[2])
                             )
                    color = ColorTools.floorceil(color)
                current = cv2.rectangle(current,
                                        (x+params['padding'],y+params['padding']),
                                        (x+sqdim, y+sqdim),
                                        color,
                                        params['thickness']
                                        )

        return current
