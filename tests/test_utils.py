import requests

def post_rest_call(url, params={}):
    response = requests.post(url, params)
    return response.json()

def get_rest_call(url, params={}):
    response = requests.get(url, params)
    return response.json()

def put_rest_call(url, params={}):
    response = requests.put(url, params)
    return response.json()

def delete_rest_call(url):
    response = requests.delete(url)
    return response.json()

