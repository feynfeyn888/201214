# -*- coding: utf-8 -*-

import paho.mqtt.subscribe as subscribe
from time import sleep

# MQTT Broker
MQTT_HOST = "172.16.120.148"    # brokerのアドレス
MQTT_PORT = 1883                # brokerのport
MQTT_KEEP_ALIVE = 60            # keep alive

# broker接続時


DOC_loop = True
subscribe_loop = True
while DOC_loop:
    while subscribe_loop:
        print("start")
        msg = subscribe.simple("Topic", hostname=MQTT_HOST)
        print("msg.payload:", msg.payload)
            
        # if msg.payload include "query", DOC starts
        if 'query' in msg.payload:
            print("query")
            # key = msg.payload[-8:] 後ろから8文字=Queryの長さの分切り出す
            print("query key:", msg.payload[-8:])
            break

    # 撮影のため全点灯・全消灯
    print("撮影をしていく")
    print("sleep:10")
    sleep(10)


    # listにして符号化~
