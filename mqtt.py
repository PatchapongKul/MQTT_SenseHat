from sense_emu import SenseHat
import time

sense = SenseHat()

red = (255, 0, 0)
blue = (0, 0, 255)

while True:
    time.sleep(3)
    temp = sense.temp
    pixels = [red if i < temp else blue for i in range(64)]
    sense.set_pixels(pixels)