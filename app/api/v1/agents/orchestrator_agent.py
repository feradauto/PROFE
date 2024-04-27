from langchain.agents import initialize_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from app.api.v1.helpers.llm_callback import CustomCallbackHandler
from langchain import hub
import os 
from loguru import logger
from app.api.v1.tools.orchestrator_tools import WizardAgent, EnrichmentAgent, StudyAgent
from app.api.v1.helpers.messages import format_chat_history

## Class that represents the Orchestrator Agent with an init method that initializes it and a run method to run it
class OrchestratorAgent:
    def __init__(self, whatsapp):
        self.whatsapp = whatsapp
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro",
            google_api_key = os.getenv("GEMINI_API_KEY", ""),
            convert_system_message_to_human = True,
            verbose = True,
            return_intermediate_steps = True,
        )
        self.custom_callback_handler = CustomCallbackHandler()
        self.prompt = hub.pull("langchain-ai/react-agent-template")

    def get_conversation(self, whatsapp):
        chat_history=[{'role':'Human','message':'Hi, I am John'},
                        {'role':'Teacher','message':'Hi John!'}]
        chat = format_chat_history(chat_history)
        return chat

    def get_tools(self):
        enrichment = EnrichmentAgent()
        wizard = WizardAgent()
        study = StudyAgent()
        tools = [enrichment, wizard, study]
        return tools

    def run(self, message):
        instructions=f"""
You are a helpful teacher, expert in every topic. Your goal is to help students learning the topic of their choice.
"""
        prompt = hub.pull("langchain-ai/react-agent-template")
        stored_chat = self.get_conversation(self.whatsapp)
        tools_agent = self.get_tools()
        logger.info(prompt)
        agent_executor = initialize_agent(llm=self.llm, 
                                          tools=tools_agent, 
                                          prompt=prompt, 
                                          verbose = True, 
                                          handle_parsing_errors = True, 
                                          max_iterations = 2,
                                          early_stopping_method="generate")
        
        res=agent_executor.invoke({"input":message, "instructions":instructions,"chat_history":stored_chat},{"callbacks":[self.custom_callback_handler]})

        logger.info(res)
        return res['output']