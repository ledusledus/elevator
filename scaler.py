
class Scaler():
    """ 
    this class represents efficient scaling mechanisms
    """
    def __init__(self, x, y, min_x, min_y):
        """
        x, y - current_size
        min_x, min_y - real_values
        """
        self.x = x
        self.y = y
        self.scale_x = x
        self.scale_y = y
        self.min_x = min_x
        self.min_y = min_y
        self.ratio = 1
    def set_scale_x(self, x):
        self.scale_x = x
        self.ratio = float(self.scale_x) / self.x
        # linear relation ship
        # x / scale_x = y / scale_y
        # thus y*scale_x/x = scale_y
        self.scale_y = self.y*self.scale_x/self.x
    def set_scale_y(self, y):
        # swap x and y, call for x, swap back
        self.x, self.y = self.y, self.x
        self.set_scale_x(y)
        self.x, self.y = self.y, self.x
        self.scale_y, self.scale_x = self.scale_x, self.scale_y
    def locate(self, point):
        p = point[0]-self.min_x, point[1]-self.min_y
        p = p[0] * self.ratio, p[1]*self.ratio
        return p
        

import unittest

class TestScaler(unittest.TestCase):
    def test_min_zeroes(self):
        scaler = Scaler(100, 200, 0, 0)
        scaler.set_scale_x( 200 )
        self.assertEqual( scaler.scale_x, 200 )
        self.assertEqual( scaler.scale_y, 400 )
        scaler.set_scale_y( 2 )
        self.assertEqual(.01, scaler.ratio)
        self.assertEqual( scaler.scale_x, 1 )
        self.assertEqual( scaler.scale_y, 2 )
        self.assertEqual( (1,2), scaler.locate( (100, 200) ) )
    def test_min_non_zeroes(self):
        scaler = Scaler(100, 200, 1500, 4000)
        scaler.set_scale_x( 200 )
        self.assertEqual( scaler.scale_x, 200 )
        self.assertEqual( scaler.scale_y, 400 )
        scaler.set_scale_y( 2 )
        self.assertEqual(.01, scaler.ratio)
        self.assertEqual( scaler.scale_x, 1 )
        self.assertEqual( scaler.scale_y, 2 )
        self.assertEqual( (1,2), scaler.locate( (1600, 4200) ) )
                
if __name__ == "__main__":
    unittest.main()