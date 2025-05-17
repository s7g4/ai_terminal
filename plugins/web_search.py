from core.plugin_template import BasePlugin
import requests
from bs4 import BeautifulSoup
import urllib.parse

class WebSearchPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        
    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args:
            return "Please provide a search query (e.g. 'search for python tutorials')"
            
        # Parse voice command
        intent, query = self.parse_voice_command(" ".join(args))
        return self.search(query)

    def search(self, query):
        try:
            encoded_query = urllib.parse.quote_plus(query)
            search_url = f"https://www.google.com/search?q={encoded_query}"
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(search_url, headers=headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, "html.parser")
            results = []
            for g in soup.find_all("div", class_="BVG0Nb"):
                link = g.a["href"]
                title = g.get_text()
                results.append(f"Title: {title}\nURL: {link}\n")

            return "\n".join(results) if results else "No results found"
        except Exception as e:
            return self.handle_error(e)

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    searcher = WebSearchPlugin()
    return searcher.run(*args, **kwargs)
