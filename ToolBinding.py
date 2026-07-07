from dotenv import load_dotenv
load_dotenv()
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool

from rich import print

# createing tool

@tool
def get_text_length(text: str) -> int:
    """Returns the length of the given text."""
    return len(text)

llm =ChatMistralAI(model="mistral-small-2506")

#tool binding
llm_with_tool=llm.bind_tools([get_text_length])

result=llm.invoke('hello')
result2=llm_with_tool.invoke('hello')

print(result.content)
print()
print()
print()
print(result2.content)

