
import paho.mqtt.client as mqtt
# import io

def on_connect(client, userdata, flags, rc):

    print("Connected with result code "+str(rc))

    client.subscribe("topic1",2)
#
# def store(str):
#     str.append(str)
#     if cnt==1000:
#         for i in str:
#             print str[i]
cnt=0
# str=[]
def on_message(client, userdata, msg):
    global cnt
    # global str
    # str.append(str(msg.payload))
    print("The count is %d"%cnt),
    print(msg.topic + " -> " + str(msg.payload))
    cnt+=1
    if cnt==900:
        print "its almost done"
    # data=str(msg.payload)
    # file.write(unicode(data))
    # # file.write(unicode(str(msg.payload)))
    # file.write(u"\n")



client = mqtt.Client()
client.tls_set("/etc/mosquitto/certs/ca.crt")
client.on_connect = on_connect

# file = io.open("outputfile.txt", "a")
# print(" Output file is created as outputfile.txt")
client.on_message = on_message
client.connect("localhost", 8883, 60)
client.loop_forever()