import ImageEffects as imgEffect
import os

blurDegree = [3, 5]
colorSpectrum = ['R', 'G', 'B']
grayscaleModes = ['AVG', 'MAX', 'MEDIAN', 'MIN']
singleToneNoiseLevel = [25, 50]
multiToneNoiseLevel = [(100, 0, 0), (25, 50, 75), (30, 30, 30)]
pixelation = [10, 25]
vignetteOrder = [2, 3]
vignetteColor = ['B', 'W']
vignetteOffset = [(0, 0), (100, 100)]

for f in os.listdir('..\Test_Images'):
    fname, fext = os.path.splitext(f)
    fPath = "..\\Test_Images\\" + f

    #Blur
    for b in blurDegree:
        blurFileName = f"Results\\Blur\\{fname}_Blur_{b}{fext}"
        imgEffect.blur(fPath, blurFileName, b)

    #ColorSpectrum
    for c in colorSpectrum:
        colorFileName = f"Results\\ColorSpectrum\\{fname}_ColorSpectrum_{c}{fext}"
        imgEffect.isolateColorSpectrum(fPath, colorFileName, c)

    #Grayscale
    for m in grayscaleModes:
        grayscaleFileName = f"Results\\Grayscale\\{fname}_Grayscale_{m}{fext}"
        imgEffect.grayscale(fPath, grayscaleFileName, m)

    #Invert
    invertFileName = f"Results\\Invert\\{fname}_Invert{fext}"
    imgEffect.invert(fPath, invertFileName)

    #Noise
    for n in multiToneNoiseLevel:
        multiToneNoiseFileName = f"Results\\Noise\\{fname}_Noise_Multi_{n}{fext}"
        imgEffect.addMultitoneNoise(fPath, multiToneNoiseFileName, n)

    for n in singleToneNoiseLevel:
        singleToneNoiseFileName = f"Results\\Noise\\{fname}_Noise_Single_{n}{fext}"
        imgEffect.addSingletoneNoise(fPath, singleToneNoiseFileName, n)

    #Pixelate
    for p in pixelation:
        pixelateFileName = f"Results\\Pixelate\\{fname}_Pixelate_{p}{fext}"
        imgEffect.pixelate(fPath, pixelateFileName, p)

    #Vignette
    for color in vignetteColor:
        for order in vignetteOrder:
            for offset in vignetteOffset:
                vignetteFileName = f"Results\\Vignette\\{fname}_Vignette_{color}_{order}_{offset}{fext}"
                imgEffect.vignette(fPath, vignetteFileName, color, order, offset)