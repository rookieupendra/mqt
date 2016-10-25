import paho.mqtt.client as mqtt
import time
import datetime

def on_connect(client, userdata, flags, rc):

    print("Connected with result code "+str(rc))
    client.subscribe("topic1",0)

cnt=0
t1=0.0
def on_message(client, userdata, msg):
    # global t1
    # if msg.payload=='start':
    #     t1=time.time()
    # if msg.payload=='exit':
    #     t2=time.time()
    #     download_time = "%0.2f" % ((t2 - t1) * 1000.0)
    #     print download_time
    # print(msg.topic + " -> " + str(msg.payload))

    global cnt
    global t1
    print(cnt),
    print(msg.topic + " -> " + str(msg.payload))
    if msg.payload=='start':
        t1=time.time()
    if msg.payload == 'exit':
        t2 = time.time()
        download_time = "%0.2f" % ((t2 - t1) * 1000.0)
        cnt=cnt-1
        print "download_time= " + download_time+" count is :%d"%cnt
        st = datetime.datetime.fromtimestamp(t2).strftime('%Y-%m-%d %H:%M:%S')
        print st
        client.publish("topic2","{},{},{},{},{},{},{}".format('dw', q, st, download_time,cnt, 'undefined','sub@upendra_simple'), q)
        # cnt=0

    cnt+=1

global q
q=0

client = mqtt.Client()
client.tls_set("/etc/mosquitto/certs/ca.crt")
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 8883, 60)
client.loop_forever()
