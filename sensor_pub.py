from sense_emu import SenseHat
import time
from Crypto.Cipher import AES
import Crypto.Cipher.AES
from binascii import hexlify, unhexlify
import paho.mqtt.publish as publish

key = unhexlify('2b7e151628aed2a6abf7158809cf4f3c')    #16 byte
IV = unhexlify('000102030405060708090a0b0c0d0e0f')     #16 byte

sense = SenseHat()

#encrypt temperature data before publish
cipher = AES.new(key,AES.MODE_CBC,IV)

while True:
    time.sleep(3)
    temp = str(sense.temp)
    
    temp_16 = ('0'*(16-len(temp)) + temp).encode('utf-8')
    #print(temp_16)
    
    temp_encrypted = cipher.encrypt(temp_16)
    #print(hexlify(temp_encrypted))

    #Publish to broker
    publish.single("MyRoom/sensor/temp", temp_encrypted, hostname="test.mosquitto.org")
    
    #pixels = [red if i < temp else blue for i in range(64)]
    #sense.set_pixels(pixels)
    