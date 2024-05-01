from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Optional
import os
import pickle
import json
from loguru import logger


PROMPT = """

Generate google quiz based on user question topic and number of  questions. All  question should be radio type. 
Respect this format of structure . Generate the questions and answers in spanish .  

{
  "info": {
    "title": "Biochemistry Quiz",
    "description": "Test your understanding of key biochemistry concepts."
  },
  "items": [
    {
      "title": "What is the building block of proteins?",
      "questionItem": {
        "question": {
          "textQuestion": {
            "paragraph": false
          }
        },
        "required": true,
        "choiceQuestion": {
          "type": "RADIO",
          "options": [
            {"value": "Carbohydrates"},
            {"value": "Lipids"},
            {"value": "Amino acids"},
            {"value": "Nucleic acids"}
          ],
          "shuffle": true
        }
      },
      "correctAnswer": {
        "value": "Amino acids"
      }
    },
    {
      "title": "Which molecule carries genetic information?",
      "questionItem": {
        "question": {
          "textQuestion": {
            "paragraph": false
          }
        },
        "required": true,
        "choiceQuestion": {
          "type": "RADIO",
          "options": [
            {"value": "DNA"},
            {"value": "RNA"},
            {"value": "Proteins"},
            {"value": "Enzymes"}
          ],
          "shuffle": true
        }
      },
      "correctAnswer": {
        "value": "DNA"
      }
    },
    {
      "title": "What is the primary energy currency of cells?",
      "questionItem": {
        "question": {
          "textQuestion": {
            "paragraph": false
          }
        },
        "required": true,
        "choiceQuestion": {
          "type": "RADIO",
          "options": [
            {"value": "Glucose"},
            {"value": "ATP"},
            {"value": "Water"},
            {"value": "Oxygen"}
          ],
          "shuffle": true
        }
      },
      "correctAnswer": {
        "value": "ATP"
      }
    }
  ]
}
```


"""


class GoogleFormsAPITool():
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
                    creds = self._get_new_credentials()
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


    def run(self, input_payload: str):
        raw_generated_quiz = self._call_gemini_api(input_payload)
        print(raw_generated_quiz)
        json_payload = self._clean_json_string(raw_generated_quiz)
        payload = json.loads(json_payload)
        """Create and update a Google Form based on the provided json formated question set."""
        print(f"Data type of payload is {type(payload)}")
        print(f"Payload is {payload}")
        title = payload.get('info', 'test').get('title', "Default quiz title")
        questions = payload.get('items', [])
        
        form_id = self.create_form(title)
        if questions:
            form_url = self.setup_quiz(form_id, questions)

        #form_url = self._convert_form_to_quiz(form_id)
 
        return form_url

    def create_form(self, title):
        """Create a new Google Form with a given title and return the form ID."""
        form_body = {"info": {"title": title}}
        form = self.service.forms().create(body=form_body).execute()
        return form.get('formId')


    def setup_quiz(self, form_id, questions):
        """
        Setups up the Google Form as a quiz and adds questions to it.
        """
        # First, convert the form to a quiz
        form_url = self._convert_form_to_quiz(form_id)
        if not form_url:
            print("Error converting form to a quiz. Aborting question addition.")
            return None

        # If the form has been successfully converted, proceed to add questions
        try:
            self.add_questions(form_id, questions)
            print("Questions successfully added to the quiz.")
        except Exception as e:
            print(f"Error adding questions to the quiz: {e}")
            return None

        return form_url

    def add_questions(self, form_id, questions):
        """Add questions to the specified Google Form including correct answers and grading."""
        print(f"Form ID is {form_id}, questions are: {questions}")
        requests = []
        for index, question in enumerate(questions):
            options = [{"value": opt["value"]} for opt in question['questionItem']['choiceQuestion']['options']]
            correct_answer_value = question['correctAnswer']['value']

            grading = {
                "pointValue": question.get('pointValue', 1),  # Default point value if not specified
                "correctAnswers": {
                    "answers": [{"value": correct_answer_value}]
                },
                "whenRight": {"text": "¡Correcto! Buen trabajo, sigue así."},
                "whenWrong": {"text": "Incorrecto. ¡No te desanimes, sigue preparándote y lo conseguirás"}
            }

            new_item_request = {
                "createItem": {
                    "item": {
                        "title": question['title'],
                        "questionItem": {
                            "question": {
                                "required": True,
                                "grading": grading,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": options,
                                    "shuffle": True
                                }
                            }
                        }
                    },
                    "location": {
                        "index": index
                    }
                }
            }
            requests.append(new_item_request)

        update_body = {"requests": requests}
        self.service.forms().batchUpdate(formId=form_id, body=update_body).execute()
        print("Questions added to the form successfully with grading and feedback.")


    def _clean_json_string(self, input_string):
        """
        Cleans a JSON string by removing markdown code block tags and other formatting artifacts.
        """

        lines = input_string.strip().splitlines()
        
        if lines[0].startswith('```') and lines[-1].startswith('```'):
            lines = lines[1:-1]  # Remove the first and last line which are assumed to be ```json and ```
        
        cleaned_string = '\n'.join(lines).strip()
        
        return cleaned_string

    def _convert_form_to_quiz(self, form_id):
        """
        Converts the specified Google Form into a quiz and returns the URL of the quiz.
        """
        try:
            # JSON to convert the form into a quiz
            update = {
                "requests": [
                    {
                        "updateSettings": {
                            "settings": {"quizSettings": {"isQuiz": True}},
                            "updateMask": "quizSettings.isQuiz"
                        }
                    }
                ]
            }
            
            # Converts the form into a quiz
            self.service.forms().batchUpdate(formId=form_id, body=update).execute()
            
            # Generate the URL of the quiz
            form_url = f"https://docs.google.com/forms/d/{form_id}/viewform"
            return form_url
        except Exception as e:
            print(f"Failed to convert the form to a quiz or generate URL: {e}")
            return None



  
    def _call_gemini_api(self, input_payload = "random academic topic", num_questions= 5):
        "Calls via a single call to gemini AI"
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", google_api_key=os.getenv("GEMINI_API_KEY", ""),)
        result = llm.invoke(f"{PROMPT}+ Topic is : {input_payload} Total number of question to be generated is {num_questions}")
        print(result.content)
        return result.content

       