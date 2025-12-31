# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy==2.4.0",
#     "pillow==12.0.0",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")

with app.setup:
    import marimo as mo
    import numpy as np
    from PIL import Image

    size = (384, 216)
    num_swaps = 1_000_000
    swap_range = 3
    save_every = 250
    disp_mul = 2
    optimal = True


@app.function
def identify_swap(
    img_1,
    img_2,
    p_r,
    p_c,
    optimal = False
):
    best_improvement, best_i, best_j = 0, 0, 0
    
    for i in range(-swap_range, swap_range + 1):
        for j in range(-swap_range, swap_range + 1):
    
    
            curr_diff = (
                np.abs(img_2[p_r][p_c] - img_1[p_r][p_c]).sum() +
                np.abs(img_2[p_r + i][p_c + j] - img_1[p_r + i][p_c + j]).sum()
            )
            swap_diff = (
                np.abs(img_2[p_r + i][p_c + j] - img_1[p_r][p_c]).sum() +
                np.abs(img_2[p_r][p_c] - img_1[p_r + i][p_c + j]).sum()
            )
            
            improvement = curr_diff - swap_diff

            # print(img_1[p_r][p_c])
            # print(img_1[p_r + i][p_c + j])
            # print(img_2[p_r][p_c])
            # print(img_2[p_r + i][p_c + j])
            # print(np.abs(img_2[p_r + i][p_c + j] - img_1[p_r][p_c]))
            # print(np.abs(img_2[p_r][p_c] - img_1[p_r + i][p_c + j]))
    
            if improvement > best_improvement:
                if optimal:
                    best_improvement = improvement
                    best_i = i
                    best_j = j
                else:
                    return i, j, improvement
                
    return best_i, best_j, best_improvement


@app.cell
def _():
    img_1 = np.array(
        Image.open(r"..\Test_Images\Img_02.jpg").convert('RGB').resize(size)
    ).astype('int32')
    mo.image(img_1, width = size[0] * disp_mul, height = size[1] * disp_mul)
    return (img_1,)


@app.cell
def _():
    img_2 = np.array(
        Image.open(r"..\Test_Images\Img_01.jpg").convert('RGB').resize(size)
    ).astype('int32')
    print(img_2.sum(), img_2.shape)
    mo.image(img_2, width = size[0] * disp_mul, height = size[1] * disp_mul)
    return (img_2,)


@app.cell
def _(img_1, img_2):
    valid_swaps = 0
    anim_snapshots = [Image.fromarray(img_2.astype('uint8'))]

    rnd_p_r = np.random.randint(swap_range, size[1] - swap_range, size = num_swaps)
    rnd_p_c = np.random.randint(swap_range, size[0] - swap_range, size = num_swaps)

    for s_i in mo.status.progress_bar(range(num_swaps)):
        p_r = rnd_p_r[s_i]
        p_c = rnd_p_c[s_i]

        curr_px = img_2[p_r][p_c].copy()
        swap_i, swap_j, improvement = identify_swap(img_1, img_2, p_r, p_c, optimal = optimal)

        # print(p_r, p_c, curr_px)
        # print(swap_i, swap_j, improvement)
    
        if improvement > 0:
            valid_swaps += 1
            img_2[p_r][p_c] = img_2[p_r + swap_i][p_c +  swap_j]
            img_2[p_r + swap_i][p_c +  swap_j] = curr_px

            if valid_swaps % save_every == 0:
                anim_snapshots.append(Image.fromarray(img_2.astype('uint8')))
            
    anim_snapshots.append(Image.fromarray(img_2.astype('uint8')))

    print(img_2.sum())
    print(valid_swaps)
    print(len(anim_snapshots))
    mo.image(img_2, width = size[0] * disp_mul, height = size[1] * disp_mul)
    return (anim_snapshots,)


@app.cell
def _(anim_snapshots):
    anim_snapshots[0].save(
        "out.gif",
        save_all = True,
        append_images = anim_snapshots[1:],
        duration = 100,
        loop = 0
    )
    mo.image("out.gif", width = size[0] * disp_mul, height = size[1] * disp_mul)
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
