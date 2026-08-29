from langchain.tools import tool
import requests
from dotenv import load_dotenv
import os 
from tavily import TavilyClient
from bs4 import BeautifulSoup
load_dotenv()

tavily=TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query: str) -> str:
    """Search the web for reliable and recent information on a topic. Returns title, url and snippet."""
    try:
        results = tavily.search(query=query, max_results=5)
    except Exception as e:
        return f"Error while searching: {e}"

    out = [f"Title:{r['title']}\nURL:{r['url']}\nCONTENT:{r['content'][:300]}\n" for r in results['results']]
    return "\n-----\n".join(out)

@tool
def scrape_webpage(url: str) -> str:
    """
    Scrapes readable text from a webpage. Returns at most ~3000 characters.
    """
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text[:3000]  # cap tool output before it ever reaches the LLM

    except requests.exceptions.RequestException as e:
        return f"Error while scraping website: {e}"

  
