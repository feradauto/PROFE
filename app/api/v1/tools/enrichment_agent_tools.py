from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from typing import Any, Optional
from app.api.v1.helpers.db_manipulation import collections,write_collection_to_db

class StoreInformation(BaseTool):
    name = "store_in_collection"
    description = """stores knowledge in an existent collection. It receives a JSON with the keys 'collection':collection_name,'subtopic':subtopic_name,'information':the subtopic information"""
    whatsapp=""
    def _run(
        self, query: dict, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        print("Query: ", query)
        ## scheck if it is dict
        if type(query) is not dict:
            query_dict=eval(query)
        else:
            query_dict=query
        result = write_collection_to_db(query_dict['information'],self.whatsapp,query_dict['collection'],query_dict['subtopic'])
        if result:
            res="Topic stored succesfully"
        else:
            res="Error storing information"
        return res
