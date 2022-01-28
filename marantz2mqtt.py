import paho.mqtt.client as mqtt
import serial
import time
ser = serial.Serial('/dev/XXX',9600, timeout=1)# XXX Your serial device


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("in_marantz")


def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    ser.write(msg.payload)
    resp=(ser.read(16))
    print(resp)
    mesg=resp.decode("utf8" )
    print(mesg)
    if mesg[1:4]=="SRC":
        client.publish("out_marantz/SRC", resp, qos=0, retain=True)
    elif mesg[1:4]=="NGT":
        client.publish("out_marantz/NGT", resp, qos=0, retain=True)
    elif mesg[1:4]=="SUR":
        client.publish("out_marantz/SUR", resp, qos=0, retain=True)
    elif mesg[1:4]=="INP":
        client.publish("out_marantz/INP", resp, qos=0, retain=True)
    elif mesg[1:4]=="VOL":
        client.publish("out_marantz/VOL", mesg[5:8], qos=0, retain=True)
    else:
        client.publish("out_marantz", resp, qos=0, retain=True)
client = mqtt.Client()
client.username_pw_set(username="XXXXXX",password="XXXXXXXXX")# Your credential to MQTT server
client.connect("XXXXXX", 1883, 60)# IP of your mqtt server
client.on_connect = on_connect
client.on_message = on_message
client.loop_forever()
