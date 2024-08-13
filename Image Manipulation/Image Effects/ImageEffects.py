from PIL import Image
from random import randint
import ImageUtilityMethods as util
import time

def imageEffect(effect_func):

    def applyEffectAndSave(originalFile, newFile, *args):
        startTime = time.time()

        originalImg = Image.open(originalFile)
        size = originalImg.size

        newImg = Image.new("RGB", size, (255, 255, 255))

        pix = util.PixelReferenceContainer(originalImg.load(), newImg.load())

        effect_func(pix, size, *args)

        newImg.save(newFile)

        print(f"Added {newFile}. Took {round(time.time() - startTime, 2)}s.")
    return applyEffectAndSave

@imageEffect
def addMultitoneNoise(pix, size, noiseLevel):
    noiseFunc = util.getNoiseFunc(noiseLevel, False)
    original = pix.original
    
    for x in range(size[0]):
        for y in range(size[1]):
            pix.new[x, y] = noiseFunc(original[x, y])  

@imageEffect
def addSingletoneNoise(pix, size, noiseLevel):
    noiseFunc = util.getNoiseFunc(noiseLevel, True)
    original = pix.original
    
    for x in range(size[0]):
        for y in range(size[1]):
            pix.new[x, y] = noiseFunc(original[x, y])    

@imageEffect
def blur(pix, size, blurDegree):
    getAvgColor = util.getAvgColor
    getNearbyPixels = util.getNearbyPixels
    original = pix.original
    new = pix.new

    for x in range(size[0]):
        for y in range(size[1]):
            new[x, y] = getAvgColor(getNearbyPixels(original, x, y, blurDegree, size))

@imageEffect
def grayscale(pix, size, mode):
    grayscaleFunc = util.getGrayscaleFunc(mode)

    for x in range(size[0]):
        for y in range(size[1]):
            pix.new[x, y] = util.getGrayscaleColorForPixel(pix.original, x, y, grayscaleFunc)

@imageEffect
def invert(pix, size):
    for x in range(size[0]):
        for y in range(size[1]):
            pix.new[x, y] = util.getInvertColor(pix.original, x, y)

@imageEffect
def isolateColorSpectrum(pix, size, colorSpectrum):
    colorIndex = util.getColorSpectrumIndex(colorSpectrum)
    for x in range(size[0]):
        for y in range(size[1]):
            pix.new[x, y] = util.getSingleColorSpectrumForPixel(pix.original, x, y, colorIndex)

@imageEffect
def pixelate(pix, size, pixelation):
    for y in range(0, size[1], pixelation):
        for x in range(0, size[0], pixelation):
            pixelColor = util.getAvgColor(util.getPixelBlockForCornerPixel(pix.original, x, y, pixelation, size))

            xMax = min(size[0], x + pixelation)
            yMax = min(size[1], y + pixelation)

            for i in range(x, xMax):
                for j in range(y, yMax):
                    pix.new[i, j] = pixelColor

@imageEffect
def vignette(pix, size, colorCode = 'B', order = 2, offset = (0, 0)):
    order = int(order)
    if order < 1:
        raise ValueError("Invalid value of 'scale' variable. The accepted value is any positive integer.")

    centralPt = (size[0]//2, size[1]//2)
    maxDistance = util.getMaxDistanceFromCentralPt(centralPt, order)
    vignetteFunc = util.getVignetteFunc(colorCode)

    original = pix.original
    new = pix.new

    relDistDict = {}

    for x in range(size[0]):
        for y in range(size[1]):
            xDist = abs(centralPt[0] - x)
            yDist = abs(centralPt[1] - y )

            relativeDist = relDistDict.get((xDist, yDist))
            
            if relativeDist is None:
                relativeDist = util.getRelativeDistanceFromCentralPt(xDist, yDist, offset, order, maxDistance)
                relDistDict[(xDist, yDist)] = relativeDist

            new[x, y] = vignetteFunc(original[x, y], relativeDist)