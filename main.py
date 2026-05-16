from fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup

# Create MCP server instance
mcp = FastMCP("Blue Report MCP Server")

def scrape_stories(endpoint: str, limit : int=10) -> dict:
    """Scrape stories from Blue Report endpoint"""
    url = f"https://bsky-social.github.io/blue-dot-report/{endpoint}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        stories = []
        
        # Parse the stories (adjust selectors as needed)
        for story in soup.find_all('div', class_='story'):  # Update selector based on actual HTML
            title = story.find('h2')
            link = story.find('a')
            if title and link:
                stories.append({
                    'title': title.get_text().strip(),
                    'url': link.get('href', '')
                })
        
        return {
            'endpoint': endpoint,
            'total_stories': len(stories),
            'stories': stories
        }
        
    except Exception as e:
        return {'error': f'Failed to fetch stories: {str(e)}'}

@mcp.tool()
def blue_report_hourly(limit: int = 10) -> dict:
    """Fetch hourly top stories from The Blue Report"""
    return scrape_stories('hour')

@mcp.tool()
def blue_report_daily(limit: int = 10) -> dict:
    """Fetch daily top stories from The Blue Report"""  
    return scrape_stories('day')

@mcp.tool()
def blue_report_weekly(limit: int = 10) -> dict:
    """Fetch weekly top stories from The Blue Report"""
    return scrape_stories('week')

if __name__ == "__main__"  :
    mcp.run()