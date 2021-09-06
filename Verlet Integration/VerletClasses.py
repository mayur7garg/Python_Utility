import math
from typing import Union

class Vector():
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __truediv__(self, factor: Union[int,float]):
        return Vector(self.x / factor, self.y / factor)

    def __mul__(self, factor: Union[int,float]):
        return Vector(self.x * factor, self.y * factor)

    def __str__(self) -> str:
        return f"Vector({self.x}, {self.y})"

    def distance(self, other) -> float:
        return math.sqrt(pow(self.x - other.x, 2) + pow(self.y - other.y, 2))

    def magnitude(self) -> float:
        return self.distance(Vector(0, 0))

    def normalized(self):
        mag = self.magnitude()
        if mag <= 0:
            return Vector(0, 0)
        else:
            return self / mag

class Point():
    def __init__(self, loc: Vector, isLocked: bool = False) -> None:
        self.loc = loc
        self.prevLoc = loc
        self.isLocked = isLocked

class Stick():
    def __init__(self, p1: Point, p2: Point) -> None:
        self.p1 = p1
        self.p2 = p2
        self.length = p1.loc.distance(p2.loc)