# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy==2.4.0",
#     "pillow==12.0.0",
#     "scipy==1.16.3",
# ]
# ///

import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium", layout_file="layouts/SeamCarving.grid.json")

with app.setup:
    import marimo as mo
    import numpy as np
    from scipy.ndimage import convolve
    from PIL import Image

    filter_du = np.array([
        [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])
    # This converts it from a 2D filter to a 3D filter, replicating the same
    # filter for each channel: R, G, B
    filter_du = np.stack([filter_du] * 3, axis=2)

    filter_dv = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])
    # This converts it from a 2D filter to a 3D filter, replicating the same
    # filter for each channel: R, G, B
    filter_dv = np.stack([filter_dv] * 3, axis=2)# Initialization code that runs before all other cells


@app.cell
def _():
    mo.md(r"""
    # Seam Carving
    """)
    return


@app.cell
def _():
    mo.md(r"""
    ## Reference: https://karthikkaranth.me/blog/implementing-seam-carving-with-python/
    """)
    return


@app.cell
def _():
    mo.md(r"""
    ## Utility functions
    """)
    return


@app.function
def calc_energy(img):
    global filter_du, filter_dv

    img = img.astype('float32')
    convolved = np.absolute(convolve(img, filter_du)) + np.absolute(convolve(img, filter_dv))

    # We sum the energies in the red, green, and blue channels
    energy_map = convolved.sum(axis=2)

    return energy_map


@app.function
def minimum_seam(img):
    r, c, _ = img.shape
    energy_map = calc_energy(img)

    M = energy_map.copy()
    backtrack = np.zeros_like(M, dtype = int)

    for i in range(1, r):
        for j in range(0, c):
            # Handle the left edge of the image, to ensure we don't index a -1
            if j == 0:
                idx = np.argmin(M[i-1, j:j + 2])
                backtrack[i, j] = idx + j
                min_energy = M[i-1, idx + j]
            else:
                idx = np.argmin(M[i - 1, j - 1:j + 2])
                backtrack[i, j] = idx + j - 1
                min_energy = M[i - 1, idx + j - 1]

            M[i, j] += min_energy

    return M, backtrack


@app.function
def carve_column(img):
    r, c, _ = img.shape

    M, backtrack = minimum_seam(img)
    mask = np.ones((r, c), dtype = bool)

    j = np.argmin(M[-1])
    for i in reversed(range(r)):
        mask[i, j] = False
        j = backtrack[i, j]

    mask = np.stack([mask] * 3, axis=2)
    img = img[mask].reshape((r, c - 1, 3))
    return img


@app.function
def crop_c(img, scale_c):
    r, c, _ = img.shape
    new_c = int(scale_c * c)

    for i in mo.status.progress_bar(
        range(c - new_c),
        title = "Carving image",
        subtitle = "Please wait",
        show_eta = True,
        show_rate = True,
        remove_on_exit = True
    ):
        img = carve_column(img)

    return img


@app.function
def crop_r(img, scale_r):
    img = np.rot90(img, 1, (0, 1))
    img = crop_c(img, scale_r)
    img = np.rot90(img, 3, (0, 1))
    return img


@app.cell
def _():
    mo.md(r"""
    ## Carving image
    """)
    return


@app.cell
def _():
    img_selector = mo.ui.file_browser(
        multiple = False,
        filetypes = [".png", ".jpg", ".jpeg"],
        label = "Select image"
    )

    col_row_selector = mo.ui.radio(
        options = ["columns", "rows"],
        value = "columns",
        label = "Select axis to carve"
    )

    scale_slider = mo.ui.slider(
        start = 0.5,
        stop = 0.99,
        step = 0.01,
        value = 0.9,
        label = "Select relative scale of carved image",
        full_width = True
    )

    def validate_form(form_value):
        if len(form_value['img_selector']) < 1:
            return "No image selected"

    form = mo.md("""
        {img_selector}
    
        {col_row_selector}
    
        {scale_slider}
    """).batch(
        img_selector = img_selector,
        col_row_selector = col_row_selector,
        scale_slider = scale_slider
    ).form(
        submit_button_label = "Carve",
        show_clear_button = True,
        validate = validate_form
    )

    form
    return (form,)


@app.cell
def _(form):
    mo.stop(not form.value, "Submit the form above to run")

    img_path = form.value['img_selector'][0].path
    img = Image.open(img_path)
    mo.vstack([
        mo.md(f"### Selected image: {img_path.stem}"),
        mo.md(f"#### Size: {img.width} X {img.height}"),
        img
    ])
    return (img,)


@app.cell
def _(form, img):
    img_array = np.array(img)
    which_axis = form.value['col_row_selector']
    scale = form.value['scale_slider']

    if which_axis == 'columns':
        carved_img = crop_c(img_array, scale)
    elif which_axis == 'rows':
        carved_img = crop_r(img_array, scale)

    carved_img = Image.fromarray(carved_img)

    mo.vstack([
        mo.md("### Carved image"),
        mo.md(f"#### Size: {carved_img.width} X {carved_img.height}"),
        carved_img
    ])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
