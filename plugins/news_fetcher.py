import requests
from utils.config_loader import load_config
config = load_config()

class NewsReaderPlugin:
    def __init__(self):
        self.api_key = config.get("news_api_key", "YOUR_NEWS_API_KEY")
        self.base_url = "https://newsapi.org/v2/top-headlines"

    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        country = args[0] if args else "us"
        return self.get_news(country)

    def get_news(self, country="us"):
        if self.api_key == "YOUR_NEWS_API_KEY":
            return "News API key not configured. Please set 'news_api_key' in config.json"

        params = {
            'country': country,
            'apiKey': self.api_key
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])
                if articles:
                    headlines = [f"{i+1}. {article['title']}" for i, article in enumerate(articles[:10])]
                    return "\n".join(headlines)
                else:
                    return "No news articles found."
            else:
                return f"Failed to fetch news: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"Error fetching news: {str(e)}"

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    news_reader = NewsReaderPlugin()
    return news_reader.run(*args, **kwargs)
