from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from loguru import logger
from typing import Any, Optional
from app.api.v1.agents.enrichment_agent import EnrichmentAgent
from app.api.v1.helpers.vision import ImageInterpreter as II

class WizardAgentTool(BaseTool):
    name = "quiz_wizard"
    description = """Helps you creating a quiz"""
    whatsapp=""

    def _run(
        self, query: dict, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        debug_str = f"Running Agent with query: {query}"
        logger.debug(debug_str)
        res="Tool not available at the moment"
        return res

class EnrichmentAgentTool(BaseTool):
    name = "enrichment"
    description = """Helps you creating study collections and enriching your study documents with information on the internet"""
    whatsapp=""

    def _run(
        self, query: dict, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        enrichment_agent = EnrichmentAgent(self.whatsapp)
        debug_str = f"Running EnrichmentAgentTool with query: {query}"
        logger.debug(debug_str)
        res = enrichment_agent.run(query)
        return res

class StudyAgentTool(BaseTool):
    name = "study"
    description = """Helps you studying a quiz"""
    whatsapp=""

    def _run(
        self, query: dict, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        debug_str = f"Running Agent with query: {query}"
        logger.debug(debug_str)
        res="Tool not available at the moment"
        return res


class ImageInterpreter(BaseTool):
    name = "image_interpreter"
    description = """usuful when you need to answer questions about an image. It receives a JSON with the keys 'image_url' and 'query'"""
    whatsapp = ""

    def _run(
        self, query: dict, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        print("Query: ", query)
        ## scheck if it is dict
        if type(query) is not dict:
            query_dict = eval(query)
        else:
            query_dict = query

        it = II()
        result = it.query_image(query_dict["image_url"], query_dict["query"])

        return result
