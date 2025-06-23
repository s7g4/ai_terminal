from core.plugin_template import BasePlugin
from core.memory import MemoryManager
import os
import sys
import requests
import subprocess
import sounddevice as sd
import json

class SystemControlPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.app_commands = {
            'spotify': 'spotify',
            'chrome': 'google-chrome',
            'calculator': 'gnome-calculator',
            'files': 'nautilus'
        }
        self.memory = MemoryManager()

    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args:
            return "Available commands: shutdown, reboot, status, or open [app]"
        
        # Parse voice command
        intent, command = self.parse_voice_command(" ".join(args))
        command = command.lower()

        # Handle app opening - more flexible matching
        if any(cmd in command for cmd in ['open', 'start', 'launch']):
            app_name = command.replace('open', '').replace('start', '').replace('launch', '').strip()
            return self.open_application(app_name)
        
        # Handle system commands
        if command == "shutdown":
            return self.shutdown()
        elif command == "reboot":
            return self.reboot()
        elif command in ["status", "info"]:
            return self.system_status()
        elif "audio device" in command or "sound device" in command:
            return self.handle_audio_device(command)
        else:
            return f"Unknown command: {command}"

    def open_application(self, app_name):
        if app_name in self.app_commands:
            try:
                subprocess.Popen([self.app_commands[app_name]])
                return f"Opening {app_name}"
            except Exception as e:
                return self.handle_error(e)
        return f"Application '{app_name}' not configured"

    def shutdown(self):
        os.system("shutdown /s /f /t 0")  # Windows
        return "System shutting down..."

    def reboot(self):
        os.system("reboot")
        return "System rebooting..."

    def system_status(self):
        try:
            response = requests.get("http://localhost:8080/system/status")
            if response.status_code == 200:
                status = response.json().get("status", "System status is normal.")
                # Add audio device info to status
                devices = sd.query_devices()
                current_device = self.memory.load().get("preferences", {}).get("audio_device_index", 0)
                status += f"\nAudio devices: {len(devices)} available (Current: {current_device})"
                return status
            return "Unable to fetch system status."
        except Exception as e:
            return self.handle_error(e)

    def handle_audio_device(self, command):
        """Handle audio device related commands"""
        try:
            devices = sd.query_devices()
            current_index = self.memory.load()["preferences"]["audio_device_index"]
            
            if "list" in command:
                device_list = "\n".join(
                    f"{i}: {d['name']} ({d['max_input_channels']} in, {d['max_output_channels']} out)"
                    f"{' [CURRENT]' if i == current_index else ''}"
                    for i, d in enumerate(devices)
                )
                return f"Available audio devices:\n{device_list}"
            
            elif "set" in command or "change" in command:
                # Extract device number from command
                parts = command.split()
                for part in parts:
                    if part.isdigit():
                        device_index = int(part)
                        if 0 <= device_index < len(devices):
                            # Update memory
                            memory = self.memory.load()
                            memory["preferences"]["audio_device_index"] = device_index
                            self.memory.save(memory)
                            return f"Audio device changed to {device_index}: {devices[device_index]['name']}"
                        return f"Invalid device index. Use numbers between 0-{len(devices)-1}"
                return "Please specify a device number to switch to"
            
            return "Available audio commands: list devices, set device [number]"
            
        except Exception as e:
            return self.handle_error(e)

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    controller = SystemControlPlugin()
    return controller.run(*args, **kwargs)
