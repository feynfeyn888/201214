#myfunction
import Encoder_myfunction_test
from datetime import datetime
import numpy as np

#Myfunc class Encoder
myfunc = Encoder_myfunction_test.MyClass()

hour = 6
hour_binary = myfunc.binary(hour, 6)
#print(hour_binary)

#Params to be Encoded------------------------------------------------------------------------------------------------

##bit length
bit_length = 16

##LED array length
LED_array_length = 64

##Intensity of light
(r_intensity, g_intensity, b_intensity) = (200, 150, 70)

#prefix=01
##This time, Group_ID is static.
Group_ID = [0,1,0]

#Node_ID is varied according to Edge(IoT device)
Node_ID = [0,0,0]

prefix = Group_ID + Node_ID

#time
now = datetime.now()
hour = now.hour
minute = now.minute
second = now.second

###environmental data
#temperature
temperature = 30 #sense.get_temperature()
#pressure
pressure = 100 #sense.get_pressure()
#humidity
humidty = 20 #sense.get_humidity()

##data_edit-------------------------------------------------------------

###time
hour_binary = myfunc.binary(hour, 6)
minute_binary = myfunc.binary(minute, 6)
second_binary = myfunc.binary(hour, 6)

###environmental data
temper_binary = myfunc.binary(temperature, 8)
press_binary = myfunc.binary(pressure, 8)
humid_binary = myfunc.binary(humidty, 8)

##minute_binary is splited 4bit(Spectral B) and 2bit(Spectral R)
minute_B = minute_binary[0:4:1]
minute_G = minute_binary[4:6:1]

#convert edited data to RGB_array----------------------------------------------------------------------------------------------------
##Spectral B------------------------------------------------------
B_array = prefix + hour_binary + minute_B

##Spectral G------------------------------------------------------
G_array = minute_G + second_binary + temper_binary

##Spectral R------------------------------------------------------
R_array = press_binary + humid_binary

print(B_array)
print(G_array)
print(R_array)

#topic

query = str(10101101)
print("query:",query)
#Queryで渡される値。Publisher側で指定している
binary_query = [int(i) for i in query]
print("binary_query:",binary_query)

com_key = binary_query*2
print("com_key:",com_key)

# input encode

#R
R_x, R_y = myfunc.input(com_key, R_array, bit_length)
print("R_x:",R_x)
print("R_y:",R_y)

#G
G_x, G_y = myfunc.input(com_key, G_array, bit_length)
print("G_x:",G_x)
print("G_y:",G_y)

#B
B_x, B_y = myfunc.input(com_key, B_array, bit_length)
print("B_x:",B_x)
print("B_y:",B_y)

# spatial encode
R = myfunc.spatial_encode(R_x, R_y, bit_length, r_intensity, LED_array_length)
print(R)
G = myfunc.spatial_encode(G_x, G_y, bit_length, g_intensity, LED_array_length)
B = myfunc.spatial_encode(B_x, B_y, bit_length, b_intensity, LED_array_length)

image_array = myfunc.set_array(R, G, B , LED_array_length)
print(image_array)