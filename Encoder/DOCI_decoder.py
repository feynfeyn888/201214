#coding:utf-8

# python embedded module
import time
from time import sleep
from datetime import datetime

# other module
import cv2
import numpy as np

# ueye cockpit module
from pyueye import ueye
from pyueye_example_camera import Camera

# mqtt module(mosquito)
import paho.mqtt.publish as publish

# myfunc module Decode
from Decoder_myfunction import YourClass

# Myfunc class Decoder
yourfunc = Decoder_myfunction.YourClass()

# send topic 
yourfunc.topic()

#ここのsleep時間は符合器の全点灯+全消灯の時間に準ずる
sleep(10)

#------------------------------------------------------------
#　send topic & detect devices by back subsucription.
loop_back_detect = 2
for i in range(loop_back_detect):
    # get topic 
    yourfunc.topic()
    print("publish Query")
    
    # get picture
    # First argument:Capture Mode(0 or 1), Second argument:Capture Number 
    youtfunc.main(0, ,i)
    sleep(5)

# abstract devices and get contours of device.
areas = yourfunc.imread()

#--------------------------------------------------------------
# get picture & decode spatial code.
loop_decode = 10

for j in range(loop_decode):
    # get picture
    yourconf.main(1, j)
    
    # devide picture to each wavelength channel picture(RGB channnel).   

    # decode spatial code.
    yourconf.imread_src(areas, j, R)
    yourconf.imread_src(areas, j, G)
    yourconf.imread_src(areas, j, B)