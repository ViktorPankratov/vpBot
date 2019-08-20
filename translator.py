import requests

SITE_URL = 'https://translate.yandex.net/api/v1.5/tr.json/'


class Translator:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_translation(self, text, target):
        response = requests.get(SITE_URL + 'translate',
                                params={'text': text, 'key': self.api_key,
                                        'lang': target})
        return response.json()['text'][0]

    def get_language(self, text):
        response = requests.get(SITE_URL + 'detect',
                                params={'text': text,
                                        'key': self.api_key})
        return response.json()['lang']


def main():
    pass


if __name__ == '__main__':
    main()
