from langchain.agents import initialize_agent
from langchain.tools import BaseTool
import os
from langchain.agents import initialize_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from app.api.v1.helpers.llm_callback import CustomCallbackHandler
from loguru import logger
from app.api.v1.tools.form_creator_tool import GoogleFormsAPI
import os
from app.api.v1.helpers.db_manipulation import read_message_from_db 

credentials_path = os.getenv('GOOGLE_CREDENTIAL_PATH')
credentials_file = os.path.join(credentials_path, 'credentials.json') if credentials_path else None


PREFIX = """Generate the Google form based on the topic provided by the user use the provided tools.
Each question in the  quiz should contain question_text, question_type, options and answer_key
"""
FORMAT_INSTRUCTIONS = """
You have access to the following tools {tool_names}:


Use the following format:

Question: The quiz you are trying to generate should follow the format of google form payload format . 

Thought: you should always think about what to do

Action: the action to take, should be one of [{tool_names}]

Action Input: the input to the action is in json format with the keys that google form understands. 
Observation: the result of the action

... (this Thought/Action/Action Input/Observation can repeat N times)

Thought: I now know the final answer

Final Answer: the final answer to the original input question"""
SUFFIX = """Begin!

Question: {input}
Thought:{agent_scratchpad}
Begin!
"""

                
class QuizWizardAgent:
    def __init__(self, whatsapp):
        self.whatsapp = whatsapp
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            google_api_key=os.getenv("GEMINI_API_KEY", ""),
            convert_system_message_to_human=True,
            verbose=True,
            return_intermediate_steps=True,
        )
        self.google_forms_api = GoogleFormsAPI(credentials_file)
        self.custom_callback_handler = CustomCallbackHandler()

    def get_conversation(self):
        """Fetch chat history from the database."""
        chat_history = read_message_from_db(self.whatsapp)
        return chat_history

    def run(self, topic, num_questions):
        """Generate a quiz in google form based on the specified topic and number of questions."""
        agent_executor = initialize_agent(
            llm=self.llm,
            tools=[self.google_forms_api],
            agent_kwargs={
                'prefix': PREFIX,
                'suffix': SUFFIX,
                'format_instructions': FORMAT_INSTRUCTIONS 
            },
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=2,
            early_stopping_method="generate"
        )

        input_message = f"Generate {num_questions} questions about {topic}"
        chat_history = self.get_conversation()
        

        input_data = {
            "input": input_message,
            "chat_history": chat_history
        }
        

        res = agent_executor.invoke(input_data, {"callbacks": [self.custom_callback_handler]})
        return res
