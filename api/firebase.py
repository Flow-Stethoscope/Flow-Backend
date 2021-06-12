import pyrebase
import json
import os


def uploadFile(path: str):
    config = json.load(open('../../../development/Flow-Backend/api/config.json'))
    credentials = json.load(open('../../../development/Flow-Backend/api/credentials.json'))
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    user = auth.sign_in_with_email_and_password(credentials["email"], credentials["password"])
    storage = firebase.storage()
    storage.child(path).put(path, user['idToken'])
    url = (storage.child(path).get_url(user['idToken']))
    print(url)
    return url

# if __name__ == '__main__':
#     uploadFile("firebase.py")
