import math
import unittest

from astroids.utility import getPointFromPolarCoordinate, getRectangle


class TestGetPointFromPolarCoordinate(unittest.TestCase):
    def test_numbers_0_0_5_0(self):
        point = getPointFromPolarCoordinate((0, 0), 1, math.radians(0))
        print(0, 1, point)
        self.assertEqual(point, (1, 0))

    def test_numbers_0_0_5_90(self):
        point = getPointFromPolarCoordinate((0, 0), 1, math.radians(90))
        print(90, 1, point)
        self.assertEqual(point, (0, 1))

    def test_numbers_0_0_5_180(self):
        point = getPointFromPolarCoordinate((0, 0), 1, math.radians(180))
        print(180, 1, point)
        self.assertEqual(point, (-1, 0))

    def test_numbers_0_0_5_270(self):
        point = getPointFromPolarCoordinate((0, 0), 1, math.radians(270))
        print(270, 1, point)
        self.assertEqual(point, (0, -1))

    def test_accuracy(self):
        point1 = getPointFromPolarCoordinate((0, 0), 1, math.radians(45))


class TestGetRectangle(unittest.TestCase):
    def test_numbers_1_1_0_2_2(self):
        points = getRectangle((1, 1), 0, (2, 2))
        print(points)
        self.assertEqual(points, [(2, 0), (2, 2), (0, 2), (0, 0)])

