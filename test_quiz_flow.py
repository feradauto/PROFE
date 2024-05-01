from dotenv import load_dotenv
from app.api.v1.tools.form_creator_tool import GoogleFormsAPITool
import os

load_dotenv(".env")

print("Starting quiz generation")
#quiz = QuizWizardAgent(whatsapp = '12345')
#quiz.whatsapp = '12345'
#form_id = quiz.run(topic = 'biochemistry', num_questions = 3)
#print(form_id)
result = GoogleFormsAPITool(credentials_file="").run(input_payload = "physics")
print(result)