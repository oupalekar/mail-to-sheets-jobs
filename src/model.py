import spacy
from find_job_titles import FinderAcora
import joblib
from itertools import compress

nlp = spacy.load("en_core_web_sm")

class Filterer:
    def __init__(self, keywords):
        self.keywords = keywords
        self.job_classifier = joblib.load("job_classifier.joblib")
        # self.ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")

    def filter(self, emails):
        filtered_emails = []
        for email in emails:
            text = f"{email['title']}\n{email['body']}".lower()
            if any(keyword in text for keyword in self.keywords):
                if all(keyword not in text for keyword in ['sorry', 'unfortunately', 'denied']):
                    if self.job_classifier.predict([text])[0] == 1:
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
                if ent.label_ == "POSITION":
                    position = ent.text
                    break   
            company_positions.append((company, position, email['date']))
        return company_positions