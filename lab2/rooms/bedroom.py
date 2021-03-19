from VirtualCopernicusNG import TkCircuit
from rooms.switching import *
from udp_receiver import *

room_data = [
    "C3",       # room ID
    "bedroom",  # room name
    "f1"        # floor
]

configuration = {
    "name": "bedroom",
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

@circuit.run
def main():
    self_roomID, self_room, self_floor = room_data

    from gpiozero import LED, Button
    led1 = LED(21)
    led2 = LED(22)
    self_devices = [led1, led2]

    def button1_pressed():
        result = button_action(self_roomID, 1)
        if result == "self":
            led1.toggle()

    def button2_pressed():
        result = button_action(self_roomID, 2)
        if result == "self":
            led2.toggle()

    button1 = Button(11)
    button1.when_pressed = button1_pressed

    button2 = Button(12)
    button2.when_pressed = button2_pressed

    sock_receiver = udp_receiver_init()

    while True:
        command = sock_receiver.recv(10240)
        command = command.decode("utf-8")
        print(command.split(';'))
        execute_message(command, self_floor, self_roomID, self_devices)