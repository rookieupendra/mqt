import paho.mqtt.client as mqtt

mqttc = mqtt.Client("python_pub")
mqttc.tls_set("/etc/mosquitto/certs/ca.crt")
mqttc.connect("10.0.0.140", 8883)

while 1:
    x=raw_input("Enter something to send: ")
    mqttc.publish("topic1",x, qos=0)

mqttc.loop_forever()
