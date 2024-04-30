from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from typing import Optional
import os
import pickle
import json

class GoogleFormsAPI(BaseTool):
    name = "google_forms"
    description = "Tool for creating and managing Google Forms."
    credentials_file = ""
    token_path = ""
    service = ""
    
    SCOPES = ['https://www.googleapis.com/auth/forms.body']

    def __init__(self, credentials_file):
        super().__init__()
        self.credentials_file = f"{os.getenv('GOOGLE_CREDENTIAL_PATH')}/credentials.json" 
        self.token_path = os.path.join(os.path.dirname(self.credentials_file), 'token.pickle')
        self.service = self.authenticate()



    def authenticate(self):
        """Authenticate with Google and return the service object, reusing tokens if valid."""
        creds = None
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print("Failed to refresh token: ", e)
                    creds = self.get_new_credentials()
            else:
                creds = self._get_new_credentials()
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)

        return build('forms', 'v1', credentials=creds)

    def _get_new_credentials(self):
        """Helper function to handle obtaining new credentials."""
        try:
            flow = InstalledAppFlow.from_client_secrets_file(self.credentials_file, self.SCOPES)
            return flow.run_local_server(port=0)
        except Exception as e:
            print("Failed to obtain new credentials: ", e)
            return None


    def _run(self, input_payload: str, run_manager: Optional[CallbackManagerForToolRun] = None):
        json_payload = self._clean_json_string(input_payload)
        payload = json.loads(json_payload)
        """Create and update a Google Form based on the provided json formated question set."""
        print(f"Data type of payload is {type(payload)}")
        print(f"Payload is {payload}")
        title = payload.get('title', "Default quiz title")
        questions = payload.get('questions', [])
        
        form_id = self.create_form(title)
        if questions:
            self.add_questions(form_id, questions)
        
        return form_id

    def create_form(self, title):
        """Create a new Google Form with a given title and return the form ID."""
        form_body = {"info": {"title": title}}
        form = self.service.forms().create(body=form_body).execute()
        return form.get('formId')

    def add_questions(self, form_id, questions):
        """Add questions to the specified Google Form."""
        print(f"form ID is {form_id}, questions are : {questions}")
        requests = []
        for question in questions:
            new_item_request = {
                "createItem": {
                    "item": {
                        "title": question['question_text'],
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [{"value": opt} for opt in question['options']],
                                    "shuffle": True
                                }
                            }
                        }
                    },
                    "location": {"index": questions.index(question)}
                }
            }
            requests.append(new_item_request)
        
        update_body = {"requests": requests}
        self.service.forms().batchUpdate(formId=form_id, body=update_body).execute()

    def _clean_json_string(self, input_string):
        """
        Cleans a JSON string by removing markdown code block tags and other formatting artifacts.
        """

        lines = input_string.strip().splitlines()
        
        if lines[0].startswith('```') and lines[-1].startswith('```'):
            lines = lines[1:-1]  # Remove the first and last line which are assumed to be ```json and ```
        
        cleaned_string = '\n'.join(lines).strip()
        
        return cleaned_string