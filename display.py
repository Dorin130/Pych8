import numpy as np
from font import font

class Display:
    def __init__(self):
        self.display = np.zeros((32, 64), dtype='bool')

    def draw(self, x, y, data):
        ix, iy = np.meshgrid(np.arange(data.shape[1]), np.arange(data.shape[0]))

        x = (ix + x) % self.display.shape[0]
        y = (iy + y) % self.display.shape[1]

        res = self.display[y, x] & data

        self.display[y, x] ^= data

        return True in set(res.flat)

    def clear(self):
        self.display = np.zeros((32, 64), dtype='bool')

    def get_display(self):
        return self.display