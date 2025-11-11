import os
import sys
import signal
import traceback
import argparse
import cmd
import subprocess
import threading
import time
try:
    import readline  # For history and autocomplete (Unix/Linux)
except ImportError:
    try:
        import pyreadline3 as readline  # For Windows
    except ImportError:
        readline = None  # Fallback if neither is available

# Suppress ALSA/JACK warnings
os.environ['PYTHONWARNINGS'] = 'ignore'
os.environ['ALSA_CONFIG_PATH'] = '/dev/null'

from core.brain import Brain
from core.memory import load_memory, save_memory
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
        with open(intro_file, "r", encoding="utf-8") as f:
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
    # Check if we're in the virtual environment by looking for the activation script path
    if os.name == 'nt':  # Windows
        venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis_env", "Scripts", "python.exe")
        if not os.path.exists(venv_path):
            print("\n[ERROR] Virtual environment not found. Please ensure jarvis_env is set up correctly.")
            print("Run: python -m venv jarvis_env")
            print("Then: jarvis_env\\Scripts\\pip install -r requirements.txt")
            sys.exit(1)
    else:
        venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jarvis_env", "bin", "python")
        if not os.path.exists(venv_path):
            print("\n[ERROR] Virtual environment not found. Please ensure jarvis_env is set up correctly.")
            print("Run: python -m venv jarvis_env")
            print("Then: jarvis_env/bin/pip install -r requirements.txt")
            sys.exit(1)

class JarvisShell(cmd.Cmd):
    """Custom shell for JARVIS AI Terminal"""
    intro = "Welcome to JARVIS AI Terminal Shell. Type 'help' or '?' for commands.\n"
    prompt = "jarvis> "

    def __init__(self, voice_enabled=False):
        super().__init__()
        self.brain = Brain()
        self.voice_enabled = voice_enabled
        self.voice = None
        self.voice_thread = None
        if voice_enabled:
            try:
                from core.voice import Voice
                self.voice = Voice()
                if self.voice.recognizer is None:
                    print("Voice recognition unavailable.")
                    self.voice_enabled = False
                else:
                    self.voice.speak("Hello, I am JARVIS. Ready for your command.")
                    self.start_voice_thread()
            except ImportError as e:
                print(f"Voice mode unavailable: {e}")
                self.voice_enabled = False

    def start_voice_thread(self):
        """Start background voice listening thread"""
        def voice_listener():
            while True:
                try:
                    user_input = self.voice.listen()
                    if user_input and "jarvis" in user_input.lower():
                        # Remove "jarvis" keyword and process
                        query = user_input.lower().replace("jarvis", "").strip()
                        if query:
                            self.process_query(query, voice=True)
                    time.sleep(0.1)  # Small delay to prevent high CPU usage
                except Exception as e:
                    logger.error(f"Voice listener error: {e}")
                    time.sleep(1)

        self.voice_thread = threading.Thread(target=voice_listener, daemon=True)
        self.voice_thread.start()

    def process_query(self, user_input, voice=False):
        """Process user input through AI brain"""
        logger.info(f"User: {user_input}")

        # Check if it's a shell command (starts with common commands or has shell syntax)
        shell_commands = [
            # File operations
            'ls', 'dir', 'cd', 'pwd', 'mkdir', 'rmdir', 'rm', 'cp', 'copy', 'mv', 'move', 'cat', 'type', 'touch', 'ln', 'wc', 'head', 'tail', 'sort', 'uniq', 'diff', 'patch',
            # Process management
            'ps', 'tasklist', 'kill', 'taskkill', 'pgrep', 'pkill', 'jobs', 'bg', 'fg', 'nohup', 'top', 'htop',
            # System info
            'uname', 'whoami', 'id', 'uptime', 'free', 'vmstat', 'iostat', 'df', 'du', 'w', 'last',
            # Networking
            'ping', 'curl', 'wget', 'ssh', 'scp', 'rsync', 'netstat', 'ifconfig', 'ip', 'nslookup', 'dig',
            # Text processing
            'grep', 'find', 'sed', 'awk', 'cut', 'paste', 'tr', 'xargs', 'tee',
            # Archiving
            'tar', 'gzip', 'gunzip', 'bzip2', 'zip', 'unzip', 'rar', 'unrar',
            # Package managers
            'apt', 'apt-get', 'yum', 'dnf', 'pacman', 'brew', 'snap', 'flatpak', 'pip', 'npm', 'yarn', 'gem', 'cargo',
            # Development
            'git', 'svn', 'hg', 'gcc', 'g++', 'clang', 'make', 'cmake', 'python', 'python3', 'node', 'java', 'javac', 'gradle', 'maven',
            # Utilities
            'echo', 'printf', 'clear', 'cls', 'history', 'alias', 'export', 'set', 'source', 'which', 'whereis', 'locate', 'updatedb', 'chmod', 'chown', 'chgrp', 'sudo', 'su', 'passwd', 'useradd', 'usermod', 'groupadd',
            # Windows specific
            'cmd', 'powershell', 'start', 'shutdown', 'restart', 'net', 'reg', 'schtasks'
        ]
        if user_input.split()[0] in shell_commands or any(char in user_input for char in ['|', '>', '<', '&', ';']):
            # Execute as shell command
            try:
                result = subprocess.run(user_input, shell=True, capture_output=True, text=True, cwd=os.getcwd())
                output = result.stdout + result.stderr
                if output:
                    print(output.strip())
                    if voice and self.voice:
                        self.voice.speak(output.strip()[:200])  # Limit speech length
            except Exception as e:
                error_msg = f"Command error: {e}"
                print(error_msg)
                if voice and self.voice:
                    self.voice.speak(error_msg)
        else:
            # Process as AI query
            ai_response = self.brain.respond_to_query(user_input, memory)

            # Check if AI wants to invoke a plugin
            if ai_response.startswith("PLUGIN:"):
                parts = ai_response.split()
                if len(parts) >= 2:
                    plugin_name = parts[1]
                    plugin_args = parts[2:] if len(parts) > 2 else []
                    plugin_response = plugins.execute(plugin_name, plugin_args)
                    print(f"JARVIS: {plugin_response}")
                    if voice and self.voice:
                        self.voice.speak(plugin_response)
                else:
                    msg = "Invalid plugin command."
                    print(f"JARVIS: {msg}")
                    if voice and self.voice:
                        self.voice.speak(msg)
            else:
                print(f"JARVIS: {ai_response}")
                if voice and self.voice:
                    self.voice.speak(ai_response)

    def default(self, line):
        """Handle default input as AI query"""
        if line.strip():
            self.process_query(line.strip())

    def do_exit(self, arg):
        """Exit the shell"""
        print("JARVIS: Goodbye!")
        if self.voice:
            self.voice.farewell()
        return True

    def do_quit(self, arg):
        """Exit the shell"""
        return self.do_exit(arg)

    def do_cd(self, arg):
        """Change directory"""
        try:
            if arg:
                os.chdir(arg)
            else:
                os.chdir(os.path.expanduser("~"))
            print(f"Changed directory to {os.getcwd()}")
        except Exception as e:
            print(f"Error changing directory: {e}")

    def do_EOF(self, arg):
        """Exit on Ctrl+D"""
        return self.do_exit(arg)

    def completenames(self, text, *ignored):
        """Autocomplete command names"""
        commands = ['exit', 'quit', 'cd'] + [cmd for cmd in dir(self) if cmd.startswith('do_')]
        return [name[3:] for name in commands if name.startswith('do_' + text)]

    def completedefault(self, text, line, begidx, endidx):
        """Autocomplete for AI queries (basic file/dir completion)"""
        if not text:
            return []
        try:
            path = text
            if not os.path.isabs(path):
                path = os.path.join(os.getcwd(), path)
            dirname, basename = os.path.split(path)
            if dirname and not os.path.exists(dirname):
                return []
            items = os.listdir(dirname or '.')
            matches = [item for item in items if item.startswith(basename)]
            if dirname:
                matches = [os.path.join(dirname, m) for m in matches]
            return matches
        except:
            return []

def shell_mode(voice_enabled=False):
    """Run JARVIS in shell mode"""
    shell = JarvisShell(voice_enabled=voice_enabled)
    try:
        shell.cmdloop()
    except KeyboardInterrupt:
        print("\nJARVIS: Goodbye!")
    finally:
        save_memory(memory)

def main():
    parser = argparse.ArgumentParser(description="JARVIS AI Terminal")
    parser.add_argument('--mode', choices=['text', 'voice', 'shell'], default='shell',
                       help='Run mode: shell (default), text, or voice')

    args = parser.parse_args()

    check_environment()
    print_intro()

    if args.mode == 'voice':
        shell_mode(voice_enabled=True)
    elif args.mode == 'text':
        shell_mode(voice_enabled=False)
    else:  # shell mode
        shell_mode(voice_enabled=False)  # Can enable voice in shell if needed

if __name__ == "__main__":
    main()
