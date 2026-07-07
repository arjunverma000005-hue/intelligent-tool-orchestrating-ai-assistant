from dotenv import load_dotenv
load_dotenv()

import os
import requests
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import ToolMessage
from tavily import TavilyClient
from rich import print

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call

# Runnable imports
from langchain_core.runnables import RunnableLambda


# ---------------- WEATHER TOOL ---------------- #

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""

    API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Unable to fetch weather data')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"The current temperature in {city} is {temp}°C with {desc}."


# ---------------- NEWS TOOL ---------------- #

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def get_news(city: str) -> str:
    """Get latest news about the city"""

    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    results = response.get("results", [])

    if not results:
        return f"No news found for {city}."

    news_list = []

    for r in results:
        title = r.get("title", "No title")
        url = r.get("url", "")
        snippet = r.get("content", "")

        news_list.append(
            f"{title}\n - {url}\n - {snippet[:100]}..."
        )

    return f"Latest news in {city}:\n\n" + "\n\n".join(news_list)


# ---------------- LLM ---------------- #

llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.2
)


# ---------------- HUMAN APPROVAL ---------------- #

@wrap_tool_call
def human_approval(request, handler):
    """Ask user before executing tool"""

    tool_name = request.tool_call["name"]

    confirm = input(f"\nDo you want to execute tool '{tool_name}'? (yes/no): ")

    if confirm.lower() != "yes":
        return ToolMessage(
            content="Tool call denied by user",
            tool_call_id=request.tool_call["id"]
        )

    return handler(request)


# ---------------- AGENT ---------------- #

agent = create_agent(
    llm,
    tools=[get_weather, get_news],
    system_prompt="You are a helpful city assistant who can provide weather and news.",
    middleware=[human_approval]
)


# ---------------- RUNNABLE ---------------- #

def run_agent(user_input: str):
    """Runnable wrapper for agent"""

    result = agent.invoke({
        "messages": [
            {"role": "user", "content": user_input}
        ]
    })

    return result["messages"][-1].content


# Runnable pipeline
agent_runnable = RunnableLambda(run_agent)


# ---------------- AGENT LOOP ---------------- #

print("\nCity Intelligence Agent (Runnable Enabled)")
print("Type 'exit' to quit\n")

while True:

    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    response = agent_runnable.invoke(user_input)

    print("\nAI Agent:", response)