import paho.mqtt.client as mqtt

from Crypto.Cipher import AES
from binascii import unhexlify

key = unhexlify('2b7e151628aed2a6abf7158809cf4f3c')    #16 byte
IV = unhexlify('000102030405060708090a0b0c0d0e0f')     #16 byte
decipher = AES.new(key,AES.MODE_CBC,IV)

def on_connect(client, userdata, flags, rc):
    print("Command with result code " + str(rc))

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscription will be renewed.
    client.subscribe("MyRoom/Temp")

def on_message(client, userdata, msg):
    #print(msg.topic + " " + str(msg.payload))
    #print(type(msg.payload))
    
    if msg.topic == 'MyRoom/Temp':
        temp_encrypted = decipher.decrypt(msg.payload)
        temp_decrypted = temp_encrypted.decode('utf-8')
        temp = float(temp_decrypted.strip('0'))
        print(msg.topic,round(temp,3))

    
# Create an MQTT client and attach our routine to it.
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()