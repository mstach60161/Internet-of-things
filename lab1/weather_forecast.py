

from VirtualCopernicusNG import TkCircuit

# initialize the circuit inside the

configuration = {
    "name": "CopernicusNG Weather Forecast",
    "sheet": "sheet_forecast.png",
    "width": 343,
    "height": 267,

    "servos": [
        {"x": 170, "y": 150, "length": 90, "name": "Servo 1", "pin": 17}
    ],
    "buttons": [
        {"x": 295, "y": 200, "name": "Button 1", "pin": 11},
        {"x": 295, "y": 170, "name": "Button 2", "pin": 12},
    ]
}

circuit = TkCircuit(configuration)


def convert_deg_temp(temperature):
    return 180 / 35 * temperature - 90


@circuit.run
def main():
    # now just write the code you would use on a real Raspberry Pi

    from time import sleep
    from gpiozero import AngularServo, LED, Button
    from weather import Weather
    weather = Weather()

    def button1_pressed():
        city_weather = weather.get_next_weather()
        print(city_weather)
        servo1.angle = convert_deg_temp(city_weather['temp'])

    def button2_pressed():
        print("button 2 pressed!")

    button1 = Button(11)
    button1.when_pressed = button1_pressed

    button2 = Button(12)
    button2.when_pressed = button2_pressed

    servo1 = AngularServo(17,min_angle=-90, max_angle=90)
    servo1.angle = convert_deg_temp(weather.get_next_weather()['temp'])

    while True:
        pass



