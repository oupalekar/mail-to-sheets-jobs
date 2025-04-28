import spacy
import joblib
import openai
from openai import OpenAI
import os
from dotenv import load_dotenv
import json
from tqdm import tqdm
nlp = spacy.load("en_core_web_sm")

class Filterer:
    def __init__(self, keywords):
        load_dotenv()
        self.keywords = keywords
        self.job_classifier = joblib.load("job_classifier.joblib")
        # self.ner = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
        self.client = OpenAI(
            base_url = "https://integrate.api.nvidia.com/v1",
            api_key = os.getenv("OPENAI_API_KEY")
        )
        self.prompt = """
            You are a job title extractor.
            You must ONLY return a JSON string as your response. Do NOT use Markdown formatting, do NOT include triple backticks, and do NOT provide any explanation.
            If the email is not related to a job application, respond with an empty JSON: {"company": "", "position": ""}.
            Else, extract the company name and position applied for from this email. Respond ONLY with a plain JSON string, not wrapped in any Markdown or code block.
            """

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
        for email in tqdm(emails):
            while True:
                try:
                    completion = self.client.chat.completions.create(
                        model="google/gemma-2b",
                        messages=[{"role":"user","content":self.prompt + "\n\n" + email['title'] + "\n\n" + email['body']}],
                        temperature=0.5,
                        top_p=1,
                        max_tokens=1024,
                        stream=True
                    )
                    full_response = ""
                    full_response_dict = None
                    for chunk in completion:
                        if chunk.choices[0].delta.content is not None:
                            content = chunk.choices[0].delta.content
                            full_response += content
                            try:
                                full_response_dict = json.loads(full_response)
                                break
                            except json.JSONDecodeError:
                                continue
                    company = full_response_dict['company']
                    position = full_response_dict['position']
                    company_positions.append((company, position, email['date']))
                    break  # Success, break the retry loop
                except Exception as e:
                    print(f"Error: {e}")
                    break
        return company_positions