from VirtualCopernicusNG import TkCircuit
import rooms.lighting as lighting

room_id = "client4"

configuration = {
    "name": "Living room",
    "sheet": "sheet_smarthouse.png",
    "width": 332,
    "height": 300,
    "leds": [
        {"x": 112, "y": 70, "name": "LED 1", "pin": 21},
        {"x": 71, "y": 141, "name": "LED 2", "pin": 22}
    ],
    "buttons": [
        {"x": 242, "y": 146, "name": "Button 1", "pin": 11},
        {"x": 200, "y": 217, "name": "Button 2", "pin": 12},
    ],
    "buzzers": [
        {"x": 277, "y": 9, "name": "Buzzer", "pin": 16, "frequency": 440},
    ]
}

circuit = TkCircuit(configuration)

def extract_msg(msg):
    return str(msg.payload)[2:-1]

@circuit.run
def main():
    from gpiozero import LED, Button
    import paho.mqtt.client as mqtt
    led1 = LED(21)
    led2 = LED(22)
    devices = [led1, led2]

    def button1_pressed():
        led1.toggle()
        mqttc.publish("home/floor1/room/pref1", "20dfds", 0, False)

    def button2_pressed():
        mqttc.publish(lighting.zone1, "OFF", 0, False)

    button1 = Button(11)
    button1.when_pressed = button1_pressed

    button2 = Button(12)
    button2.when_pressed = button2_pressed

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        print("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        mqttc.subscribe(lighting.zone1)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))

        action = extract_msg(msg)
        for device in devices:
            if action == "ON":
                device.on()
            if action == "OFF":
                device.off()
            if action == "TOGGLE":
                device.toggle()

    # If you want to use a specific client id, use
    # mqttc = mqtt.Client("client-id")
    # but note that the client id must be unique on the broker. Leaving the client
    # id parameter empty will generate a random id for you.
    mqttc = mqtt.Client(room_id)
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect

    mqttc.connect("127.0.0.1", 1883, 60)

    mqttc.loop_forever()