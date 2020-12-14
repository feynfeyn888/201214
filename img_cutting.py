#coding:utf-8

# python embedded module
import time
from time import sleep
from datetime import datetime

# other module
import cv2
import numpy as np

# mqtt module(mosquito)
import paho.mqtt.publish as publish

####################################################

img_src0 = cv2.imread("img/DOC_0.png", 1)
img_src1 = cv2.imread("img/DOC_1.png", 1)
#全点灯グレイスケール化
gray0 = cv2.cvtColor(img_src0,cv2.COLOR_BGR2GRAY)
cv2.imwrite("img/image_gray0.png",gray0)
print(gray0.shape)

#全消灯グレイスケール化
gray1 = cv2.cvtColor(img_src1,cv2.COLOR_BGR2GRAY)
cv2.imwrite("img/image_gray1.png",gray1)
print(gray1.shape)

# 差分画像
img_diff = cv2.absdiff(gray1, gray0)
cv2.imwrite("img/image_abs_gray.png",img_diff)

#二値化
ret,img = cv2.threshold(img_diff,#入力画像
                        150,#閾値 ->ここはハードコーディングしないほうがいい(明かりありなら100, 暗くするなら200)
                        255,#画素値の最大値
                        cv2.THRESH_BINARY)#2値化のType

#処理画像を出力↓
cv2.imwrite("img/image_capture_binary.png",img)

#cv2.imwrite("C:\Users\owner\Desktop\watanabe\decoding_\output\\rectangle_detect\image_capture_bitwise.png",img)
#operator
operator = np.ones((3, 3), np.uint8)
#膨張処理
img = cv2.dilate(img, operator,iterations=5)
#収縮処理
img = cv2.erode(img,operator, iterations=5)

#処理画像を出力↓
cv2.imwrite("img/image_dilate_erode.png",img)

#矩形検知
#img, contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#img:出力画像
#contours:検出した全輪郭をpythonのリストとして出力する。len(contours)が矩形の数と対応する
#hierarchy:輪郭の数と階層情報を出力

# cv2.RETR_EXTERNAL:一番外の輪郭を抽出する
# cv2.RETR_TREE:入れ子
# cv2.RETR_LIST:同じ階層の輪郭が取得
# cv2.RETR_CCOMP:内部輪郭と外部輪郭両方を抽出
# cv2.CHAIN_APPROX_NONE:輪郭上のすべての点の情報を保持する
# cv2.CHAIN_APPROX_SIMPLE:輪郭の端点を保持する。メモリの使用量が減るのでこちらのほうが好ましい

contours = contours[0] if len(contours) == 2 else contours[1]
print(contours)
cv2.drawContours(img, contours, -1, (0,255,0), 10)
cv2.imwrite("img/image_contours.png",img)

areas = []#符号器の輪郭だけを入れるための空のリスト
for cnt in contours:#cnt:輪郭#輪郭の数だけループする
    area = cv2.contourArea(cnt)#cv2.contourArea(cnt):領域が占める面積を計算
    if area > 900:#輪郭の面積が5000以上の場合、リストに追加する
        epsilon = 0.1*cv2.arcLength(cnt,True)
        #領域を囲む周囲長を計算する
        #第二引数は対象とする領域が閉じている(True)か単なる曲線かを表すフラグ
        approx = cv2.approxPolyDP(cnt,epsilon,True)
        #approx:輪郭の近似を行う
        #第二引数は実際の輪郭と近似輪郭の最大距離を表し近似の精度を表すパラメータ
        areas.append(approx)

print("areas:", areas)

##################################################################

# imread
src = cv2.imread("img/DOC_2.png", 1) 

"""
# Binarization
ret,thre_src = cv2.threshold(src,#入力画像
                            100,#閾値
                            255,#画素値の最大値
                            cv2.THRESH_BINARY)#2値化のType
"""

#BGRの順で並ぶことに注意
cv2.drawContours(src,areas,-1,(0,0,255),1)
cv2.imwrite("img/image_thre.png",src)

#k = 矩形の数(符号器の数)
k = len(areas)          
M = np.zeros((k,3,3))
#3×3ですべての値が0の行列をk(符号器の数)だけ作る
for index in range(k):#矩形の数だけ繰り返す繰り返す
    if len(areas[index]) == 4: #これはたぶん矩形かどうかの判定
        ar = areas[index]
        #print("ar:{}".format(ar))#4点の抽出
        ar = ar.reshape(4,2)
        #print("ar.reshape:{}".format(ar))#4点の抽出
        #列順に並べる
        ar = ar[ar[:,0].argsort(),:]
        #print("ar.argsort:{}".format(ar))#
        #射影変換前の図形
        pts1 = np.float32(ar)
        #射影変換後の図形
        # ここで画像サイズを決定する
        img_size = 160

        pts2 = np.float32([[0,0],[0,img_size],[img_size,0],[img_size,img_size]])
        #変換行列を計算
        M[index] = cv2.getPerspectiveTransform(pts1,pts2)
        dst=[]
        #画像を変形
        dst = cv2.warpPerspective(src,M[index],(img_size, img_size))
        cv2.imwrite("img/encode_image_encoder_id_"+str(index)+".png",dst)

#  こっから波長分割する