import requests
import constants

def go():

    url = constants.ENKI_DATA_URL

    print(url)

    response = requests.get(url)

    # if response.status_code
    print(response.status_code)

    print(response.text)

    return ''

if __name__ == '__main__':
    go()