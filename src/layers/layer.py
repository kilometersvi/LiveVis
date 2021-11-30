from abc import ABC, abstractmethod


class Layer(ABC):

    def __init__(self, n_l=0, config={}, dims=(600,800)):

        self.n_l = n_l
        self.config = config
        self.dims = dims

        super().__init__()

    #all must return frame of shape(dims[0],dims[1],4) of type float32
    @abstractmethod
    def compute(self, current=None, params={}):
        pass

'''
    def effectAdd(self, o=None):
        frame = cv2.addWeighted(self.frame,1,o.frame,1,0)
        return frame;
'''

class ColorShifter:
    def __init__(self, timeVariance=0.5, timeSpeed=0.3):
        self.timeVariance = timeVariance
        self.timeSpeed = timeSpeed

        self.n_l = 0

    def __getitem__(self, indices):
        mod = (math.sin(self.n_l*self.timeSpeed)*self.timeVariance + (1-self.timeVariance),
                math.cos(self.n_l*self.timeSpeed)*self.timeVariance + (1-self.timeVariance),
                math.sin(self.n_l*self.timeSpeed)*self.timeVariance + (1-self.timeVariance)
                )
        return mod[indices]

    def increment_n(self):
        self.n_l += 1

class ColorTools:
    @staticmethod
    def floorceil(color):
        color_new = ((int)(min(254,max(1,color[0]))),
                     (int)(min(254,max(1,color[1]))),
                     (int)(min(254,max(1,color[2])))
                     )
        return color_new
