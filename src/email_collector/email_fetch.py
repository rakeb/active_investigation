import imaplib
import os
import pickle
import sys

from pip._vendor.distlib.compat import raw_input

import gmail_auth  as oauth2

sys.path.insert(0, '/Users/mislam7/Dropbox/PycharmProjects/emialmutation/src/clients')
dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.sep)
from client_credential import Credential

CLIENT_ID = None
CLIENT_SECRET = None

'''Google Developers Console
https://console.developers.google.com/'''

email_id = None
client_id = None
client_secret = None


def auth():
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    print('To authorize token, visit this url and follow the directions:')
    print(' %s' % oauth2.GeneratePermissionUrl(client_id))

    authorization_code = raw_input('Enter verification code: ')
    response = oauth2.AuthorizeTokens(client_id, client_secret, authorization_code)
    print("Refresh Toke :", response['refresh_token'])
    print("Access Token :", response['access_token'])
    print("Expires in :", response['expires_in'])
    return response


def collect_email(response):
    emailid = "rakeb.void@gmail.com"
    client_id = CLIENT_ID
    client_secret = CLIENT_SECRET
    refresh_token = response['refresh_token']
    access_token = response['access_token']
    oauth2String = oauth2.GenerateOAuth2String(emailid, access_token,
                                               base64_encode=False)  # before passing into IMAPLib access token needs to be converted into string
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.authenticate('XOAUTH2', lambda x: oauth2String)
    mail.select("inbox")  # connect to inbox.
    # rest of the code to play with emails

    mail.list()
    # Out: list of "folders" aka labels in gmail.
    # mail.select("inbox")  # connect to inbox.
    result, data = mail.search(None, "ALL")

    ids = data[0]  # data is a list.
    id_list = ids.split()  # ids is a space separated string
    latest_email_id = id_list[-1]  # get the latest

    # fetch the email body (RFC822) for the given ID
    result, data = mail.fetch(latest_email_id, "(RFC822)")

    raw_email = data[0][1]  # here's the body, which is raw text of the whole email
    print (raw_email)


def write_response(file):
    pass


def read_user_credential():
    with open('/Users/mislam7/Dropbox/PycharmProjects/emialmutation/clients_secret/client_secret.pkl',
              'rb') as input:
        credential = pickle.load(input)
        return credential


def read_oauth_response():
    with open('/Users/mislam7/Dropbox/PycharmProjects/emialmutation/clients_secret/response.pkl',
              'rb') as input:
        response = pickle.load(input)
        return response


def input_client_credential():
    email_id = raw_input('Enter Client Email ID: ')
    client_id = raw_input('Enter Google OAuth2 Client ID: ')
    client_secret = raw_input('Enter OAuth2 Client Secret: ')

    with open('/Users/mislam7/Dropbox/PycharmProjects/emialmutation/clients_secret/client_secret.pkl',
              'wb') as output:
        client_credential = Credential(email_id, client_id, client_secret)
        pickle.dump(client_credential, output, pickle.HIGHEST_PROTOCOL)
        return client_credential


def save_oauth_respeonse(response):
    with open('/Users/mislam7/Dropbox/PycharmProjects/emialmutation/clients_secret/response.pkl', 'wb') as output:
        pickle.dump(response, output, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    try:
        credential = read_user_credential()
    except Exception as e:
        credential = input_client_credential()

    try:
        response = read_oauth_response()
    except Exception as e:
        try:
            response = auth()
            save_oauth_respeonse(response)
        except Exception as e:
            input_client_credential()
            response = auth()

    collect_email(response)
