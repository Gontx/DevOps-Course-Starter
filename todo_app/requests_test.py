import requests
from auth import api_key, token

print (api_key)

base_url = 'https://trello.com/1/'
id_board = 'sr8Gn9uE'
payload ={ 'key' : api_key , 'token' : token }

#Request board information
r = requests.get(base_url + 'boards/' + id_board , params = payload)

print(r.url)

r = r.json()

print ('id for the board is ',r['id'])
print ('Name of the board is ', r['name'])

#Request lists on a board
r=requests.get(base_url + 'boards/' + id_board + '/lists' , params = payload)
print (r.status_code)
r=r.json()
lists = []
for key in r:
    lists.append(dict({key['name']:key['id']}))

print(lists)

#Request cards on a list
cards = []
for list in lists:
    id_list = list['id']
    name_list = list['name']
    r=requests.get(base_url + 'lists/' + id_list + '/cards', params = payload)
    print (r.status_code)
    r=r.json()

print ('Cards within list: ')
for key in r:
    print (key['name'])