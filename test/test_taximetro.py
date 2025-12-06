# test_taximetro.py
import unittest
from main import calc 

class TestCalc(unittest.TestCase):

    def test_calc_moving_10_seconds(self):
        """
        option '1' (moving) for 10 seconds
        10 * 0.05 = 0.5
        """
        result = calc('1', 10)
        self.assertAlmostEqual(result, 0.5)

    def test_calc_stopped_10_seconds(self):
        """
        option '2' (stopped) for 10 seconds
        10 * 0.02 = 0.2
        """
        result = calc('2', 10)
        self.assertAlmostEqual(result, 0.2)

    def test_calc_moving_zero_seconds(self):
        """
        0초일 때 요금은 0이어야 함
        """
        result = calc('1', 0)
        self.assertEqual(result, 0.0)

    def test_calc_stopped_zero_seconds(self):
        result = calc('2', 0)
        self.assertEqual(result, 0.0)

if __name__ == "__main__":
    unittest.main()