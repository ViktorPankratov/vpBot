import requests

API_KEY = 'trnsl.1.1.20190818T184330Z.5bf78df0e0844603.2bc3a37ba31aac853258c90fa800377242449bd6'


class Translator:
    def __init__(self, text, api_key):
        self.text = text
        self.api_key = api_key

    def get_translation(self, target):
        response = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate',
                                params={'text': self.text, 'key': self.api_key, 'lang': target})
        return response.json()['text'][0]

    def get_language(self):
        response = requests.get('https://translate.yandex.net/api/v1.5/tr.json/detect',
                                params={'text': self.text, 'key': self.api_key})
        return response.json()['lang']


def main():
    t = Translator('good', API_KEY)
    print(t.get_language())
    print(t.get_translation('ru'))


if __name__ == '__main__':
    main()
