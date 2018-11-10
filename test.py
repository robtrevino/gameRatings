import requests

igdbKey = 'd1213aa0fa52512b50fcf362367e19ea'
endpoint = 'https://api-endpoint.igdb.com'

header = {
    'user-key' : igdbKey,
    'accept' : 'application/json'
}

search = 'Mario Kart'

gamesUrl = endpoint + '/games/'
params = {
    'search' : search,
    'expand' : 'game',
    'fields' : 'name,rating'
}

r = requests.get(url = gamesUrl, headers = header, params = params)
print(r.status_code)
#print(r.text)
print(r.json())
