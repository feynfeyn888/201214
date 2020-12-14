# -*- coding: utf-8 -*-

import paho.mqtt.client as mqtt  
import paho.mqtt.publish as publish
from time import sleep

# MQTT Broker
MQTT_HOST = "172.16.120.148"       # brokerのアドレス
MQTT_PORT = 1883                # brokerのport
MQTT_KEEP_ALIVE = 60            # keep alive

# params
topic = "Topic"
msg = "query:10101001"

def on_publish(topic, msg):
    print("publish start")
    publish.single(topic, payload=msg, qos=0, retain=True, hostname=MQTT_HOST, port=MQTT_PORT, keepalive=MQTT_KEEP_ALIVE)
    print("publish end")

###
def main(topic, msg):
    on_publish(topic, msg)

if __name__ == '__main__':          # importされないときだけmain()を呼ぶ
    main(topic, msg)    # メイン関数を呼び出す