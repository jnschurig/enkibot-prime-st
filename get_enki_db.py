import requests
import constants

def go():

    url = constants.ENKI_DATA_URL

    print(url)

    response = requests.post(url)

    if response.status_code == 400:
        return response.text

    return None

if __name__ == '__main__':
    go()