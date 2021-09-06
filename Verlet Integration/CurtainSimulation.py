from VerletClasses import Vector, Point, Stick
from VerletIntegration import simulate
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from typing import List

X_DIM = 153
Y_DIM = 100
ANCHORS_X = set(i for i in range(1, X_DIM - 1, 25))
SHUFFLE = True
RANDOM_SEED = 7
GRAVITY = Vector(0, -0.012)
FRICTION = 0.999
NUM_ITERATIONS = 3
RENDER_FRAMES = 720
FPS = 30
PLOT_LIM = [-5, X_DIM + 4, -60, Y_DIM] #Keep Square plot to avoid simulations that look stretchy
SAVE_ANIM = True

def renderPoints(points: List[Point]):
    x: List[int] = list(map(lambda p: p.loc.x, points))
    y: List[int] = list(map(lambda p: p.loc.y, points))
    s: List[int] = list(map(lambda p: 20 if p.isLocked else 1, points))

    return x, y, s

points: List[Point] = []
sticks: List[Stick] = []

for i in range(X_DIM):
    for j in range(Y_DIM):
        locked = False
        if j == Y_DIM - 1 and i in ANCHORS_X:
            locked = True
        p = Point(Vector(i, j), locked)
        points.append(p)

for i in range(X_DIM):
    for j in range(Y_DIM):
        point = points[(i * Y_DIM) + j]

        if i < X_DIM - 1:
            pointRight = points[(Y_DIM * (i + 1)) + j]
            sticks.append(Stick(point, pointRight))

        if j < Y_DIM - 1:
            pointUp = points[(Y_DIM * i) + j + 1]
            sticks.append(Stick(point, pointUp))

fig, ax = plt.subplots()
ax.axis(PLOT_LIM)

scat = ax.scatter([], [], alpha = 0.5, s = 1)
linePlots = []
for stick in sticks:
    line, = ax.plot([], [], c = "green", alpha = 0.3)
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
    anim = FuncAnimation(fig, animateFrame, init_func = initRender, frames = RENDER_FRAMES, blit = True, save_count = RENDER_FRAMES)
    anim.save('Curtain.gif', fps = FPS)
else:
    anim = FuncAnimation(fig, animateFrame, init_func = initRender, frames = RENDER_FRAMES, interval = 10, blit = True, save_count = RENDER_FRAMES)
    plt.show()