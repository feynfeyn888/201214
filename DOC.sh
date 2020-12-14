#!/bin/sh
# 実行するときは bash <ファイル名>

# 1枚目,2枚目は符号器検出用画像

python img_capture.py
python img_cutting.py
python img_divide.py
python img_DOC_decode.py