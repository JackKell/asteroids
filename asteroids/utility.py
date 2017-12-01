from math import cos, sin, atan2, sqrt, radians, pi, atan, hypot
from typing import Tuple, Sequence

import pygame
from pygame.surface import Surface


def getPointFromPolarCoordinate(origin, distance: float, angle: float) -> Tuple[float, float]:
    return round(distance * cos(angle) + origin[0], 0), round(distance * sin(angle) + origin[1], 0)


def getRectangle(origin, angle, size):
    x = (size[0] / 2.0)
    y = (size[1] / 2.0)
    distance = sqrt(x ** 2 + y ** 2)
    point1 = getPointFromPolarCoordinate(origin, distance, -1 * atan2(y, x) + radians(angle))
    point2 = getPointFromPolarCoordinate(origin, distance, atan2(y, x) + radians(angle))
    point3 = getPointFromPolarCoordinate(origin, distance, -1 * atan2(-x, y) + radians(angle) + radians(90))
    point4 = getPointFromPolarCoordinate(origin, distance, -1 * atan2(-y, x) + radians(angle) + radians(180))
    return [point1, point2, point3, point4]


def drawArrow(surface: Surface,
              color: Tuple[int, int, int],
              startPoint,
              endPoint,
              headSize,
              lineWidth: int = 1) -> None:
    lineAngle = atan2(endPoint[1] - startPoint[1], endPoint[0] - startPoint[0])
    arrowHeadWidth = headSize[0]
    halfArrowHeadWidth = arrowHeadWidth / 2
    arrowHeadHeight = headSize[1]
    z = atan(halfArrowHeadWidth / arrowHeadHeight)
    d = hypot(halfArrowHeadWidth, arrowHeadHeight)
    angleA = lineAngle + (pi - z)
    angleB = lineAngle - (pi - z)
    pointA = (d * cos(angleA) + endPoint[0], d * sin(angleA) + endPoint[1])
    pointB = (d * cos(angleB) + endPoint[0], d * sin(angleB) + endPoint[1])
    pygame.draw.line(surface, color, startPoint, endPoint, lineWidth)
    pygame.draw.polygon(surface, color, [pointA, pointB, endPoint])


def getMagnitude(vector: Sequence):
    squaredSum = 0
    for i in range(len(vector)):
        squaredSum += i ** 2
    return sqrt(squaredSum)

# def getRegularPolygon(origin, sides, radius, angle):
#     points: List[Tuple[float, float]] = []
#     for i in range(sides):
#         angle = tau * i / sides + radians(angle)
#         points.append(getPointFromPolarCoordinate(origin, radius, angle))
#     return points
