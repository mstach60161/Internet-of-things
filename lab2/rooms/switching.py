from udp_controller import udp_send

rooms = {
    "C1"     : "livingroom",
    "C2"     : "kitchen",
    "C3"     : "bedroom",
    "C4"     : "lobby",
    "C5"     : "bathroom"
}


def send_order(floor, room, device, operation):
    message = floor + ";" + room + ";" + device + ";" + operation
    udp_send(message)


def button_action(roomID, switch):
    if roomID == "C1":
        if switch == 1:
            return "self"
        else:
            send_order("f2", rooms[roomID], "lamp1", "change")
    if roomID == "C2":
        if switch == 1:
            send_order("f2", rooms[roomID], "lamp1", "change")
        if switch == 2:
            return "self"
    if roomID == "C3":
        return "self"
    if roomID == "C4":
        if switch == 1:
            return "self"
        if switch == 2:
            send_order("*", "*", "*", "off")
    if roomID == "C5":
        return "self"


def use_device(device, operation):
    if operation == "on":
        device.on()
    if operation == 'off':
        device.off()
    if operation == "change":
        device.toggle()


def execute_message(message, self_floor, self_roomID, self_devices):
    floor, room, device, operation = message.split(';')
    if floor != '*' and floor != self_floor:
        return
    if room != "*" and room != rooms[self_roomID]:
        return
    if device == "*":
        for device in self_devices:
            use_device(device, operation)
    if device == "lamp1":
        use_device(self_devices[0], operation)
    if device == "lamp2":
        use_device(self_devices[1], operation)
