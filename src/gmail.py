import os
import base64
import pickle
import datetime
from utils import authenticate_google
from multiprocessing import cpu_count
from joblib import Parallel, delayed
# email.py
# Handles Gmail API authentication and fetching emails
class Gmail:
    def __init__(self):
        self.service = authenticate_google('gmail', "v1")
    
    def fetch_emails(self, last_unix_time):
        print("Fetching emails...")
        email_ids = self.fetch_emails_ids(last_unix_time)
        num_cores = cpu_count()//2
        print(f"Using {num_cores} cores.")
        output = Parallel(n_jobs=num_cores)(delayed(self.get_email_contents)(email_id['id']) for email_id in email_ids)
        return output

    def get_email_contents(self, email_id):
        email = self.fetch_email_content(email_id)
        scraped_email = self.analyze_emails(email)
        return scraped_email

    def fetch_emails_ids(self, last_unix_time=None):
        query = None
        if last_unix_time:
            query = f'after:{int(last_unix_time)}'
        all_messages = []
        next_page_token = None
        while True:
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                pageToken=next_page_token
        ).execute()
            messages = results.get('messages', [])
            all_messages.extend(messages)
            next_page_token = results.get('nextPageToken')
            if not next_page_token:
                break
        all_messages.reverse()
        return all_messages

    def fetch_email_content(self, message_id):
        message = self.service.users().messages().get(userId='me', id=message_id).execute()
        return message

    def analyze_emails(self, email):
        """
        Analyze the email payload and return structured data.
        TODO: Implement email analysis logic.
        """

        title = self.get_email_title(email['payload'])
        body = self.get_email_body(email['payload'])
        internal_date = email['internalDate']
        scraped_email = {
            'title': title,
            'body': body,
            'date': datetime.datetime.fromtimestamp(int(internal_date) / 1000),
            'internal_date': internal_date
        }
        return scraped_email

    def get_email_title(self, payload):
        # Try the top-level subject first
        if payload['headers']:
            for header in payload['headers']:
                if header['name'] == 'Subject':
                    return header['value']
        return None

    def get_email_body(self, payload):
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
        return ""
    