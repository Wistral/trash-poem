import requests
import random

api = 'https://international.v1.hitokoto.cn'

types = 'adfik'

def gen_sentence():
    params = {
        'c': random.choice(types)
    }

    r = requests.get(api, params=params)
    assert r.status_code == 200
    js = r.json()
    return js['hitokoto'], js['from'], js['uuid']


if __name__ == '__main__':
    print(gen_sentence())
