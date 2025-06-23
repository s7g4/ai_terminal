import openai
import requests
from core.memory import MemoryManager
from utils.config_loader import load_config
config = load_config()

class AIAgent:
    def __init__(self):
        self.api_key = config.get("llm", {}).get("api_keys", {}).get("openai")
        self.model = config.get("llm", {}).get("model", "gpt-4")
        self.memory = MemoryManager()

    def query(self, prompt, context=None):
        if not self.api_key:
            return "OpenAI API key missing."

        headers = {"Authorization": f"Bearer {self.api_key}"}
        messages = [{"role": "system", "content": "You are a helpful assistant."}]

        if context:
            messages.append({"role": "user", "content": context})
        messages.append({"role": "user", "content": prompt})

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=messages
            )
            reply = response.choices[0].message.content.strip()
            try:
                self.memory.update_context(prompt, reply)
            except Exception as e:
                logger.error(f"Failed to update memory: {e}")
            return reply
        except Exception as e:
            return f"Error with OpenAI API: {e}"

    def internet_search_fallback(self, prompt):
        try:
            search_url = f"https://api.duckduckgo.com/?q={prompt}&format=json"
            res = requests.get(search_url)
            res_json = res.json()
            return res_json.get("AbstractText") or res_json.get("RelatedTopics", [{}])[0].get("Text") or "No good result found."
        except:
            return "Internet search failed."

    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args:
            return "Please provide a query for the AI agent."
        return self.query(args[0])

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    agent = AIAgent()
    return agent.run(*args, **kwargs)
