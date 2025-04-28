# utils.py
# Helper functions for text analysis
from multiprocessing import cpu_count
from joblib import Parallel, delayed
from functools import partial
from itertools import compress
import os
import json
import base64
from google.auth.transport.requests import Request
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import re
# email.py
# Handles Gmail API authentication and fetching emails

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/drive.file']

def authenticate_google(service_type, version_type):
    """
    Authenticate with Gmail API and return service object.
    TODO: Implement authentication logic.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
    service = build(service_type, version_type, credentials=creds)
    return service


            
def load_config(file_name = None):
    if file_name is None:
        try:
            file_name = "config.json"
            cwd = os.getcwd()
            file_path = os.path.join(cwd, file_name)
            with open(file_path, 'r') as f:
                config = json.load(f)
                return config
        except FileNotFoundError:
            print(f"Config file '{file_name}' not found.")
            return None
    else:
        try:
            with open(file_name, 'r') as f:
                config = json.load(f)
                return config
        except FileNotFoundError:
            print(f"Config file '{file_name}' not found.")
            return None
            
        
CLEANR = re.compile('<.*?>')
def clean_string(string):
    cleantext = re.sub(CLEANR, '', string)
    return cleantext