import cv2
import numpy as np
import math
import time
import random
from layers.layer import Layer, ColorTools

class Checkerboard(Layer):

    def compute(self, current=None, params={}):

        #dist between squares
        if 'padding' not in self.config:
            self.config['padding'] = 2
        #use random color fill every frame
        if 'colorRand' not in self.config:
            self.config['colorRand'] = False
        #use set color for each square (false = use random)
        if 'color' not in self.config:
            self.config['color'] = False
        #set seed so each square will be same between frames
        if 'colorSeed' not in self.config:
            self.config['colorSeed'] = 125411
        #num squares across x axis
        if 'numSquares' not in self.config:
            self.config['numSquares'] = 12
        #thickness of border (-1 = fill)
        if 'thickness' not in self.config:
            self.config['thickness'] = -1
        #random color ceiling (max 255)
        if 'randCeil' not in self.config:
            self.config['randCeil'] = 220
        #random color floor (min 50)
        if 'randFloor' not in self.config:
            self.config['randFloor'] = 80
        #adjust by n_live:
        if 'useTime' not in self.config:
            self.config['useTime'] = False
        #amount of shift by time (vector3, range 0:1):
        if 'timeVariance' not in self.config:
            self.config['timeVariance'] = 0.3
        #speed of color shift
        if 'timeSpeed' not in self.config:
            self.config['timeSpeed'] = (0.03, 0.04, 0.07)

        if self.config['colorRand']:
            self.config['colorSeed'] = (int)(time.time()//30000)

        random.seed(self.config['colorSeed'])

        mod = (1,1,1)
        if self.config['useTime']:
            mod = (0.5 + random.random()*math.sin(random.random()*self.n_l*self.config['timeSpeed'][0])*self.config['timeVariance'] ,#+ (1-self.config['timeVariance']),
                    0.5 + random.random()*math.cos(random.random()*self.n_l*self.config['timeSpeed'][1])*self.config['timeVariance'] ,#+ (1-self.config['timeVariance']),
                    0.5 + random.random()*math.sin(random.random()*self.n_l*self.config['timeSpeed'][2])*self.config['timeVariance'] #+ (1-self.config['timeVariance'])
                    )

        #print(mod)

        sqdim = (int)((self.dims[0]-(self.config['padding']*2*self.config['numSquares']))/self.config['numSquares'])
        for x in range(0,self.dims[1],sqdim+(2*self.config['padding'])):
            for y in range(0,self.dims[0],sqdim+(2*self.config['padding'])):
                color = self.config['color']
                if not self.config['color']:
                    color = ((int)(random.randint(self.config['randFloor'],self.config['randCeil'])*mod[0]),
                             (int)(random.randint(self.config['randFloor'],self.config['randCeil'])*mod[1]),
                             (int)(random.randint(self.config['randFloor'],self.config['randCeil'])*mod[2])
                             )
                    color = ColorTools.floorceil(color)
                current = cv2.rectangle(current,
                                        (x+self.config['padding'],y+self.config['padding']),
                                        (x+sqdim, y+sqdim),
                                        color,
                                        self.config['thickness']
                                        )

        return current
