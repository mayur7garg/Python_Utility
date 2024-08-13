import numpy as np
import random
from VerletClasses import Vector, Point, Stick
from VerletIntegration import simulate
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List

SHUFFLE = False
RANDOM_SEED = 7
LOCKED_CHANCE = 0.05
NOISE_STRENGTH = 25
GRAVITY = Vector(0, -0.1)
FRICTION = 0.999
NUM_ITERATIONS = 4
RENDER_FRAMES = 600
FPS = 30
PLOT_LIM = [-160, 1240, -800, 600] #Keep Square plot to avoid simulations that look stretchy
SAVE_ANIM = True

points: List[Point] = []
sticks: List[Stick] = []

x = np.arange(0, 1081, 15)
y = (np.sin(x * (np.pi / 180)) * 150) + (np.random.random(size = len(x)) * NOISE_STRENGTH)

for i, j in zip(x, y):
    p = Point(Vector(i, j))

    if random.random() < LOCKED_CHANCE:
        p.isLocked = True

    points.append(p)

points[0].isLocked = True
points[-1].isLocked = True

for i in range(len(points) - 1):
    sticks.append(Stick(points[i], points[i + 1]))

def renderPoints(points: List[Point]):
    x: List[int] = list(map(lambda p: p.loc.x, points))
    y: List[int] = list(map(lambda p: p.loc.y, points))
    s: List[int] = list(map(lambda p: 20 if p.isLocked else 5, points))

    return x, y, s

fig, ax = plt.subplots()
ax.axis(PLOT_LIM)

scat = ax.scatter([], [], alpha = 0.6, s = 3)
linePlots = []
for stick in sticks:
    line, = ax.plot([], [], c = "green", alpha = 0.4)
    linePlots.append(line)

plt.axis(False)

def initRender():
    x, y, s = renderPoints(points)
    scat.set_offsets(list(zip(x, y)))
    scat.set_sizes(s)

    for linePlot, stick in zip(linePlots, sticks):
        linePlot.set_data([stick.p1.loc.x, stick.p2.loc.x], [stick.p1.loc.y, stick.p2.loc.y])

    return scat, *linePlots

def animateFrame(i):
    simulate(points, sticks, NUM_ITERATIONS, SHUFFLE, i * RANDOM_SEED, GRAVITY, FRICTION)
    return initRender()

if SAVE_ANIM:
    anim = FuncAnimation(fig, animateFrame, init_func = initRender, frames = RENDER_FRAMES, interval = 0, blit = True)
    anim.save('Rope.gif', fps = FPS)
else:
    anim = FuncAnimation(fig, animateFrame, init_func = initRender, frames = RENDER_FRAMES, interval = 0, blit = True, repeat = False)
    plt.show()