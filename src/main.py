import gmail
import sheets
import json
import utils
import os
from model import Filterer

def setup(config):
    last_unix_time = None
    if not os.path.exists(config['time_filename']):
        last_unix_time = 0
    else:
        with open(config['time_filename'], 'r') as f:
            last_unix_time = int(f.read())

    with open(config['keywords_filename'], 'r') as f:
        keywords = f.read().splitlines()
    return last_unix_time, keywords

def cleanup(config, last_unix_time):
    with open(config['time_filename'], 'w') as f:
        f.write(str(last_unix_time))

def main():
    config = utils.load_config()

    # gmail_obj = gmail.Gmail()

    last_unix_time, keywords = setup(config)
    # scraped_emails = gmail_obj.fetch_emails(last_unix_time)

    with open('scraped_emails.json', 'r') as f:
        scraped_emails = json.load(f)
 
    print(f"Fetched {len(scraped_emails)} emails.")
    filterer = Filterer(keywords)
    filtered_emails = filterer.filter(scraped_emails)
    company_positions = filterer.extract_company_and_position(filtered_emails)
    print(f"Filtered {len(company_positions)} company positions.")
    # sheet_rows = [filterer.extract_company_and_position(email) for email in filtered_emails if email]
    with open('company_positions.json', 'w') as f:
        json.dump(company_positions, f, indent=4)
    # SheetObj = sheets.Sheet(config['sheet_filename'])
    # SheetObj.append_rows(company_positions)

    cleanup(config, scraped_emails[-1]['internal_date'])

if __name__ == "__main__":
    main()
