import spacy
import re
from transformers import pipeline
from find_job_titles import FinderAcora

nlp = spacy.load("en_core_web_sm")

class Filterer:
    def __init__(self, keywords):
        self.keywords = keywords
        self.ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

    def filter(self, emails):
        filtered_emails = []
        for email in emails:
            text = f"{email['title']}\n{email['body']}".lower()
            if any(keyword in text for keyword in self.keywords):
                if all(keyword not in text for keyword in ['sorry', 'unfortunately', 'denied']):
                    filtered_emails.append(email)
        return filtered_emails

    def extract_company_and_position(self, emails):
        company_positions = []
        for email in emails:
            text = f"{email['title']}\n{email['body']}"
            entities = nlp(text).ents
            company = None
            position = None
            for ent in entities:
                if ent.label_ == "ORG":
                    company = ent.text
                    break

            finder = FinderAcora()
            position = [x.match for x in finder.finditer(text)][0]
            company_positions.append((company, position, email['date']))
        return company_positions