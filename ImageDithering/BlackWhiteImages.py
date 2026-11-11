from PIL import Image
from pathlib import Path

def ditherImage(image):
    image = image.resize((128, 64), Image.Resampling.LANCZOS)
    myImage2 = image.convert("L")


    imageX, imageY = myImage2.size[0], myImage2.size[1]

    def addToPixel(coord, diff):
        currentBrightness = myImage2.getpixel(coord)
        adjustedBrightness = currentBrightness + (diff)
        adjustedBrightness = max(0, min(adjustedBrightness, 255))
        return round(adjustedBrightness)


    for i in range(imageY):
        for j in range(imageX):
            ogBrightness = myImage2.getpixel((j, i))
            newBrightness = 0

            if ogBrightness >= 128:
                newBrightness = 255

            difference = ogBrightness - newBrightness

            tl = (j, i)
            tr = (j + 1, i)
            b = (j, i + 1)
            br = (j + 1, i + 1)

            myImage2.putpixel(tl, newBrightness)

            if j + 1 < imageX:
                myImage2.putpixel(tr, addToPixel(tr, difference * 7/16))

            if i + 1 < imageY:
                myImage2.putpixel(b, addToPixel(b, difference * 5/16))

            if j + 1 < imageX and i + 1 < imageY:
                myImage2.putpixel(br, addToPixel(br, difference * 1/16))

            if j > 0 and i + 1 < imageY:
                bl = (j - 1, i + 1)
                myImage2.putpixel(bl, addToPixel(bl, difference * 3/16))
    return myImage2