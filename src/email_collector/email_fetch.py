import imaplib
import os
import pickle
import sys
import traceback

from pip._vendor.distlib.compat import raw_input

import gmail_auth  as oauth2

sys.path.insert(0, '/Users/mislam7/Dropbox/PycharmProjects/emialmutation/src/clients')
dir_path = os.path.dirname(os.path.realpath(__file__))
root_path = os.path.abspath(os.sep)
from client_credential import Credential

# CLIENT_ID = None
# CLIENT_SECRET = None

'''Google Developers Console
https://console.developers.google.com/'''

# email_id = None
# client_id = None
# client_secret = None


def auth(client_id, client_secret):
    try:
        print('To authorize token, visit this url and follow the directions:')
        print(' %s' % oauth2.GeneratePermissionUrl(client_id))

        authorization_code = raw_input('Enter verification code: ')
        response = oauth2.AuthorizeTokens(client_id, client_secret, authorization_code)
        print("Refresh Toke : %s" %response['refresh_token'])
        print("Access Token : %s" %response['access_token'])
        print("Expires in : %s" %response['expires_in'])
        return response
    except:
        raise Exception('Authentication failed while generating Access Token, '
                        'please retry or enter user credential again.\n')



def collect_email(response):
    emailid = "rakeb.void@gmail.com"
    # client_id = CLIENT_ID
    # client_secret = CLIENT_SECRET
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
    try:
        with open('/Users/mislam7/Dropbox/PycharmProjects/emialmutation/clients_secret/client_secret.pkl',
                  'rb') as input:
            credential = pickle.load(input)
            return credential
    except:
        raise Exception('Exception occurred while reading user credential, please enter user credential again\n')


def read_oauth_response():
    try:
        with open('/Users/mislam7/Dropbox/PycharmProjects/emialmutation/clients_secret/response.pkl',
                  'rb') as input:
            response = pickle.load(input)
            return response
    except:
        raise Exception('Exception occurred while reading previous Access Token\n')


def input_client_credential():
    try:
        email_id = raw_input('Enter Client Email ID: \n')
        client_id = raw_input('Enter Google OAuth2 Client ID: \n')
        client_secret = raw_input('Enter OAuth2 Client Secret: \n')

        with open('/Users/mislam7/Dropbox/PycharmProjects/emialmutation/clients_secret/client_secret.pkl',
                  'wb') as output:
            client_credential = Credential(email_id, client_id, client_secret)
            pickle.dump(client_credential, output, pickle.HIGHEST_PROTOCOL)
            print ("User credential saved for further use.\n")
            return client_credential
    except:
        raise Exception('Exception occurred while inputting user credential\n')


def save_oauth_respeonse(response):
    with open('/Users/mislam7/Dropbox/PycharmProjects/emialmutation/clients_secret/response.pkl', 'wb') as output:
        pickle.dump(response, output, pickle.HIGHEST_PROTOCOL)
    print ("Access Token saved for further use.\n")


def complete_auth():
    pass


if __name__ == '__main__':
    # try:
    #     credential = read_user_credential()
    # except Exception as e:
    #     credential = input_client_credential()
    #
    # try:
    #     response = read_oauth_response()
    # except Exception as e:
    #     try:
    #         response = auth()
    #         save_oauth_respeonse(response)
    #     except Exception as e:
    #         input_client_credential()
    #         response = auth()
    response = None
    credential = None
    while 1:
        print('To get current session user ID, Press "0"\n'
              'To enter user credential, Press "1"\n'
              'To authenticate, Press "2"\n'
              'To read inbox message, Press "3"\n')
        y = raw_input()
        try:
            if y == '0':
                credential = read_user_credential()
                print('Current session for user: %s\n' %credential.email_id)
            if y == '1':
                credential = input_client_credential()
            if y == '2':
                credential = read_user_credential()
                response = auth(credential.client_id, credential.client_secret)
                save_oauth_respeonse(response)
            if y == '3':
                response = read_oauth_response()
                collect_email(response)
        except Exception:
            traceback.print_exc()
