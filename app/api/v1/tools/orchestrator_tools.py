from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from loguru import logger
from typing import Any, Optional
from app.api.v1.agents.enrichment_agent import EnrichmentAgent
from app.api.v1.helpers.vision import ImageInterpreter as II
from app.api.v1.helpers.vision import PDFInterpreter as PI
from app.api.v1.global_config.global_config import audio_config

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


class PDFInterpreter(BaseTool):
    name = "pdf_interpreter"
    description = """ask questions about pdf files. It receives a JSON with the keys 'pdf_url' and 'query'"""
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

        ii = II()
        pi = PI()

        # currenntly only the first page is used for interpreting
        pdf_in_images = pi.convert_pdf_to_images(query_dict["pdf_url"])
        if pdf_in_images is None:
            return "Provide a valid pdf url"
        result = ii.query_image(pdf_in_images[0], query_dict["query"])

        return result


class AudioConfig(BaseTool):
    name = "response_config"
    description = """Useful to change the response settings and respond with audios. It receives a JSON with the key 'audio' and value True or False"""
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

        if 'audio' in query_dict:
            if query_dict['audio'] == True:
                if self.whatsapp not in audio_config:
                    audio_config[self.whatsapp]= {'audio':True}
                else:
                    audio_config[self.whatsapp]['audio'] = True
            else:
                if self.whatsapp not in audio_config:
                    audio_config[self.whatsapp]= {'audio':False}
                else:
                    audio_config[self.whatsapp]['audio'] = False

        return "Configuration Updated"
