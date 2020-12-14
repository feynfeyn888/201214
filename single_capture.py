# camera 設定など
# https://dev.classmethod.jp/articles/opencv-webcam-setting/
# これでカメラの対応している諸元をしることができる : $ v4l2-ctl --list-formats-ext

# v4l2-ctl -L これでカメラパラメータを確認できる
# $ v4l2-ctl -c <option> = <value>　# これでカメラパラメータを変更できる
# 例)カメラ感度を落としたいとき
# $ v4l2-ctl -c exposure_absolute=<値>
import cv2
import subprocess
from time import sleep
# prams
file_name = "G50_wavelength_GAMMA72_GAIN_0_"
FRAME_WIDTH = 1920
FRAME_HEIGHT = 1080
GAMMA = 72  # 72~500
GAIN = 0 # 0~100 default=0
#BRIGHTNESS = -64 # -64~64
#EXPOSURE = 1
exposure_auto = 1
exposure_absolute = 115
backlight_compensation = 1

def still_image(file_name, FRAME_WIDTH, FRAME_HEIGHT):
    #カメラのＮｏの設定、1つしかカメラがない場合は0
    cap_no = 0
    cap = cv2.VideoCapture(cap_no)

    # camera設定を反映させるためにいるかも
    _, _ = cap.read() # <-対策としてこの1行を追加

    #カメラのサイズを640 x 480ピクセルに設定
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
    cap.set(cv2.CAP_PROP_GAMMA, GAMMA)
    cap.set(cv2.CAP_PROP_GAIN, GAIN)
    #cap.set(cv2.CAP_PROP_BRIGHTNESS, BRIGHTNESS)
    #cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)


    # 設定の確認
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    gain = cap.get(cv2.CAP_PROP_GAIN)
    brightness = cap.get(cv2.CAP_PROP_BRIGHTNESS)
    exposure = cap.get(cv2.CAP_PROP_EXPOSURE)

    print("width:{} height:{} gain:{} brightness:{}　exposure:{}".format(width, height, gain, brightness, exposure))

    # v4l2の設定をsubprocessを用いて実行
    cmd = "v4l2-ctl -d /dev/video0 -c exposure_auto={} -c exposure_absolute={}".format(exposure_auto, exposure_absolute)
    ret = subprocess.check_output(cmd, shell=True)

    
    # v4l2の設定値を確認
    cmd = 'v4l2-ctl --list-ctrls'
    ret = subprocess.check_output(cmd, shell=True)
    print(ret)
    

    ret1, frame1 = cap.read()
    cv2.imwrite('img/'+file_name+'.png',frame1)
    cap.release()
    #カメラをリリース
    cap.release()
    #画像をすべて閉じる

if __name__ == "__main__":
    still_image(str(file_name), FRAME_WIDTH, FRAME_HEIGHT)
    print("capture")