import gmail
import sheets
import utils

def main():

    service = gmail.authenticate_gmail()

    last_unix_time = None
    with open('stored_unix_time.txt', 'r') as f:
        last_unix_time = int(f.read())

    emails = gmail.fetch_emails(service, last_unix_time)

    for email in emails:
        email_content = gmail.fetch_email_content(service, email['id'])
        gmail.analyze_email(email_content['payload'])
        break
        last_unix_time = email_content['internalDate']
    
    with open('stored_unix_time.txt', 'w') as f:
        f.write(str(last_unix_time))

if __name__ == "__main__":
    main()
