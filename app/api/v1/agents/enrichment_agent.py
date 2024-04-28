from langchain.agents import initialize_agent, AgentType
from langchain_google_genai import ChatGoogleGenerativeAI
from app.api.v1.helpers.llm_callback import CustomCallbackHandler
from langchain import hub
import os 
from loguru import logger
from app.api.v1.tools.enrichment_agent_tools import StoreInformation
from langchain.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from app.api.v1.helpers.messages import format_chat_history
from app.api.v1.helpers.db_manipulation import read_message_from_db, read_collections_from_db

PREFIX = """
You are a helpful teacher that always gets the information using the available tools. Your goal is to help a student enrich the information they have about a specific topic.
You have 2 main tasks:
1. Figure out if the student wants to enrich their information using wikipedia.
2. Retrieve information about a specific topic from wikipedia
3. Store the information in the corresponding collection
Please NEVER use your internal information ALWAYS get the information from your tools.
The student you have to help has the following collections of topics: {collections_info}
You have access to the following tools:"""
FORMAT_INSTRUCTIONS = """Use a json blob to specify a tool by providing an action key (tool name) and an action_input key (tool input).

Valid "action" values: "Final Answer" or {tool_names}

Provide only ONE action per $JSON_BLOB, as shown:

```
{{{{
  "action": $TOOL_NAME,
  "action_input": $INPUT
}}}}
```

Follow this format:

Question: input question to answer
Thought: consider previous and subsequent steps
Action:
```
$JSON_BLOB
```
Observation: action result
... (repeat Thought/Action/Observation N times)
Thought: I know what to respond
Action:
```
{{{{
  "action": "Final Answer",
  "action_input": "Final response to human"
}}}}
```"""
SUFFIX = """Begin! Reminder to ALWAYS respond with a valid json blob of a single action. Use tools if necessary. Respond directly if appropriate. Format is Action:```$JSON_BLOB```then Observation:.
Thought:"""
HUMAN_MESSAGE="{input}\n\n{agent_scratchpad}"



## Class that represents the Orchestrator Agent with an init method that initializes it and a run method to run it
class EnrichmentAgent:
    def __init__(self, whatsapp):
        self.whatsapp = whatsapp
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro",
            google_api_key = os.getenv("GEMINI_API_KEY", ""),
            convert_system_message_to_human = True,
            verbose = True,
            return_intermediate_steps = True,
        )
        self.custom_callback_handler = CustomCallbackHandler()

    def get_conversation(self):
        chat_history = read_message_from_db(self.whatsapp)
        chat = format_chat_history(chat_history)
        return chat

    def get_tools(self):
        store_info = StoreInformation()
        store_info.whatsapp=self.whatsapp
        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        tools = [store_info, wikipedia]
        return tools

    def get_collections_info(self):
        collections=read_collections_from_db(self.whatsapp)
        topics=""
        if collections:
            for topic in collections.keys():
                topics+=f"{topic} ,"
        else:
            topics="No information available"
        return topics

    def run(self, message):
        stored_chat = self.get_conversation()
        tools_agent = self.get_tools()
        collections_info = self.get_collections_info()
        agent_executor = initialize_agent(llm=self.llm,
                                          agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                                          tools=tools_agent, 
                                          agent_kwargs={'prefix':PREFIX, 'suffix':SUFFIX, 'format_instructions':FORMAT_INSTRUCTIONS, "human_message_template":HUMAN_MESSAGE}, 
                                          verbose = True, 
                                          handle_parsing_errors = True, 
                                          max_iterations = 3,
                                          early_stopping_method="generate")
        
        res=agent_executor.invoke({"input":message, "chat_history":stored_chat, "collections_info":collections_info},{"callbacks":[self.custom_callback_handler]})

        logger.info(res)
        return res['output']