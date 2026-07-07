from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool

from rich import print

# creating tool

@tool
def get_text_length(text: str) -> int:
    """Returns the number of characters in the given text."""
    return len(text)

llm =ChatMistralAI(model="mistral-small-2506")

#LLm decide to call the tool based on the user query
llm_with_tool=llm.bind_tools([get_text_length])
result2=llm_with_tool.invoke("use the get_text_length tool to find the length of the text 'hello how are you'")


print(result2.tool_calls[0])
print(get_text_length.invoke( {"text": "hello how are you"}))
