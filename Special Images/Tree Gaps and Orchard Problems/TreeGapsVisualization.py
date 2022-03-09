#Visualization for seeing which trees are visible to a person standing at origin
#Based on the following Numberphile video ('Tree Gaps and Orchard Problems - Numberphile'): https://youtu.be/p-xa-3V5KO8

import numpy as np
from matplotlib import pyplot as plt

def are_coprimes(a, b):
    mx = max(a, b)
    mn = min(a, b)

    if mn == 0:
        return True if mx == 1 else False
    if mn == 1:
        return True
    
    for i in range(2, mn + 1):
        if mx % i == 0:
            return False
            
    return True

def generate_img(size):
    img = []
    for i in range(size, -1, -1):
        row = []
        for j in range(size + 1):
            if (i == 0) and (j == 0):
                row.append([1.0, 0.0, 0.0])
            elif are_coprimes(i, j):
                row.append([1.0, 1.0, 1.0])
            else:
                row.append([0.0, 0.0, 0.0])
        img.append(row)

    return img

def save_image(img, size, grid = False, dpi = 200, figsize = (16, 16)):
    plt.figure(figsize = figsize)
    plt.imshow(img)
    
    if grid:
        ax = plt.gca()
        ax.grid(linewidth = 1)

        ax.set_xticks(np.arange(-0.5, size, 1))
        ax.set_yticks(np.arange(-0.5, size, 1))

        ax.set_xticklabels([])
        ax.set_yticklabels([])

        for axi in (ax.xaxis, ax.yaxis):
            for tick in axi.get_major_ticks():
                tick.tick1line.set_visible(False)
                tick.tick2line.set_visible(False)
                tick.label1.set_visible(False)
                tick.label2.set_visible(False)
    
    else:
        plt.axis(False)

    plt.savefig(f"Outputs/TreeGaps_{size}_{grid}.png", dpi = dpi, bbox_inches = 'tight')
    plt.close()

SIZES = [20, 50, 100, 200]
GRIDS = [True, False]
FIGSIZE = (16, 16)
DPI = 200

for size in SIZES:
    for grid in GRIDS:
        img = generate_img(size)
        save_image(img, size, grid, DPI, FIGSIZE)
