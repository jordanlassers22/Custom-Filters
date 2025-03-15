# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:21:25 2022

@author: Jordan
"""

import image
import math

def convert_pixel_to_gray(pixel):
    '''Converts an individual pixel to gray intensity.'''
    tot_intensity = pixel.getRed() + pixel.getGreen() + pixel.getBlue()
    avg_intensity = tot_intensity // 3
    bst_intensity = min(avg_intensity, 255)
    pixel = image.Pixel(bst_intensity, bst_intensity, bst_intensity)
    return pixel

def convertPixelToSepia(oldPixel):
    '''Converts an individual pixel to sepia'''
    newR = min(int(oldPixel.getRed() * 0.393 + oldPixel.getGreen() * 0.769 + oldPixel.getBlue() * 0.189),255)
    newG = min(int(oldPixel.getRed() * 0.349 + oldPixel.getGreen() * 0.686 + oldPixel.getBlue() * 0.168),255)
    newB = min(int(oldPixel.getRed() * 0.272 + oldPixel.getGreen() * 0.534 + oldPixel.getBlue() * 0.131),255)
    return image.Pixel(newR, newG, newB)

def convolve(originalImage, pixelRow, pixelCol, kernel):
    '''Convolves a row and column based on a given kernel.'''
    kernelColBase = pixelCol - 1
    kernelRowBase = pixelRow - 1
    total = 0
    for row in range(kernelRowBase, kernelRowBase+3):
        for col in range(kernelColBase, kernelColBase+3):
            kColIndex = col - kernelColBase
            kRowIndex = row - kernelRowBase
            pixel = originalImage.getPixel(col, row)
            intensity = pixel.getRed()
            total = total + intensity * kernel[kRowIndex][kColIndex]
    return total

def make_grayscale(original_image, width, height):
    '''Converts an image to grayscale.'''
    modified_image = image.EmptyImage(width, height)

    for row in range(height):
        for col in range(width):
            pixel = original_image.getPixel(col, row)
            pixel = convert_pixel_to_gray(pixel)
            modified_image.setPixel(col, row, pixel)

    modified_image.setPosition(0, 0)
    return modified_image

def make_sepia(original_image, width, height):
    '''Converts an image to sepia.'''
    width = original_image.getWidth()
    height = original_image.getHeight()
    modified_image = image.EmptyImage(width, height)

    for row in range(height):
        for col in range(width):
            pixel = original_image.getPixel(col, row)
            pixel = convertPixelToSepia(pixel)
            modified_image.setPixel(col, row, pixel)
 
    modified_image.setPosition(width + 1, 0)
    return modified_image

def edgeDetect(originalImage, width, height):
    '''Detects the edges of an image, and outlines it in a returned new image.'''
    grayscale = make_grayscale(originalImage, width, height)

    edgeImage = image.EmptyImage(originalImage.getWidth(), originalImage.getHeight())
    black = image.Pixel(0, 0, 0)
    white = image.Pixel(255, 255, 255)
    xMask = [ [-1, -2, -1], [0, 0, 0], [1,2,1] ]
    yMask = [ [1, 0, -1], [2, 0, -2], [1,0,-1] ]
    
    for row in range(1, originalImage.getHeight()-1):
        for col in range(1, originalImage.getWidth()-1):
            gX = convolve(grayscale, row, col, xMask)
            gY = convolve(grayscale, row, col, yMask)
            g = math.sqrt(gX**2 + gY**2)
            if g > 175:
                edgeImage.setPixel(col, row, black)
            else:
                edgeImage.setPixel(col, row, white) 
    edgeImage.setPosition((width * 2) + 2, 0)
    return edgeImage

def makeNegative(original_image, width, height):
    '''Converts an image to negative intensity.'''
    negative = image.EmptyImage(width, height)
    for row in range(height):                                   
        for col in range(width):                                
            pixel = original_image.getPixel(col, row)
            r = 255 - pixel.getRed()
            g = 255 - pixel.getGreen()
            b = 255 - pixel.getBlue()
            pixel = image.Pixel(r, g, b)
            negative.setPixel(col, row, pixel)
    negative.setPosition(0, height + 1)
    return negative

def makeSwapRGB(original_image, width, height):
    '''Custom filter that swaps the rgb values of an image with eachother.'''
    newImage = image.EmptyImage(width, height)
    for row in range(height):                                   
        for col in range(width):                               
            pixel = original_image.getPixel(col, row)
            tempR = pixel.getRed()
            tempG = pixel.getGreen()
            tempB = pixel.getBlue()
            r = tempG
            g = tempB
            b = tempR
            pixel = image.Pixel(r, g, b)
            newImage.setPixel(col, row, pixel)
    newImage.setPosition((width * 2) + 2, height + 1)
    return newImage

def makeHorizontalFlip(originalImage, width, height):
    '''Flips an image over the y axis'''
    height = originalImage.getHeight()
    width = originalImage.getWidth()
    last = width - 1
    
    flippedImage = image.EmptyImage(width, height)
    for x in range(width):
        for y in range(height):
            pixel = originalImage.getPixel(last - x, y)
            flippedImage.setPixel(x, y, pixel)
    flippedImage.setPosition(0, (height * 2) + 2)
    return flippedImage

def makeMirror(originalImage, width, height):
    '''Mirrors an image over the y axis'''
    height = originalImage.getHeight()
    width = originalImage.getWidth()
    last = width - 1
    
    flippedImage = image.EmptyImage(width, height)
    for x in range(width):
        for y in range(height):
            if x < width / 2:
                pixel = originalImage.getPixel(x,y)
                flippedImage.setPixel(x, y, pixel)
            else:
                pixel = originalImage.getPixel(last - x, y)
                flippedImage.setPixel(x, y, pixel)
    flippedImage.setPosition(width + 1, (height * 2) + 2)
    return flippedImage

def makeBlur(originalImage, width, height):
    '''Blurs an image'''
    mask = [[1,2,1], [2,1,2], [1,2,1]]
    blurredImage = image.EmptyImage(width, height)
    for x in range(width): #Sets background of image to black to match collage image background
        for y in range(height):
            pixel = image.Pixel(0, 0, 0)
            blurredImage.setPixel(x, y, pixel)
    for pixel_x in range(1,width - 1):
        for pixel_y in range(1,height - 1):
            r = 0
            g = 0
            b = 0
            for mask_x in range(0,len(mask)):
                for mask_y in range(0,len(mask)):
                    pixel = originalImage.getPixel(pixel_x + mask_x - 1, pixel_y + mask_y - 1)
                    r += mask[mask_x][mask_y] * pixel.getRed()
                    g += mask[mask_x][mask_y] * pixel.getGreen()
                    b += mask[mask_x][mask_y] * pixel.getBlue()
            blurredPixel = image.Pixel(math.floor(r/13), math.floor(g/13), math.floor(b/13))
            blurredImage.setPixel(pixel_x, pixel_y, blurredPixel)
            blurredImage.setPosition((width * 2) + 1, (height * 2) + 2)
    return blurredImage

def makeBackground(width, height):
    '''Creates a black background over a canvas that is 3 times the size of an original image.'''
    newWidth = width * 3 + 2
    newHeight = height * 3 + 2
    newImage = image.EmptyImage(newWidth, newHeight)
    for x in range(newWidth):
        for y in range(newHeight):
            pixel = image.Pixel(0, 0, 0)
            newImage.setPixel(x, y, pixel)
    return newImage

#Creates black background first, and then adds in pictures
img = image.FileImage("flower.jpg")
oWidth = img.getWidth()
oHeight = img.getHeight()
win = image.ImageWin(oWidth * 3 + 2, oHeight * 3 + 2, "Collage Project")
background = makeBackground(oWidth, oHeight)
background.draw(win)
grayscale = make_grayscale(img, oWidth, oHeight)
sepia = make_sepia(img, oWidth, oHeight)
negative = makeNegative(img, oWidth, oHeight)
edgeDetection = edgeDetect(img, oWidth, oHeight)
verticalFlip = makeHorizontalFlip(img, oWidth, oHeight)
swapRGB = makeSwapRGB(img, oWidth, oHeight)
mirror = makeMirror(img, oWidth, oHeight)
blur = makeBlur(img, oWidth, oHeight)
sepia.draw(win)
grayscale.draw(win)
negative.draw(win)
edgeDetection.draw(win)
img.setPosition(oWidth + 1, oHeight + 1)
img.draw(win)
swapRGB.draw(win)
verticalFlip.draw(win)
mirror.draw(win)
blur.draw(win)

win.exitonclick()

