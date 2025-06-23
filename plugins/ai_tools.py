from core.plugin_template import BasePlugin
import requests
from utils.logger import get_logger

logger = get_logger("ai_tools")

class AIToolsPlugin(BasePlugin):
    def __init__(self):
        super().__init__()

    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if args and args[0].lower() == "search":
            query = " ".join(args[1:]) if len(args) > 1 else ""
            return self.search_ai_tools(query)
        return "\n".join(self.list_ai_tools())

    def list_ai_tools(self):
        try:
            url = "https://huggingface.co/api/spaces?sort=likes"
            response = requests.get(url)
            response.raise_for_status()
            tools = response.json()
            logger.info(f"Fetched {len(tools)} AI tools")
            return [f"🔧 {tool['id']} - {tool['likes']} likes" for tool in tools[:10]]
        except Exception as e:
            logger.error(f"Failed to fetch tools: {e}")
            return [self.handle_error(e)]

    def search_ai_tools(self, query):
        try:
            url = f"https://huggingface.co/api/spaces?search={query}"
            response = requests.get(url)
            response.raise_for_status()
            tools = response.json()
            if not tools:
                return f"No AI tools found for: {query}"
            return "\n".join([f"🔍 {tool['id']}" for tool in tools[:5]])
        except Exception as e:
            return self.handle_error(e)

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    ai_tools = AIToolsPlugin()
    return ai_tools.run(*args, **kwargs)
