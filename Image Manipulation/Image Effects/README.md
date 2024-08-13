# Image Effects using Pillow (Python)
Contains scripts to manipulate an image by applying any of the following effects:
* Blur
* Isolating the RGB color spectrum 
* Grayscale
* Invert
* Noise
* Pixelate
* Vignette

## Note
These scripts modify an image at the pixel level and hence are quite inefficient for usage in production. This is mostly meant for learning or experimental purposes. If you are looking for using such effects in any of your applications, I suggest you look up for more optimised solutions.

> Implementation of Blur, Noise and Vignette effects will be optimised in the upcoming changes.

## Effects and their Parameters
This module consists of two scripts:
* **`ImageEffects.py`** - This contains the functions which are used to apply the forementioned effects to the images.
* **`ImageUtilityMethods.py`** - This contains the utility methods which are called from inside the `ImageEffects.py`.


All effect functions in `ImageEffects.py` take first parameter as the path (relative to `ImageEffects.py` and including the full name) of the image file on which the effect is to be applied. The second parameter is the path (relative to `ImageEffects.py` and including the full name)) where the resultant image will be saved. If a file already exists at this path, then it would be overwritten by the new image file. The original image is never modified.

`Main.py` contains examples depicting how these effects have been applied to all of the images in **Test_Images** folder and the resulant images stored in **Results** folder.

### Blur
The Blur effect is applied using the `blur` function. Apart from the name of the original and resultant image file, it takes the following arguments:

* **blurDegree** - Required. Must be a positive integer value. Denotes the degree by which the image is to be blurred. A high value of `blurDegree` leads to poor performance as the time taken to blur an image scales rapidly by a factor of `(2*blurDegree + 1)^2`.

### Isolating the RGB color spectrum 
This effect is used to isolate any one of R,G or B spectrum from the image. It is applied using the `isolateColorSpectrum` method which, apart from the name of the original and resultant image file, it takes the following arguments:

* **colorSpectrum** - Required. Must be one of the following string values - 'R', 'G', 'B', 'RED', 'GREEN' or 'BLUE'. Denotes the color spectrum to be isolated.

### Grayscale
This effect is used to turn an image containing multitude of colors to a one containing only shades of gray and is applied using the `grayscale` method. Apart from the name of the original and resultant image file, it takes the following arguments:

* **mode** - Required. Must be one of the following string values - 'AVG', 'MAX', 'MEDIAN' or 'MIN'. Denotes the method used to calculate the gray tone of each pixel.

    * AVG - Gray tone of each pixel is the average of its R, G and B pixel values.
    * MAX - Gray tone of each pixel is the maximum of its R, G and B pixel values.
    * MEDIAN - Gray tone of each pixel is the median of its R, G and B pixel values.
    * MIN - Gray tone of each pixel is the minimum of its R, G and B pixel values.

### Invert
This image is used to invert the color of each pixel of the image. This effect is applied using the `invert` method and takes no additional argument than the two file names.

### Noise
This effect is used to add noise to each pixel of the image. For this effect, there are two functions defined - `addMultitoneNoise` and `addSingletoneNoise`. For single tone noise, each of the R, G and B value for a particular pixel is modified by the same amount. For multi tone noise, each of the R, G and B value for a particular pixel is modified by a different amount. Apart from the name of the original and resultant image file, they take the following arguments:

* **noiseLevel** - Required. Must be an integer value for `addSingletoneNoise` and a tuple/list of 3 integer values for `addMultitoneNoise` methods respectively. Denotes the maximum amount by which the value of R, G and B for a pixel will be altered.

### Pixelate
The Pixelate effect is applied using the `pixelate` method. Apart from the name of the original and resultant image file, it takes the following arguments:

* **pixelation** - Required. Must be a positive integer value. Denotes the size of the pixelated blocks in the resultant image. The higher this value, the quicker the effect.

### Vignette
The Vignette effect is applied using the `vignette` method. Apart from the name of the original and resultant image file, it takes the following arguments:

* **colorCode** - Optional. Must be one of the following string values - 'B', 'W', 'BLACK', or 'WHITE'. Default value is 'B'. Denotes the color of the vignette effect.

* **order** - Optional. Must be a positive integer value. Default value is 2. Denotes how prominent the boundary of the vignette effect is.

* **offset** - Optional. Must be a tuple/list of two integer values. Default value is (0, 0). Denotes the pixels by which the vignette effect is shifted towards the center on the X and Y axis.

## Python concepts used
This module makes use of the following Python concepts - 
* PIL (Pillow) module
* Decorators
* Lambda functions
* Functions as objects
* Nested functions
* Raising exceptions
* Reading and saving files
* Code modularity

> Developed by - Mayur Kr. Garg