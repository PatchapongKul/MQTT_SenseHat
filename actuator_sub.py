from sense_emu import SenseHat
import paho.mqtt.client as mqtt
from Crypto.Cipher import AES
from binascii import unhexlify

sense = SenseHat()

key = unhexlify('2b7e151628aed2a6abf7158809cf4f3c')    #16 byte
IV = unhexlify('000102030405060708090a0b0c0d0e0f')     #16 byte
decipher = AES.new(key,AES.MODE_CBC,IV)

def on_connect(client, userdata, flags, rc):
    print("Command with result code " + str(rc))

    # Subscribing in on_connect() - if we lose the connection and
    # reconnect then subscription will be renewed.
    client.subscribe("MyRoom/ac/command")

def on_message(client, userdata, msg):
    #print(msg.topic + " " + str(msg.payload))
    #print(type(msg.payload))
    
    if msg.topic == 'MyRoom/ac/command':
        command_encrypted = decipher.decrypt(msg.payload)
        command_decrypted = command_encrypted.decode('utf-8')
        command = command_decrypted.strip('0')
        
        print(msg.topic,command)
        
        red   = (255, 0, 0)
        blue  = (0, 0, 255)
        green = (0,255,0)
        white = (255,255,255)
        
        if command == "decrease temp":
            minus = [25,26,27,28,29,30,33,34,35,36,37,38]
            pixels = [white if i in minus else blue for i in range(64)]
            sense.set_pixels(pixels)
        elif command == "increase temp":
            plus = [11,12,19,20,25,26,27,28,29,30,33,34,35,36,37,38,43,44,51,52]
            pixels = [white if i in plus else red for i in range(64)]
            sense.set_pixels(pixels)
        else:
            smile = [10,18,13,21,40,47,49,50,51,52,53,54]
            pixels = [white if i in smile else green for i in range(64)]
            sense.set_pixels(pixels)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("test.mosquitto.org", 1883, 60)

client.loop_forever()