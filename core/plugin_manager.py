import importlib
import os
import sys
import traceback
from utils.logger import get_logger
logger = get_logger("plugin_manager")

PLUGINS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "plugins")

class PluginManager:
    def __init__(self):
        self.plugins = {}
        self.load_plugins()

    def load_plugins(self):
        """Dynamically load all plugins from the plugins directory"""
        # Add plugins directory to Python path temporarily
        original_sys_path = sys.path.copy()
        try:
            sys.path.insert(0, os.path.dirname(PLUGINS_DIR))
            
            if not os.path.exists(PLUGINS_DIR):
                logger.error(f"Plugins directory not found: {PLUGINS_DIR}")
                return
            
            for filename in os.listdir(PLUGINS_DIR):
                if filename.endswith(".py") and not filename.startswith("__"):
                    plugin_name = filename[:-3]
                    try:
                        module = importlib.import_module(f"plugins.{plugin_name}")
                        if hasattr(module, "run"):
                            self.plugins[plugin_name] = module
                            logger.info(f"Loaded '{plugin_name}'")
                        else:
                            logger.warning(f"'{plugin_name}' does not have a run() method")
                    except Exception as e:
                        logger.error(f"Failed to load '{plugin_name}': {e}")
                        traceback.print_exc()
        finally:
            # Restore original sys.path
            sys.path = original_sys_path

    def list_plugins(self):
        """Return a list of available plugins"""
        return list(self.plugins.keys())

    def execute(self, plugin_name, command):
        """Run the plugin's main method with a command"""
        plugin = self.plugins.get(plugin_name)
        if not plugin:
            return f"Plugin '{plugin_name}' not found."
        try:
            return plugin.run(command)
        except Exception as e:
            logger.error(f"Error running plugin '{plugin_name}': {e}")
            traceback.print_exc()
            return f"Error: {e}"

    def get_plugin_help(self, plugin_name):
        """Return help text if available in the plugin"""
        plugin = self.plugins.get(plugin_name)
        if plugin and hasattr(plugin, "help"):
            return plugin.help()
        return f"No help available for '{plugin_name}'."

    def smart_dispatch(self, command):
        """
        Try to infer the correct plugin based on keywords in command.
        Returns (plugin_name, response) or fallback message.
        """
        keywords = {
            "weather": "weather",
            "temperature": "weather",
            "forecast": "weather",
            "git": "git_helper",
            "commit": "git_helper",
            "clone": "git_helper",
            "push": "git_helper",
            "pull": "git_helper",
            "search": "web_search",
            "google": "web_search",
            "info": "web_search",
            "system": "system_control",
            "shutdown": "system_control",
            "restart": "system_control",
            "cpu": "system_control",
            "ram": "system_control",
            "kill": "system_control",
            "tasks": "system_control",
            "music": "music_player",
            "play": "music_player", 
            "pause": "music_player",
            "spotify": "system_control",
            "open": "system_control",
            "reminder": "reminder",
            "note": "reminder",
            "todo": "todo_manager",
            "timer": "timer",
            "convert": "unit_converter",
            "units": "unit_converter",
            "translate": "translator",
            "language": "translator",
            "news": "news_fetcher",
            "joke": "fun_tools",
            "quote": "fun_tools",
            "ip": "network_tools",
            "network": "network_tools",
            "port": "network_tools",
            "process": "process_watcher",
            "monitor": "process_watcher",
            "calendar": "calendar_tools",
            "date": "calendar_tools"
        }

        for keyword, plugin_name in keywords.items():
            if keyword in command.lower():
                return plugin_name, self.execute(plugin_name, command)

        return None, "I couldn't find a plugin for that. Try another command."

