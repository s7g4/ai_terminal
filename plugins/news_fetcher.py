import requests
from utils.config_loader import load_config
config = load_config()

class NewsReaderPlugin:
    def __init__(self):
        self.default_feed = config.get("news_rss_feed", "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_API_KEY")

    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        feed_url = args[0] if args else self.default_feed
        return self.get_news(feed_url)

    def get_news(self, rss_feed_url):
        response = requests.get(rss_feed_url)
        if response.status_code == 200:
            return "\n".join([entry.title for entry in response.json()['articles']])
        else:
            return "Unable to fetch news."

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    news_reader = NewsReaderPlugin()
    return news_reader.run(*args, **kwargs)
