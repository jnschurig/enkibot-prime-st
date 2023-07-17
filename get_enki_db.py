import requests
import constants

def go():
    # Fetch data from original enkibot app.
    # Someday perhaps I will have it fetch the data from the git source...
    
    url = constants.ENKI_DATA_URL

    response = requests.post(url)

    if response.status_code == 200:
        print('herokuapp ok. returning text...')
        return response.text

    return None

if __name__ == '__main__':
    go()