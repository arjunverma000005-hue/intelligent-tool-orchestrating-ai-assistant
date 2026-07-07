import os
import requests
import streamlit as st
from dotenv import load_dotenv

from langchain_mistralai import ChatMistralAI
from langchain.tools import StructuredTool
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# ---------------- UI CONFIGURATION ---------------- #
st.set_page_config(page_title="City Intelligence Agent", page_icon="🏙️")
st.title("🏙️ City Intelligence Agent")
st.markdown("Ask me for the latest weather and news for any city!")

# ---------------- TOOLS ---------------- #
def get_weather_logic(city: str) -> str:
    """Get current weather of a city"""
    API_KEY = os.getenv("OPEN_WEATHER_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    response = requests.get(url)
    data = response.json()

    if str(data.get("cod")) != "200":
        return f"❌ Error: {data.get('message', 'Unable to fetch weather data')}"

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]
    # Added icon here
    return f"🌡️ **Weather Report:** The current temperature in {city} is {temp}°C with {desc}."

def get_news_logic(city: str) -> str:
    """Get latest news about the city"""
    tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
    response = tavily_client.search(
        query=f"latest news in {city}",
        search_depth="basic",
        max_results=3
    )

    results = response.get("results", [])
    if not results:
        return f"📭 No news found for {city}."

    news_list = [
        f"**{r.get('title', 'No title')}**\n\n{r.get('content', '')[:100]}...\n\n[🔗 Read more]({r.get('url', '')})"
        for r in results
    ]
    # Added icon here
    return f"📰 **Latest news in {city}:**\n\n---\n\n" + "\n\n---\n\n".join(news_list)

# ---------------- TOOL WRAPPER (ADAPTED FOR WEB) ---------------- #
def with_ui_notification(func, name: str, description: str):
    """Wraps a tool's logic to notify the user via Streamlit UI instead of a blocking terminal input."""
    def wrapper(*args, **kwargs):
        # Streamlit cannot pause mid-chain without LangGraph, so we use a toast/status notification 
        # to alert the user that a tool is being utilized.
        st.toast(f"Agent triggered tool: {name}", icon="⚙️")
        return func(*args, **kwargs)
    
    return StructuredTool.from_function(
        func=wrapper,
        name=name,
        description=description
    )

# Wrap our tools
weather_tool = with_ui_notification(get_weather_logic, "get_weather", "Get current weather of a city")
news_tool = with_ui_notification(get_news_logic, "get_news", "Get latest news about the city")
tools = [weather_tool, news_tool]

# ---------------- AGENT SETUP (CACHED) ---------------- #
@st.cache_resource
def setup_agent():
    llm = ChatMistralAI(
        model="mistral-small-latest",
        temperature=0.2
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful city assistant who can provide weather and news."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    agent = create_tool_calling_agent(llm, tools, prompt)
    return AgentExecutor(agent=agent, tools=tools, verbose=False)

agent_executor = setup_agent()

# ---------------- CHAT STATE MANAGEMENT ---------------- #
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat history with icons
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "🤖"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# ---------------- AGENT LOOP (STREAMLIT UI) ---------------- #
if user_input := st.chat_input("Type your question here..."):
    
    # 1. Add user message to state and UI
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # 2. Generate and display agent response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("💭 Thinking..."):
            try:
                # Invoke the agent directly
                result = agent_executor.invoke({"input": user_input})
                response = result["output"]
                st.markdown(response)
                
                # Save agent response to state
                st.session_state.messages.append({"role": "assistant", "content": response})
                
            except Exception as e:
                st.error(f"⚠️ An error occurred: {str(e)}")