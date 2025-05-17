import os
from utils.logger import get_logger
logger = get_logger("brain")
from utils.config_loader import load_config
from core.memory import update_memory

# Load config
config = load_config()
USE_MODEL = config.get("use_model", "openai")

# Initialize based on provider
if USE_MODEL == "claude":
    import anthropic
    anthropic_client = anthropic.Anthropic(api_key=config.get("anthropic_api_key", os.getenv("ANTHROPIC_API_KEY")))
else:
    import openai
    openai.api_key = config.get("openai_api_key", os.getenv("OPENAI_API_KEY"))

BASE_SYSTEM_PROMPT = (
    "You are JARVIS, a smart AI terminal assistant with a touch of personality. "
    "You understand commands, tasks, jokes, coding, system control, and productivity help. "
    "Respond creatively and efficiently."
)

class Brain:
    def __init__(self):
        self.config = load_config()
        self.USE_MODEL = self.config.get("use_model", "openai")
        
        if self.USE_MODEL == "claude":
            import anthropic
            self.client = anthropic.Anthropic(api_key=self.config.get("anthropic_api_key", os.getenv("ANTHROPIC_API_KEY")))
        else:
            import openai
            openai.api_key = self.config.get("openai_api_key", os.getenv("OPENAI_API_KEY"))
            self.client = openai

        self.BASE_SYSTEM_PROMPT = (
            "You are JARVIS, a smart AI terminal assistant with a touch of personality. "
            "You understand commands, tasks, jokes, coding, system control, and productivity help. "
            "Respond creatively and efficiently."
        )

    def respond_to_query(self, query, memory=None):
        try:
            # Add memory context
            user_history = []
            if memory:
                context = memory.get("context", [])
                for past in context[-3:]:
                    user_history.append({"role": "user", "content": past.get("user")})
                    user_history.append({"role": "assistant", "content": past.get("ai")})

            # Claude 3.5 Sonnet
            if self.USE_MODEL == "claude":
                response = self.client.messages.create(
                    model="claude-3-sonnet-20240229",
                    max_tokens=1024,
                    temperature=0.7,
                    system=self.BASE_SYSTEM_PROMPT,
                    messages=user_history + [{"role": "user", "content": query}]
                )
                reply = response.content[0].text

            # OpenAI GPT
            else:
                messages = [{"role": "system", "content": self.BASE_SYSTEM_PROMPT}]
                messages += user_history
                messages.append({"role": "user", "content": query})

                response = self.client.Completion.create(
                    engine=self.config.get("llm_model", "gpt-3.5-turbo"),
                    prompt=messages,
                    temperature=0.7,
                    max_tokens=150
                )
                reply = response["choices"][0]["text"].strip()

            # Update memory
            if memory is not None:
                update_memory(memory, query, reply)

            # Cache last response to reduce repeated calls (simple in-memory cache)
            self._last_query = query
            self._last_reply = reply

            return reply

        except Exception as e:
            logger.error(f"Error: {e}")
            return "⚠️ My mind is offline at the moment. Try again later."
