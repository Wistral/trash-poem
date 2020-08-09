from googletrans import Translator


translator = Translator(service_urls=['translate.google.cn'])


def gtrans(text, lan='en'):
    return translator.translate(text, dest=lan).text


if __name__ == '__main__':
    print(gtrans('今天天气不错'))
    print(gtrans('今天天气不错','ja'))
    print(gtrans('今天天气不错', 'ko'))
