import requests
import constants

def go():

    url = constants.ENKI_DATA_URL

    print(url)

    response = requests.post(url)

    if response.status_code == 200:
        print('herokuapp ok. returning text...')
        return response.text

    return None

if __name__ == '__main__':
    go()