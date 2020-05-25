# Image Manipulation using Pillow (Python)
Contains scripts to manipulate an image by applying any of the following effects:
* Blur
* Isolating the RGB color spectrum 
* Grayscale
* Invert
* Noise
* Pixelate
* Vignette

## Note
These scripts modify an image at the pixel level and hence are quite inefficient for usage in production. If you are looking for using such effects in any of your applications, I suggest you look up for more optimised solutions.

> Implementation of Blur, Noise and Vignette effects will be optimised in the upcoming changes.

## Effects and their Parameters
This module consists of two scripts:
* **`ImageEffects.py`** - This contains the functions which are used to apply the forementioned effects to the images.
* **`ImageUtilityMethods.py`** - This contains the utility methods which are called from inside the `ImageEffects.py`.


All effect functions in `ImageEffects.py` take first parameter as the path(including full name of the file) of the image file on which the effect is to be applied. The second parameter as the path(including full name of the file) where the resultant image will be saved. If a file already exists at this path, then it would be overwritten by the new image file. The original image is never modified.

`Main.py` contains examples depicting how these effects have been applied to all of the images in **Test_Images** folder and the resulant images stored in **Results** folder.
> Developed by - Mayur Kr. Garg