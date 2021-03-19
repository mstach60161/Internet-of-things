from pyowm.owm import OWM


class Weather:

    def __init__(self):
        self.owm = OWM('4526d487f12ef78b82b7a7d113faea64')
        self.mgr = self.owm.weather_manager()
        self.city_counter = 1
        self.cities = {
                        1 : 'krakow',
                        2 : 'london',
                        3 : 'stockholm'
                    }

    def update_city_counter(self):
        self.city_counter += 1
        if self.city_counter == 4:
            self.city_counter = 1

    def get_weather(self, city):
        observation = self.mgr.weather_at_place(city)
        weather = observation.weather
        result = {
            'status' : weather.status,
            'temp' : weather.temperature('celsius').get('temp')
        }
        return result

    def get_next_weather(self):
        self.update_city_counter()
        return self.get_weather(self.cities[self.city_counter])
