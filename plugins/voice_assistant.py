import pyttsx3
import speech_recognition as sr
from utils.logger import get_logger

logger = get_logger("voice_assistant")

class VoiceAssistantPlugin:
    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args:
            return "Available commands: speak <text>, listen"
        
        command = args[0].lower()
        if command == "speak" and len(args) > 1:
            return self.speak(" ".join(args[1:]))
        elif command == "listen":
            return self.listen()
        else:
            return f"Unknown command: {command}"

    def __init__(self):
        self.engine = pyttsx3.init()
        self.recognizer = sr.Recognizer()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        try:
            # Try with default microphone settings first
            with sr.Microphone() as source:
                print("\n[Audio] Adjusting for ambient noise (2 seconds)...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print("[Audio] Ready - speak now (5 second limit)")
                try:
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=5)
                    command = self.recognizer.recognize_google(audio)
                    print(f"[Success] Recognized: {command}")
                    return command
                except sr.WaitTimeoutError:
                    return "[Timeout] No speech detected. Try typing your command instead."
                except sr.UnknownValueError:
                    return "[Error] Couldn't understand audio. Please speak clearly."
                except sr.RequestError as e:
                    return f"[Network] Speech API error: {str(e)}"
                    
        except OSError as e:
            print(f"\n[Critical] Audio system error: {str(e)}")
            print("Troubleshooting steps:")
            print("1. Check microphone is connected and not muted")
            print("2. Verify audio permissions for this application")
            print("3. Try alternative input method below")
            return "[Audio] Switching to text input - please type your command:"
            
        except Exception as e:
            print(f"\n[System] Unexpected error: {str(e)}")
            return "[Error] Please use text input for now."

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    logger.info(f"Running voice_assistant with args: {args}")
    assistant = VoiceAssistantPlugin()
    result = assistant.run(*args, **kwargs)
    logger.info(f"Voice assistant result: {result}")
    return result
