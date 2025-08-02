# agents.py

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool


def create_debater_agent(persona: str) -> AgentExecutor:
    """
    Creates a debater agent with a specific persona.
    
    Args:
        persona (str): The personality and role description for the debater
        
    Returns:
        AgentExecutor: A configured agent executor ready for debate
    """
    # Initialize ChatOpenAI model with GPT-4 Turbo
    llm = ChatOpenAI(model="gpt-4-turbo")
    
    # Create chat prompt template with persona and placeholders
    prompt = ChatPromptTemplate.from_messages([
        ("system", persona),
        ("user", "Topic: {topic}\n\nDebate History:\n{debate_history}"),
        ("placeholder", "{agent_scratchpad}")
    ])
    
    # Create tool-calling agent with LLM, prompt, and search tool
    agent = create_tool_calling_agent(llm, [search_tool], prompt)
    
    # Wrap in AgentExecutor and return
    agent_executor = AgentExecutor(agent=agent, tools=[search_tool], verbose=True)
    
    return agent_executor