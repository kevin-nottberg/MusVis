import pyaudio
import time
import numpy
import audioop 
import math
import sys
import struct

import pygame
from pygame.locals import *

from bibliopixel.led import *
from bibliopixel.animation import StripChannelTest
from bibliopixel.drivers.LPD8806 import *
from bibliopixel.colors import *


driver = DriverLPD8806(320)
led = LEDStrip(driver)
led.all_off()
led.update()

p = pyaudio.PyAudio()
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
exponet = 1

frames = []

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
#pygame.init()

print("passed")

while True:
    try:
        stream.start_stream()
    except IOError:
        print("Caught IOError and restarting gggggggggggggggggggggggggggggggggggggggggggggggggggggg")
        time.sleep(0.1)        
        stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)
        continue
    except: 
        print("Caught something and restarting")
        time.sleep(0.1)
        continue

    data = 0
    data = stream.read(CHUNK)
    '''
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                exponet = 1
            if event.key == pygame.K_r:
                exponet = 2
            if event.key == pygame.K_q:
                print("Ending")
                pygame.quit()
                sys.exit()    
    '''    
    data2 = struct.unpack("%dh"%(len(data)/2), data)
    data2 = numpy.array(data2, dtype='h')
    fourier = numpy.fft.rfft(data2)
    
    fourier = numpy.delete(fourier, len(fourier)-1)
    power = numpy.log10(numpy.abs(fourier)) ** 2
    size = len(power)
    levels = [sum(power[i:(i+size/3)]) for i in xrange(0, size, size/3)][:3]
    
    allLev = []
    i = 0
    j = 0
    for level in levels:
       	level = level/29500
        print("Level ")
        print(i)
        print(level)        
        level = level ** exponet
        level = int(level * 255)
        allLev.append(level)
   
    print("All level: ")
    print(allLev)
    while i < len(allLev):
        if allLev[i] > 255:
            allLev[i] = 255
        elif allLev[i] <= 0: 
            allLev[i] = 0        
        print(allLev[i])
        i = i + 1

    led.fill([max(int(allLev[2]-10), 0), max(int(allLev[0]-20), 0), max(int(allLev[1]-10), 0)], 0, 319)
    led.update() 
    print([max(int(allLev[0]-20), 0), allLev[1], allLev[2]])
    stream.stop_stream()
        
