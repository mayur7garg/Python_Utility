import random
from VerletClasses import Vector, Point, Stick
from typing import List, Union

def simulate(points: List[Point], sticks: List[Stick], num_iter: int, shuffle: bool = False, seed: int = 7,
    additive_force: Vector = Vector(0, 0), multiplicative_force_factor: Union[int, float] = 1):

    if shuffle:
        random.seed(seed)
        points = random.sample(points, len(points))
        sticks = random.sample(sticks, len(sticks))

    for p in points:
        if not p.isLocked:
            currentPos = p.loc
            p.loc += (p.loc - p.prevLoc + additive_force) * multiplicative_force_factor
            p.prevLoc = currentPos

    for i in range(num_iter):
        for stick in sticks:
            stickCentre = (stick.p1.loc + stick.p2.loc) / 2
            stickDir = (stick.p1.loc - stick.p2.loc).normalized()

            if (not stick.p1.isLocked) and (not stick.p2.isLocked):
                stick.p1.loc = stickCentre + (stickDir * (stick.length / 2))
                stick.p2.loc = stickCentre - (stickDir * (stick.length / 2))
            elif (not stick.p1.isLocked) and stick.p2.isLocked:
                stick.p1.loc = stick.p2.loc + (stickDir * stick.length)
            elif stick.p1.isLocked and (not stick.p2.isLocked):
                stick.p2.loc = stick.p1.loc - (stickDir * stick.length)