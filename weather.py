import requests
from weather_strings import icon, Strings

SITE_URL = 'https://api.openweathermap.org/data/2.5/'
text = Strings()
WEATHER_APP_KEY = 'c1b4f3df7e0e3fd445d4f8ed0b590d5e'


class Weather:
    def __init__(self, app_key, city, response_language_code='en'):
        self.request_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/76.0.3809.100 Safari/537.36',
        }
        self.app_key = app_key
        self.response_language_code = response_language_code
        self.city = city

    def get_api_response(self, query_type):
        api_response = requests.get(SITE_URL + query_type,
                                    params={'appid': self.app_key,
                                            'q': self.city,
                                            'units': 'metric',
                                            'cnt': 1,
                                            'lang': self.response_language_code
                                            },
                                    headers=self.request_headers, timeout=3)
        return api_response.json()

    def get_weather(self):
        try:
            current_weather = self.get_api_response('weather')
            current = self.get_weather_data(current_weather)
            current['label'] = text.weather_label
        except KeyError:
            return False
        try:
            forecast_weather = self.get_api_response('forecast')
            # nearest_forecast
            forecast = self.get_weather_data(forecast_weather['list'][0])
            forecast['label'] = text.forecast_label
        except KeyError:
            return False
        return current, forecast

    def get_weather_data(self, weather_info):
        weather_data = {'weather': weather_info['weather'][0]['description'],
                        'icon': self.get_icon(
                            weather_info['weather'][0]['icon']),
                        'temperature': weather_info['main']['temp']
                        }
        return weather_data

    @staticmethod
    def get_icon(api_icon_code):
        return icon[api_icon_code]


def main():
    pass


if __name__ == '__main__':
    main()
