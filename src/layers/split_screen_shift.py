import cv2
import numpy as np
import pandas as pd

class Split_Screen_Split:
    def __init__(self, n_start):
        self.n = n_start

    def __iter__(self)


"""
def __init__(self):
        self.all_data = list(range(23))
        self.size = 0

    def __iter__(self):
        random.shuffle(self.all_data)
        batch = list()
        for i in self.all_data:
            batch.append(i)
            if len(batch) >= self.size:
                yield batch
                batch = list()

    def __call__(self, n):
        self.size = n
        return self
"""
