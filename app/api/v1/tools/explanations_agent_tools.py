from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from typing import Any, Optional
from app.api.v1.helpers.vision import ImageInterpreter
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper


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
        
        it = ImageInterpreter()
        result = it.query_image(query_dict["image_url"], query_dict["query"])
        
        return result
