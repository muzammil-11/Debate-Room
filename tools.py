# tools.py

from langchain_community.tools.tavily_search import TavilySearchResults

# Initialize Tavily search tool with max 3 results
search_tool = TavilySearchResults(max_results=3)