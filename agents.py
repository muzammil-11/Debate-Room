# agents.py

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool


def create_debater_agent(persona: str) -> AgentExecutor:
    """
    Creates a sophisticated debater agent with tool-calling capabilities.
    
    This function constructs a debate agent that can engage in structured arguments
    using GPT-4 Turbo and has access to web search tools for evidence gathering.
    The agent is designed to participate in formal debates with specific personas
    and can access current information to support its arguments.
    
    Args:
        persona (str): A detailed system prompt defining the debater's personality,
            arguing style, and strategic approach. This should include instructions
            on how the agent should behave, what tone to use, and any specific
            debate strategies or characteristics that define this debater's role
            (e.g., "proposition" vs "opposition").
    
    Returns:
        AgentExecutor: A fully configured agent executor that can:
            - Process debate topics and history
            - Generate coherent arguments based on the given persona
            - Use web search tools to find supporting evidence
            - Maintain context throughout multi-turn debates
            - Follow the debate format and rules embedded in the persona
    
    Example:
        >>> persona = "You are a confident proposition debater who always..."
        >>> debater = create_debater_agent(persona)
        >>> result = debater.invoke({
        ...     "topic": "Should AI be regulated?",
        ...     "debate_history": "Previous arguments here..."
        ... })
    
    Note:
        The agent requires valid OpenAI API credentials and Tavily API key
        to be set in the environment for full functionality.
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