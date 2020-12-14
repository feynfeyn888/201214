import cv2
import glob
import numpy as np
filepath = "img/encode_image_encoder_id_0.png"
filename = glob.glob(filepath)

print("image divide")
for files in filename:
    img = cv2.imread(files)
    
    # 画像情報
    height, width, channels = img.shape[:3]
    print("height:",height)
    print("width:", width)
    print("channels:", channels)

    Blue,Green,Red = cv2.split(img)
    cv2.imwrite("img/Blue.png",Blue)
    cv2.imwrite("img/Green.png",Green)
    cv2.imwrite("img/Red.png",Red)