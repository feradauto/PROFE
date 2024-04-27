from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from typing import Any, Optional


class WizardAgent(BaseTool):
    name = "quiz_wizard"
    description = """Helps you creating a quiz"""

    def _run(
        self, query: dict, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        print("Query: ", query)
        res="Your quiz is now available on https://www.quiz.com"
        return res

class EnrichmentAgent(BaseTool):
    name = "enrichment"
    description = """Helps you enriching your study documents with information on the internet"""

    def _run(
        self, query: dict, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        print("Query: ", query)
        res="Your information has been enriched"
        return res

class StudyAgent(BaseTool):
    name = "study"
    description = """Helps you studying a quiz"""

    def _run(
        self, query: dict, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        print("Query: ", query)
        res="Your quiz is now available on https://www.quiz.com"
        return res
