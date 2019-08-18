import requests

class Weather:
    def __init__(self, app_key, city, response_language_code='en'):
        self.request_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/76.0.3809.100 Safari/537.36',
        }
        self.app_key = app_key
        self.response_language_code = response_language_code
        self.city = city

    def get_api_response(self, query_type):
        api_response = requests.get(
            'https://api.openweathermap.org/data/2.5/' + query_type,
            params={'appid': self.app_key, 'q': self.city, 'units': 'metric',
                    'lang': self.response_language_code, 'cnt': 1},
            headers=self.request_headers, timeout=3)
        return api_response.json()

    def get_weather(self):
        if int(self.get_api_response('weather')['cod']) != 200:
            return False
        else:
            current_weather = self.get_api_response('weather')
            current = self.get_weather_data(current_weather)
            current['label'] = 'Сейчас'

        if int(self.get_api_response('forecast')['cod']) != 200:
            return False
        else:
            forecast_weather = self.get_api_response('forecast')
            forecast = self.get_weather_data(forecast_weather['list'][0])  # nearest_forecast
            forecast['label'] = 'Ожидается'
        return current, forecast

    def get_weather_data(self, weather_info):
        weather_data = {'weather': weather_info['weather'][0]['description'],
                        'icon': self.get_icon(weather_info['weather'][0]['icon']),
                        'temperature': weather_info['main']['temp']
                        }
        return weather_data

    @staticmethod
    def get_icon(api_icon_code):
        if api_icon_code == '01d':
            return '\u2600'
        if api_icon_code == '01n':
            return '\uF311'
        if api_icon_code == '02d':
            return '\u26C5'
        if api_icon_code == '02n':
            return '\u2601'
        if api_icon_code == '03d':
            return '\u2601'
        if api_icon_code == '03n':
            return '\u2601'
        if api_icon_code == '04d':
            return '\u2601'
        if api_icon_code == '04n':
            return '\u2601'
        if api_icon_code == '09d':
            return '\u2614'
        if api_icon_code == '09n':
            return '\u2614'
        if api_icon_code == '10d':
            return '\u2614'
        if api_icon_code == '10n':
            return '\u2614'
        if api_icon_code == '11d':
            return '\u2614'
        if api_icon_code == '11n':
            return '\u2614'
        if api_icon_code == '13d':
            return '\u2744'
        if api_icon_code == '13n':
            return '\u2744'
        if api_icon_code == '50d':
            return '\u1F301'
        if api_icon_code == '50n':
            return '\u1F301'


def main():
    city = 'Ульяновск'
    weather = Weather(city=city, response_language_code='ru', app_key='c1b4f3df7e0e3fd445d4f8ed0b590d5e')


if __name__ == '__main__':
    main()
