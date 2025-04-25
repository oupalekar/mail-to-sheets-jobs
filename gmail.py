import os
import base64
from google.auth.transport.requests import Request
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# email.py
# Handles Gmail API authentication and fetching emails

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
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
    service = build('gmail', 'v1', credentials=creds)
    return service
    
def fetch_emails(service, last_unix_time=None):
    query = None
    if last_unix_time:
        # Gmail expects seconds, not ms
        query = f'after:{int(last_unix_time)}'
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    return messages
    
def fetch_email_content(service, message_id):
    message = service.users().messages().get(userId='me', id=message_id).execute()
    return message

def analyze_email(payload):
    """
    Analyze the email payload and return structured data.
    TODO: Implement email analysis logic.
    """
    print(get_email_title(payload))
    print(get_email_body(payload))

def get_email_title(payload):
    # Try the top-level subject first
    if payload['headers']:
        for header in payload['headers']:
            if header['name'] == 'Subject':
                return header['value']
    return None

def get_email_body(payload):
    # Try the top-level body first
    if payload['body'] and payload['body'].get('data'):
        data = payload['body']['data']
        return base64.urlsafe_b64decode(data).decode('utf-8')
    # Otherwise, check parts
    if 'parts' in payload:
        for part in payload['parts']:
            if part['mimeType'] == 'text/plain' and part['body'].get('data'):
                data = part['body']['data']
                return base64.urlsafe_b64decode(data).decode('utf-8')
            # Optionally, handle 'text/html' if you want HTML content
    return None
    