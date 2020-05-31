from random import randint

class PixelReferenceContainer():
    def __init__(self, original, new):
        self.original = original
        self.new = new

def getAvgColor(lstPixels):
    r = 0
    g = 0
    b = 0
    count = len(lstPixels)

    for pixRGB in lstPixels:
        r += pixRGB[0]
        g += pixRGB[1]
        b += pixRGB[2]

    r = r//count
    g = g//count
    b = b//count
    
    return (r, g, b)

def getColorSpectrumIndex(colorSpectrum):
    colorSpectrum = colorSpectrum.strip().upper()
    
    if colorSpectrum == "R" or colorSpectrum == "RED":
        return 0
    elif colorSpectrum == "G" or colorSpectrum == "GREEN":
        return 1
    elif colorSpectrum == "B" or colorSpectrum == "BLUE":
        return 2
    else:
        raise ValueError("Invalid value of 'colorSpectrum' variable. The accepted values are: 'R', 'G', 'B', 'RED', 'GREEN' or 'BLUE'.")

def getGrayscaleColorForPixel(pix, x, y, grayscaleFunc):
    grayscale = grayscaleFunc(pix[x, y])
    return (grayscale, grayscale, grayscale)

def getGrayscaleFunc(mode):
    mode = mode.strip().upper()

    if mode == "AVG":
        return lambda rgb : sum(rgb)//len(rgb)
    elif mode == "MAX":
        return max
    elif mode == "MEDIAN":
        return lambda rgb : sorted(rgb)[1]
    elif mode == "MIN":
        return min
    else:
        raise ValueError("Invalid value of 'mode' variable. The accepted values are: 'AVG', 'MAX', 'MEDIAN' or 'MIN'.")

def getInvertColor(pix, x, y):
    (r, g, b) = pix[x, y]
    return (255 - r, 255 - g, 255 - b)

def getMaxDistanceFromCentralPt(centralPt, order):
    maxDistance = centralPt[0] ** order + centralPt[1] ** order
    return maxDistance

def getNearbyPixels(pix, x, y, blockSize, size):
    xMin = max(0, x - blockSize)
    xMax = min(size[0], x + blockSize + 1)
    yMin = max(0, y - blockSize)
    yMax = min(size[1], y + blockSize + 1)

    return [pix[i, j] for i in range(xMin, xMax) for j in range(yMin, yMax)]

def getNoiseFunc(noiseLevel, isWhite):
    whiteNoise = lambda tone, noise : min(max(tone + noise, 0), 255)
    randomNoise = lambda tone, level : min(max(tone + randint(-level, level), 0), 255)

    def addWhiteNoise(rgb):
        noise = randint(-noiseLevel, noiseLevel)
        return (whiteNoise(rgb[0], noise), whiteNoise(rgb[1], noise), whiteNoise(rgb[2], noise))

    def addRandomNoise(rgb):
        return (randomNoise(rgb[0], noiseLevel), randomNoise(rgb[1], noiseLevel), randomNoise(rgb[2], noiseLevel))

    if isWhite:
        return addWhiteNoise
    else:
        return addRandomNoise

def getPixelBlockForCornerPixel(pix, x, y, blockSize, size):
    xMax = min(size[0], x + blockSize)
    yMax = min(size[1], y + blockSize)

    return [pix[i, j] for i in range(x, xMax) for j in range(y, yMax)]

def getRelativeDistanceFromCentralPt(xDist, yDist, offset, order, maxDistance):
    distance = ((xDist + offset[0]) ** order) + ((yDist + offset[1]) ** order)
    return min(distance/maxDistance, 1)

def getSingleColorSpectrumForPixel(pix, x, y, colorIndex):
    color = [0, 0, 0]
    color[colorIndex] = pix[x, y][colorIndex]
    return tuple(color)

def getVignetteFunc(colorCode):
    blackVignette = lambda rgb, relativeDistance : int(rgb - (relativeDistance * rgb))
    whiteVignette = lambda rgb, relativeDistance : int(rgb + relativeDistance * (255 - rgb))

    def blackVignetteFunc(rgb, relativeDistance):
        if relativeDistance == 1:
            return (0, 0, 0)
        else:
            return (blackVignette(rgb[0], relativeDistance), blackVignette(rgb[1], relativeDistance), blackVignette(rgb[2], relativeDistance))

    def whiteVignetteFunc(rgb, relativeDistance):
        if relativeDistance == 1:
            return (255, 255, 255)
        else:
            return (whiteVignette(rgb[0], relativeDistance), whiteVignette(rgb[1], relativeDistance), whiteVignette(rgb[2], relativeDistance))

    colorCode = colorCode.strip().upper()

    if colorCode == 'B' or colorCode == 'BLACK':
        return blackVignetteFunc
    elif colorCode == 'W' or colorCode == 'WHITE':
        return whiteVignetteFunc
    else:
        raise ValueError("Invalid value of 'colorCode' variable. The accepted values are: 'B', 'W', 'BLACK', or 'WHITE'.")
