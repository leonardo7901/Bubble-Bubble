import unittest
import x7_BB

class ParamDragonTest(unittest.TestCase):
    def dragon_symbol(self):
        test_values = ((-10, -10 )) # dx, dy

        for i in test_values:
            x0, y0 = i
            d = Dragon(x0, y0)
            d.move()
            self.assertTrue(d.symbol() == (217, 36, 16, 16) )