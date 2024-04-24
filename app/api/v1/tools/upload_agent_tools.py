from langchain.tools import BaseTool
from typing import Any, Optional
from langchain.callbacks.manager import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun

LINKS_DB={}

class SaveLinks(BaseTool):
    name= "save_links"
    description = "This tool lets you save a link provided by the user. It receives a tuple  with the user, topic and link."

    def _run(self, link_info: tuple, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Use the tool"""
        link_info = eval(link_info)
        if not( link_info[0] in LINKS_DB.keys()):
            LINKS_DB[0] = { LINKS_DB[1]:LINKS_DB[2] }
        else:
            if not(link_info[1] in LINKS_DB[0].keys()):
                

