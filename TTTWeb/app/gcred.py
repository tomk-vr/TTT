from __future__ import print_function
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    #flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    Flags = None
except ImportError:
    flags = None

class GCredentials(object):
    """Get Google app credentials"""
    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/calendar-python-quickstart.json
 
    #SCOPES = 'https://www.googleapis.com/auth/calendar'
    SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
    #CRED_FILENAME = 'calendar-python-quickstart.json'
    CRED_FILENAME = 'sheets.googleapis.com-python-quickstart.json'
    #CLIENT_SECRET_FILE = 'client_secret.json'
    CLIENT_SECRET_FILE = 'sheet_client_secret.json'
    APPLICATION_NAME = 'Google Calendar API Python Quickstart'

    def __init__(self, **kwargs):
        if 'scope' in kwargs:
            self.SCOPES = kwargs['scope']
        if 'cfname' in kwargs:
            self.CRED_FILENAME = kwargs['cfname']
        if 'sfname' in kwargs:
            self.CLIENT_SECRET_FILE = kwargs['sfname']

        self.credentials = self.get_credentials();
        return super().__init__()

    def get_credentials(self):
        """Gets valid user credentials from storage.
    
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
    
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, self.CRED_FILENAME)
    
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.CLIENT_SECRET_FILE, self.SCOPES)
            flow.user_agent = self.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print('Storing credentials to ' + credential_path)
        return credentials

