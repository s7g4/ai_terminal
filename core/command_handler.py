import re
from core.plugin_manager import PluginManager
from core.brain import Brain
from core.memory import Memory
from core.voice import Voice
from core.personality import Personality
from utils.logger import get_logger
logger = get_logger("command_handler")
from utils.config_loader import load_config

class CommandHandler:
    def __init__(self):
        self.plugins = PluginManager()
        self.brain = Brain()
        self.memory = Memory()
        self.voice = Voice()
        self.personality = Personality()
        self.config = load_config()

        # Load aliases dynamically from config.json
        self.aliases = self.config.get("aliases", {})

    def handle(self, command: str, use_voice=False):
        """Main entry point to process and respond to a command."""
        logger.info(f"Raw input: {command}")
        if not command.strip():
            return "No command provided."

        command = self._preprocess(command)
        logger.info(f"Preprocessed: {command}")
        self.memory.update(command, "")

        subcommands = self._split_tasks(command)
        results = []

        for subcmd in subcommands:
            resolved = self._apply_aliases(subcmd)

            # First try direct plugin match
            plugin_name, plugin_response = self.plugins.smart_dispatch(resolved)
            if plugin_name:
                try:
                    result = self.plugins.execute(plugin_name, resolved)
                    self.memory.update("", result)
                    self.respond(result, use_voice)
                    results.append(result)
                    continue
                except Exception as e:
                    logger.error(f"Plugin '{plugin_name}' failed: {str(e)}")
                    error_msg = f"The {plugin_name} plugin encountered an error. Let me try to help another way..."
                    self.respond(error_msg, use_voice)
                    results.append(error_msg)
                    # Fall through to AI handling

            # Try AI-powered command understanding
            try:
                ai_suggestion = self.brain.respond_to_query(
                    f"Interpret this command and suggest how to execute it: {resolved}\n"
                    "Provide either: 1) A plugin name that can handle it, or "
                    "2) Direct instructions/code to execute it."
                )
                logger.info(f"AI command interpretation: {ai_suggestion}")

                # Try to match the AI's suggestion to a plugin
                plugin_name, plugin_response = self.plugins.smart_dispatch(ai_suggestion)
                if plugin_name:
                    try:
                        result = self.plugins.execute(plugin_name, ai_suggestion)
                        self.memory.update("", result)
                        self.respond(result, use_voice)
                        results.append(result)
                        continue
                    except Exception as e:
                        logger.error(f"AI-suggested plugin '{plugin_name}' failed: {str(e)}")
                        error_msg = f"The AI-suggested plugin '{plugin_name}' encountered an error."
                        self.respond(error_msg, use_voice)
                        results.append(error_msg)
                        continue
            except Exception as e:
                logger.error(f"AI command interpretation failed: {str(e)}")

            # Final AI fallback - direct execution
            logger.debug(f"Attempting direct AI execution for: {resolved}")
            try:
                ai_response = self.brain.respond_to_query(
                    f"Provide direct executable solution for: {resolved}\n"
                    "Format as either:\n"
                    "1) A bash command between ```bash ``` marks\n"
                    "2) Python code between ```python ``` marks\n"
                    "3) Plain instructions if neither is possible"
                )

                # Try to execute the AI's suggestion
                try:
                    if "```" in ai_response:  # Extract code blocks
                        code_blocks = re.findall(r'```(?:python|bash)?\n(.*?)\n```', ai_response, re.DOTALL)
                        for block in code_blocks:
                            self.execute_code_block(block)
                            results.append(f"Executed: {block[:50]}...")
                    else:
                        self.respond(ai_response, use_voice)
                        results.append(ai_response)
                except Exception as e:
                    error_msg = f"Failed to execute: {str(e)}"
                    self.respond(error_msg, use_voice)
                    results.append(error_msg)
                
                self.memory.update("", "\n".join(results))

            except Exception as e:
                logger.error(f"AI direct execution failed: {str(e)}")
                error_msg = "I encountered an error while trying to process your request."
                self.respond(error_msg, use_voice)
                results.append(error_msg)
                continue

        return "\n".join(results)

    def respond(self, response, use_voice=False):
        """Speak or print the response."""
        if use_voice:
            self.voice.say(response)
        else:
            print(self.personality.format_response(response))

    def help(self):
        """Returns help text for all available plugins."""
        help_texts = []
        for plugin_name in self.plugins.list_plugins():
            help_texts.append(f"\n[{plugin_name}]\n{self.plugins.get_plugin_help(plugin_name)}")
        return "\n".join(help_texts)

    # ──────────────────────────────
    # Internal Helpers
    # ──────────────────────────────

    def _preprocess(self, command):
        """Normalize and sanitize command string."""
        command = command.lower().strip()
        command = re.sub(r"[^\w\s\-\.\/]", "", command)  # remove symbols
        command = self._filter_profanity(command)
        return command

    def _split_tasks(self, command):
        """Split tasks by conjunctions (and, then)."""
        return [task.strip() for task in re.split(r"\b(?:and|then|&|,)\b", command)]

    def _apply_aliases(self, command):
        """Replace command with alias if it exists in config."""
        return self.aliases.get(command, command)

    def _filter_profanity(self, command):
        """Censor known bad words (optional)."""
        blacklist = {"damn", "hell", "crap"}
        return " ".join("[censored]" if word in blacklist else word for word in command.split())

    def execute_code_block(self, code):
        """Execute a code block from AI response."""
        # Simple implementation - could be enhanced with sandboxing
        if code.strip().startswith("python"):
            exec(code[6:].strip(), globals())
        elif code.strip().startswith("bash"):
            os.system(code[4:].strip())
        else:
            # Default to trying as Python
            try:
                exec(code, globals())
            except:
                # Fallback to shell if Python fails
                os.system(code)
