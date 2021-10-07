from todo_app.data import session_items as si
from todo_app.app import create_app
from dotenv import find_dotenv,load_dotenv
import datetime as dt
import pytest
import json
from unittest.mock import patch, Mock

@pytest.fixture
def client():
    # Use our test integration config instead of the "real" version
    file_path = find_dotenv('.env.test') 
    load_dotenv(file_path, override=True)

    # Create the new app.
    test_app = create_app()

    # Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client

@staticmethod
def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_lists
    response = client.get('/')
    assert response.status_code == 200

def mock_get_lists(url, params):
    if url == 'https://trello.com/1/boards/' + si.get_id_board() + '/lists':
        response = Mock()
        # sample_trello_lists_response should pointto some test response data
        sample_trello_lists_response='[{"id":"5fda74f60fc61c6f342225cf","name":"To Do","closed":false,"pos":16384,"softLimit":null,"idBoard":"5fda74f60fc61c6f342225ce","subscribed":false},{"id":"5fda74f60fc61c6f342225d0","name":"Doing","closed":false,"pos":32768,"softLimit":null,"idBoard":"5fda74f60fc61c6f342225ce","subscribed":false},{"id":"5fda74f60fc61c6f342225d1","name":"Done","closed":false,"pos":49152,"softLimit":null,"idBoard":"5fda74f60fc61c6f342225ce","subscribed":false}]'
        response.json.return_value =json.loads(sample_trello_lists_response)
        return response
    elif url[-6:] == '/cards':
        response = Mock()
        # sample_trello_cards_response should pointto some test response data
        sample_trello_cards_response='[{"id":"5fda751bc2a79447fa921c8b","checkItemStates":null,"closed":false,"dateLastActivity":"2021-03-23T18:45:29.636Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fda74f60fc61c6f342225ce","idList":"5fda74f60fc61c6f342225d1","idMembersVoted":[],"idShort":3,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Do Exercise 2","pos":252927,"shortLink":"43ASCkOn","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/43ASCkOn","start":null,"subscribed":false,"url":"https://trello.com/c/43ASCkOn/3-do-exercise-2","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light","idPlugin":null}},{"id":"5fda7508cada764d36ea088c","checkItemStates":null,"closed":false,"dateLastActivity":"2021-02-08T16:45:31.243Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fda74f60fc61c6f342225ce","idList":"5fda74f60fc61c6f342225d1","idMembersVoted":[],"idShort":1,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Finish knowledge checks Module 2","pos":253951,"shortLink":"GKtEMSt2","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/GKtEMSt2","start":null,"subscribed":false,"url":"https://trello.com/c/GKtEMSt2/1-finish-knowledge-checks-module-2","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light","idPlugin":null}},{"id":"604dfc978e51d08685b09fb9","checkItemStates":null,"closed":false,"dateLastActivity":"2021-03-18T16:02:27.195Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fda74f60fc61c6f342225ce","idList":"5fda74f60fc61c6f342225d1","idMembersVoted":[],"idShort":23,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Test 3","pos":294911,"shortLink":"N0wL6YJa","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/N0wL6YJa","start":null,"subscribed":false,"url":"https://trello.com/c/N0wL6YJa/23-test-3","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light","idPlugin":null}},{"id":"604df7f55840112557e09923","checkItemStates":null,"closed":false,"dateLastActivity":"2021-03-14T12:01:11.555Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fda74f60fc61c6f342225ce","idList":"5fda74f60fc61c6f342225d1","idMembersVoted":[],"idShort":21,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"Testing done items","pos":393215,"shortLink":"cpN3SYZM","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/cpN3SYZM","start":null,"subscribed":false,"url":"https://trello.com/c/cpN3SYZM/21-testing-done-items","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light","idPlugin":null}},{"id":"604e0b5ec1e43b7103094a9c","checkItemStates":null,"closed":false,"dateLastActivity":"2021-03-14T13:10:54.983Z","desc":"","descData":null,"dueReminder":null,"idBoard":"5fda74f60fc61c6f342225ce","idList":"5fda74f60fc61c6f342225d1","idMembersVoted":[],"idShort":24,"idAttachmentCover":null,"idLabels":[],"manualCoverAttachment":false,"name":"recent test","pos":458751,"shortLink":"NLGqOeVG","isTemplate":false,"cardRole":null,"badges":{"attachmentsByType":{"trello":{"board":0,"card":0}},"location":false,"votes":0,"viewingMemberVoted":false,"subscribed":false,"fogbugz":"","checkItems":0,"checkItemsChecked":0,"checkItemsEarliestDue":null,"comments":0,"attachments":0,"description":false,"due":null,"dueComplete":false,"start":null},"dueComplete":false,"due":null,"idChecklists":[],"idMembers":[],"labels":[],"shortUrl":"https://trello.com/c/NLGqOeVG","start":null,"subscribed":false,"url":"https://trello.com/c/NLGqOeVG/24-recent-test","cover":{"idAttachment":null,"color":null,"idUploadedBackground":null,"size":"normal","brightness":"light","idPlugin":null}}]'
        response.json.return_value =json.loads(sample_trello_cards_response)
        return response
    return None