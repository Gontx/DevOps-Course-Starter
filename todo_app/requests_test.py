import requests
from auth import api_key, token
from todo_app.classes import Item

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
lists = r

print(lists)

#Request cards on a list
cards = []
for list in lists:
    id_list = list['id']
    name_list = list['name']
    r=requests.get(base_url + 'lists/' + id_list + '/cards', params = payload)
    print (r.status_code)
    r=r.json()
    for card in r:
        cards.append(card)

# Assign name, and status to item
i=0
items=[]
for card in cards:
    for list in lists:
        if card['idList'] == list['id']:
            status = list['name']
            name = card['name']
            item=Item(i,status,name)
            items.append(item)
            i=i+1

print ('Cards within list: ')
for item in items:
    print('Item id: ',item.id, ' with title: ',item.title, ' is ',item.status)

