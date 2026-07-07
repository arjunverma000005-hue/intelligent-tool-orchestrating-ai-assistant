from dotenv import load_dotenv
load_dotenv()
import langchain
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage

from rich import print

# creating tool

@tool
def get_text_length(text: str) -> int:
    """Returns the number of characters in the given text."""
    return len(text)

tools={
    "get_text_length":get_text_length
}
llm =ChatMistralAI(model="mistral-small-2506")

#LLm decide to call the tool based on the user query
llm_with_tool=llm.bind_tools([get_text_length])

message=[]
prompt=input('you: ')
query=HumanMessage(prompt)
message.append(query)
# print(message)


result=llm_with_tool.invoke(message)
message.append(result)

if result.tool_calls:
   
    tool_name=result.tool_calls[0]['name']
    tool_message=tools[tool_name].invoke(result.tool_calls[0])
    print(tool_message)
    message.append(tool_message)
    print(message)

result=llm_with_tool.invoke(message)
print(result.content)

