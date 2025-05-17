import os
import sys
import signal
import traceback

# Suppress ALSA/JACK warnings
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['ALSA_CONFIG_PATH'] = '/dev/null'

from core.voice import Voice
from core.brain import Brain
from core.memory import load_memory, save_memory
from core.personality import get_personality_response
from core.command_handler import CommandHandler
from core.plugin_manager import PluginManager
from utils.logger import get_logger
logger = get_logger("main")
from utils.config_loader import load_config

# Global Variables
memory = load_memory()
config = load_config()
plugins = PluginManager()

# Boot message
def print_intro():
    intro_file = os.path.join("assets", "intro.txt")
    if os.path.exists(intro_file):
        with open(intro_file, "r") as f:
            print(f.read())

# Signal handler to safely exit
def signal_handler(sig, frame):
    print("\n[!] Exiting JARVIS gracefully...")
    try:
        save_memory(memory)
    except Exception as e:
        print(f"[ERROR] Failed to save memory: {e}")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def check_environment():
    """Verify we're running in the correct virtual environment"""
    if not os.environ.get("VIRTUAL_ENV"):
        print("\n[ERROR] Please activate the virtual environment first:")
        print(f"  source {os.path.dirname(os.path.abspath(__file__))}/jarvis_env/bin/activate")
        print("Then run the application again.\n")
        sys.exit(1)

def main():
    check_environment()
    print_intro()
    voice = Voice()
    brain = Brain()
    command_handler = CommandHandler()
    voice.speak("Hello, I am JARVIS. Ready for your command.")

    try:
        while True:
            try:
                user_input = voice.listen()

                if not user_input:
                    continue

                logger.info(f"User: {user_input}")

                # Step 1: Personality layer (mood-aware response)
                persona_response = get_personality_response(user_input)
                if persona_response:
                    voice.speak(persona_response)

                # Step 2: Plugin matching
                plugin_response = plugins.smart_dispatch(user_input)[1]
                if plugin_response:
                    voice.speak(plugin_response)
                    continue

                # Step 3: Hardcoded command handler (if plugin didn't match)
                command_response = command_handler.handle(user_input)
                if command_response:
                    voice.speak(command_response)
                    continue

                # Step 4: General AI brain response
                ai_response = brain.respond_to_query(user_input, memory)
                voice.speak(ai_response)

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                logger.error(error_msg)
                voice.speak("Something went wrong.")
                traceback.print_exc()
    except KeyboardInterrupt:
        print("\n[!] Keyboard interrupt received. Exiting gracefully...")
        try:
            save_memory(memory)
        except Exception as e:
            print(f"[ERROR] Failed to save memory: {e}")
        sys.exit(0)

if __name__ == "__main__":
    main()
