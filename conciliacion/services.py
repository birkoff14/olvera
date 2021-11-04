import requests

"""
def generate_request(url, params={}):
    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

def get_username(params={}):
    response = generate_request('https://randomuser.me/api', params)
    if response:
       user = response.get('results')[0]
       return user.get('name').get('first')

    return ''"
"""

def generate_request(url):
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

def cuentasContables():
    response = generate_request('http://127.0.0.1:8000/cuentasContables/')
    if response:
        id = response.get('')
