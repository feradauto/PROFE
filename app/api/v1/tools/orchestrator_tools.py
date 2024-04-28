from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from loguru import logger
from typing import Any, Optional
from app.api.v1.agents.enrichment_agent import EnrichmentAgent

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
