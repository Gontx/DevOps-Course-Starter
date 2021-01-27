import requests
from auth import api_key, token

print (api_key)

base_url = 'https://trello.com/1/'
id_board = 'sr8Gn9uE'
payload ={ 'key' : api_key , 'token' : token }

r = requests.get(base_url + 'boards/' + id_board , params = payload)

print(r.url)

r = r.json()

print ('id for the board is ',r['id'])
print ('Name of the board is ', r['name'])

r=requests.get(base_url + 'boards/' + id_board + '/lists' , params = payload)
print (r.status_code)
r=r.json()
board_list={}
for i in range(len(r)):
    print(r[i]['name'])
    board_list.update({'id':r[i]['id'],'name':r[i]['name']})

print(board_list)