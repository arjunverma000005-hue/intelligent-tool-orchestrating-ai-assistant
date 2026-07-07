from dotenv import load_dotenv
load_dotenv()

import os
import requests
from langchain_mistralai import ChatMistralAI
from langchain.tools import tool
from langchain_core.messages import HumanMessage, ToolMessage
from tavily import TavilyClient
from rich import print


# ---------------- WEATHER TOOL ---------------- #

@tool
def get_weather(city: str) -> str:
    """Get current weather of a city"""

    API_KEY = os.getenv("OPEN_WEATHER_API_KEY")

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    print("[yellow]DEBUG:[/yellow]", data)

    if str(data.get("cod")) != "200":
        return f"Error: {data.get('message', 'Unable to fetch weather data')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    return f"The current temperature in {city} is {temp}°C with {desc}."


# Test weather tool
print(get_weather.invoke({"city": "Ghaziabad"}))


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


# Test news tool
print(get_news.invoke({"city": "Ghaziabad"}))


# ---------------- LLM ---------------- #

llm = ChatMistralAI(
    model="mistral-small-2506",
    temperature=0.2
)


# ---------------- TOOLS ---------------- #

tools = {
    "get_weather": get_weather,
    "get_news": get_news
}

llm_with_tools = llm.bind_tools(list(tools.values()))


# ---------------- AGENT LOOP ---------------- #

messages = []

print("\n[bold cyan]City Intelligence System[/bold cyan]")
print("Type 'exit' to quit\n")

running = True

while running:

    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "q"]:
        print("[red]Exiting...[/red]")
        break

    messages.append(HumanMessage(content=user_input))

    loop_count = 0

    while running:

        result = llm_with_tools.invoke(messages)
        messages.append(result)

        loop_count += 1
        if loop_count > 5:
            print("[red]Agent loop stopped for safety.[/red]")
            break

        if result.tool_calls:

            for tool_call in result.tool_calls:

                tool_name = tool_call["name"]

                confirm = input(
                    f"\nAgent wants to call tool '{tool_name}'. Proceed? (yes/no): "
                )

                if confirm.lower() in ["exit", "quit", "q"]:
                    print("[red]Exiting...[/red]")
                    running = False
                    break

                if confirm.lower() != "yes":
                    print("[yellow]Tool call denied.[/yellow]")
                    continue

                tool_result = tools[tool_name].invoke(tool_call["args"])

                messages.append(
                    ToolMessage(
                        content=tool_result,
                        tool_call_id=tool_call["id"]
                    )
                )

            if not running:
                break

            continue

        else:
            print("\n[green]Agent:[/green]", result.content)
            break