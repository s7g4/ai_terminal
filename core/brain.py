import os
import ollama
import openai
import anthropic
from utils.logger import get_logger
logger = get_logger("brain")
import utils.config_loader
from core.memory import update_memory

BASE_SYSTEM_PROMPT = (
    "You are JARVIS, a smart AI terminal assistant with a touch of personality. "
    "You understand commands, tasks, jokes, coding, system control, and productivity help. "
    "Respond creatively and efficiently. "
    "You have access to various plugins for specific tasks. When a user query requires a plugin, respond with 'PLUGIN: <plugin_name> <args>' where <plugin_name> is the exact plugin name and <args> are the arguments. "
    "Available plugins: ai_agent, ai_tools, calculator, currency_converter, email_manager, file_manager, git_helper, joke_teller, movie_recommender, music_player, news_fetcher, notes, reminder, system_control, task_scheduler, todo_list, weather, web_search. "
    "For example, for a reminder: 'PLUGIN: reminder set my message 10'. "
    "If no plugin is needed, respond normally."
)

class Brain:
    def __init__(self):
        self.config = utils.config_loader.load_config()
        self.USE_MODEL = self.config.get("use_model", "ollama")
        self.model = self.config.get("ollama_model", "llama3.2")

        if self.USE_MODEL == "claude":
            self.client = anthropic.Anthropic(api_key=self.config.get("anthropic_api_key", os.getenv("ANTHROPIC_API_KEY")))
        elif self.USE_MODEL == "openai":
            self.client = openai.OpenAI(api_key=self.config.get("openai_api_key", os.getenv("OPENAI_API_KEY")))
        # For Ollama, no client init needed

        self.BASE_SYSTEM_PROMPT = BASE_SYSTEM_PROMPT

    def respond_to_query(self, query, memory=None):
        try:
            # Check for plugin invocation
            if query.startswith("PLUGIN:"):
                return query

            # Add memory context
            user_history = []
            if memory:
                context = memory.get("context", [])
                for past in context[-3:]:
                    user_history.append({"role": "user", "content": past.get("user")})
                    user_history.append({"role": "assistant", "content": past.get("ai")})

            # Ollama
            if self.USE_MODEL == "ollama":
                messages = [{"role": "system", "content": self.BASE_SYSTEM_PROMPT}]
                messages += user_history
                messages.append({"role": "user", "content": query})
                
                response = ollama.chat(
                    model=self.model,
                    messages=messages,
                    options={
                        "temperature": 0.7,
                        "num_predict": 150
                    }
                )
                reply = response['message']['content']

            # Claude 3.5 Sonnet
            elif self.USE_MODEL == "claude":
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1024,
                    temperature=0.7,
                    system=self.BASE_SYSTEM_PROMPT,
                    messages=user_history + [{"role": "user", "content": query}]
                )
                reply = response.content[0].text

            # OpenAI GPT (updated to modern API)
            else:
                messages = [{"role": "system", "content": self.BASE_SYSTEM_PROMPT}]
                messages += user_history
                messages.append({"role": "user", "content": query})

                response = self.client.chat.completions.create(
                    model=self.config.get("llm_model", "gpt-3.5-turbo"),
                    messages=messages,
                    temperature=0.7,
                    max_tokens=150
                )
                reply = response.choices[0].message.content.strip()

            # Update memory
            if memory is not None:
                update_memory(memory, query, reply)

            # Cache last response to reduce repeated calls (simple in-memory cache)
            self._last_query = query
            self._last_reply = reply

            return reply

        except Exception as e:
            logger.error(f"Error: {e}")
            return "My mind is offline at the moment. Try again later."
