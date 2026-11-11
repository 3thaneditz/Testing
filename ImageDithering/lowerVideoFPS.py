import subprocess
from PIL import Image
from pathlib import Path
import os
import shutil
from BlackWhiteImages import ditherImage

def convertVideoFully(path, updateProgress):
    if Path("frames").exists():
        shutil.rmtree("frames")

    Path("frames").mkdir(exist_ok=True)

    command = [
        'ffmpeg',
        '-y',
        '-i', path,
        '-vf', f'fps={15}',
        '-c:a', 'copy',
        "tempVideo.mp4"
    ]

    subprocess.run(command, check=True)

    command2 = [
        "ffmpeg",
        "-i", "tempVideo.mp4",
        "frames/frame_%05d.png"
    ]

    subprocess.run(command2, check=True)

    totalFrames = len(list(Path("frames").glob("*.png")))
    processedFrames = 0

    for frame in Path("frames").iterdir():
        targetFrame = Image.open(frame)
        ditheredFrame = ditherImage(targetFrame)
        ditheredFrame.save(frame)
        processedFrames += 1
        updateProgress(processedFrames / totalFrames * 0.8, "Processing Frames...")

    updateProgress(0.85, "Making video.bin")
    def packFrame(image):
        image = image.convert("1")
        buffer = bytearray(1024)

        for y in range(image.size[1]):
            for x in range(image.size[0]):
                pixel = image.getpixel((x, y))
                index = x + (y // 8) * 128
                bit = y % 8

                if pixel == 255:
                    buffer[index] |= 1 << bit

        return buffer

    updateProgress(0.95, "Processing video.bin")

    with open("video.bin", "wb") as file:
        for frame in sorted(Path("frames").glob("*.png")):
            imageFrame = Image.open(frame)
            buffer = packFrame(imageFrame)
            file.write(buffer)

    print(len(list(Path("frames").glob("*.png"))) * 1024)
    print(Path("video.bin").stat().st_size)

    updateProgress(1, "DONE!")
    return(Path("video.bin"))