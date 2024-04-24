from typing import Dict, List, Any
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema.output import LLMResult

class CustomCallbackHandler(BaseCallbackHandler):
    """Base callback handler that can be used to handle callbacks from langchain."""

    def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> Any:
        """Run when LLM starts running."""
        print("LLM START ###################")
        print(prompts[0])
        print("LLMSTART######################")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        """Run when LLM ends running."""
        print("LLM END ###################")
        print(response)
        print("LLMEND######################")
