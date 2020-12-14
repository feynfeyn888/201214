#!/usr/bin/env python
#coding:utf-8

import cv2
import numpy as np

import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
from time import sleep
import time
from datetime import datetime

k = 1
for hukugou in range(k):#符号器の数繰り返す
#画像の読み出し
    img = cv2.imread("img/Blue.png",1)
    # 画像サイズ取得
    height, width, channels = img.shape[:3]
    print("height:",height)
    print("width:", width)
    print("channels:", channels)

    # 切り出し間隔 = 切り出し画像/10
    cutting_pitch = 20

    # 画像の重ね合わせ
    w=int(img.shape[0]/8)#img.shape[0]:画像の縦列
    h=int(img.shape[1]/8)#img.shape[1]:画像の横列

    img1 = img[w:8*w,h:8*h]#右下切り取り　1LED左上　
    img2 = img[w:8*w,0:7*h]#左下切り取り　1LED左
    img3 = img[0:7*w,h:8*h]#右上切り取り　1LED上
    img4 = img[0:7*w,0:7*h]#左上切り取り　これを基本とする
    #XORはimg2とimg3を選択
    imgc1 = img2#[左下7*7画像]
    imgc2 = img3#[右上7*7画像]
    img_weighted = cv2.addWeighted(imgc1, 0.5, imgc2, 0.5, 0)
    img = np.array(img_weighted)
    for i in range(int(3)):#横縞#3回
        cv2.rectangle(img, (0, h*(2*i+1)), (8*h, h*(2*i+2)), (0, 0, 0), thickness=-1)
    for j in range(int(3)):#縦縞
        cv2.rectangle(img, (w*(2*j+1), 0), (w*(2*j+2), 8*w), (0, 0, 0), thickness=-1)
    cv2.imwrite("img/Blue_decode_mask.png", img)

    height, width, channels = img.shape[:3]
    print("height:",height)
    print("width:", width)
    print("channels:", channels)

    # 画像の切り出し
    for delete in range(3):#なんかよくわからんけど3ならうまくいく
        #8画素ずつマスクをしたところを切り出していく
        img = np.delete(img,np.s_[cutting_pitch*(delete+1):cutting_pitch*(delete+1)+cutting_pitch], axis=0) #列(要素)の消去
        # img = np.delete(img,np.s_[0*w:8*w:3*w], axis=0)
        img = np.delete(img,np.s_[cutting_pitch*(delete+1):cutting_pitch*(delete+1)+cutting_pitch], axis=1) #行の消去
        # img = np.delete(img,np.s_[0*w:8*w:3*w], axis=1)

    ret, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)
    #閾値を100にしている。ノイズが多い場合は変更する必要あり。
    cv2.imwrite('img/Blue_decode.png', img)

    height, width, channels = img.shape[:3]
    print("height:",height)
    print("width:", width)
    print("channels:", channels)

    # Decode
    decode=[]
    #for i in range(1):
    for i in range(4):#4行あるうち、出力する行の数#長いので今は2行まで
        for j in range(4):#4列
            mean=np.mean(img[cutting_pitch*i:cutting_pitch*(i+1)-1,cutting_pitch*j : cutting_pitch*(j+1)-1])
            if mean<50:
                mean = 0
                decode.append(mean)
            else:
                mean = 1
                decode.append(mean)
    #output:2bit→符号器番号,2bit→パラメータの指定番号,12bit→センサ情報
    prefix = decode[0:2:1]#[0,0][0,1][1,0][1,1]の4通り
    params = decode[2:4:1]#te=[0,1],pr=[1,0],hu=[1,1]
    sensor = decode[4:16:1]
    
    output=[]
    #符号器番号
    if prefix == [0,0]:
        output.append(0)
    elif prefix == [0,1]:
        output.append(1)
    elif prefix == [1,0]:
        output.append(2)
    elif prefix == [1,1]:
        output.append(3)
    else:
        output.append("error")


    #パラメータ指定番号
    if params == [0,1]:
        output.append("te")
    elif params == [1,0]:
        output.append("pr")
    elif params == [1,1]:
        output.append("hu")
    else:
        output.append("error")

    #sensor:2進数→10進数
    sensor_2 = str()
    for x in range(len(sensor)):
        sensor_2 += str(sensor[x])
    sensor_10 = int(sensor_2,2)
    output.append(sensor_10)

    print(output)

    f = open("output.txt", mode='a')
    f.write(str(hukugou)+str(output)+"\n") # 引数の文字列をファイルに書き込む
    f.close()
    print("finish decode loading")
