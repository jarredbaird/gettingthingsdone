from app import app
from models import db, Item, User
import os, json, requests

db.drop_all()
db.create_all()
''' u1 '''
u1 = User.register("jarredbaird@gmail.com", "jarred")
u1.google_email_address = "jarredbaird@gmail.com"
u1.google_refresh_token = "1//0dLppCanB2RT7CgYIARAAGA0SNwF-L9IrZIO7vVIM9e1N_mXsUB9gWTfS1jbQ0kBmaDs82qu5orMjwi9urY__sS3jOrIxeBeOypg"
""" reset the u1 historyId """
# get the access token using the refresh token
data = {
            'client_id': os.environ.get('google_client_id'),
            'client_secret': os.environ.get('google_client_secret'),
            'refresh_token': u1.google_refresh_token,
            'grant_type': 'refresh_token'}
r = requests.post('https://oauth2.googleapis.com/token', data=data)
accessJson = json.loads(r.text)
# got it. now send a watch request to set the history id
headers = {'Authorization': 'Bearer {}'.format(accessJson['access_token'])}
watchData={'topicName': "projects/taskpwner/topics/received-emails", 'labelIds': ["INBOX"]}
watchResponse = requests.post("https://gmail.googleapis.com/gmail/v1/users/me/watch", headers=headers, data=watchData)
watchJson = json.loads(watchResponse.text)
u1.google_history_id = watchJson['historyId']
# end historyId

'''u2'''
u2 = User.register("jenfisher719@gmail.com", "jen")
u2.google_email_address = "jenfisher719@gmail.com"
''' wont be needing this for a minute
u2.google_refresh_token = "1//0dLppCanB2RT7CgYIARAAGA0SNwF-L9IrZIO7vVIM9e1N_mXsUB9gWTfS1jbQ0kBmaDs82qu5orMjwi9urY__sS3jOrIxeBeOypg"
""" reset the u2 historyId """
# get the access token using the refresh token
data = {
            'client_id': os.environ.get('google_client_id'),
            'client_secret': os.environ.get('google_client_secret'),
            'refresh_token': u1.google_refresh_token,
            'grant_type': 'refresh_token'}
r = requests.post('https://oauth2.googleapis.com/token', data=data)
accessJson = json.loads(r.text)
# got it. now send a watch request to set the history id
headers = {'Authorization': 'Bearer {}'.format(accessJson['access_token'])}
watchData={'topicName': "projects/taskpwner/topics/received-emails", 'labelIds': ["INBOX"]}
watchResponse = requests.post("https://gmail.googleapis.com/gmail/v1/users/me/watch", headers=headers, data=watchData)
watchJson = json.loads(watchResponse.text)
u2.google_history_id = watchJson['historyId']
# end historyId
'''
u3 = User.register("eviluser@gmail.com", "evilpassword")
db.session.add_all([u1, u2, u3])
db.session.commit()


i1 = Item(
    i_title="meh, someday I'll workout",
    u_id = 1
)

i2 = Item(
    i_title="Gotta do it",
    u_id = 1
    )

i3 = Item(
    i_title="Shouldn't be able to see this",
    u_id = 2
)

db.session.add_all([i1, i2, i3])
db.session.commit()