import pyttsx3
import speech_recognition as sr
import os
import random
import time
from .memory import MemoryManager
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Voice:
    def __init__(self):
        try:
            # Use espeak driver for better PipeWire compatibility on Linux
            self.engine = pyttsx3.init(driverName='espeak')
        except Exception as e:
            print(f"Error initializing pyttsx3 engine with espeak: {e}")
            logger.error(f"Error initializing pyttsx3 engine with espeak: {e}")
            try:
                # Fallback to default driver
                self.engine = pyttsx3.init()
            except Exception as e2:
                print(f"Error initializing pyttsx3 engine: {e2}")
                logger.error(f"Error initializing pyttsx3 engine: {e2}")
                self.engine = None

        # Handle Python 3.14 SpeechRecognition compatibility (aifc import issue)
        try:
            self.recognizer = sr.Recognizer()
        except ImportError as e:
            print(f"SpeechRecognition unavailable due to Python 3.14 compatibility: {e}")
            logger.error(f"SpeechRecognition unavailable: {e}")
            self.recognizer = None

        self.mood = "neutral"  # Can be "neutral", "happy", "sad", "angry"
        self.memory = MemoryManager()
        self.load_device_index()  # Load saved device index
        if self.engine:
            self.setup_tts()

    def load_device_index(self):
        """Load saved audio device index from memory"""
        prefs = self.memory._load().get('preferences', {})
        device_index = prefs.get('audio_device_index', 0)
        try:
            # Get available voices and set the selected one
            voices = self.engine.getProperty('voices')
            if 0 <= device_index < len(voices):
                self.engine.setProperty('voice', voices[device_index].id)
            else:
                print(f"Warning: Invalid audio device index {device_index}")
        except Exception as e:
            print(f"Warning: Could not set audio device: {e}")

    def setup_tts(self):
        """Setup TTS engine preferences"""
        try:
            voices = self.engine.getProperty('voices')
            if voices:
                self.engine.setProperty('voice', voices[1].id)  # Using the second voice (female by default)
            self.engine.setProperty('rate', 150)  # Speed of speech
            self.engine.setProperty('volume', 1)  # Volume level
        except Exception as e:
            print(f"Warning: Could not setup TTS preferences: {e}")

    def change_mood(self, mood: str):
        """Change the voice's mood based on emotional context"""
        self.mood = mood
        if not self.engine:
            return
        if mood == "happy":
            self.engine.setProperty('rate', 180)
            self.engine.setProperty('volume', 1)
        elif mood == "sad":
            self.engine.setProperty('rate', 120)
            self.engine.setProperty('volume', 0.8)
        elif mood == "angry":
            self.engine.setProperty('rate', 160)
            self.engine.setProperty('volume', 1)
        else:
            self.setup_tts()  # reset to neutral settings

    def speak(self, text: str):
        """Convert text to speech with the current mood tone"""
        print(f"Jarvis/Friday: {text}")
        if self.engine:
            self.engine.say(text)
            self.engine.runAndWait()

    def listen(self):
        """Listen to the user's speech and return the command"""
        try:
            mic_list = sr.Microphone.list_microphone_names()
            if not mic_list:
                raise OSError("No audio input devices found")
            device_index = 0  # Default to the first device
            with sr.Microphone(device_index=device_index) as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                print("Listening...")
                audio = self.recognizer.listen(source)
                return self.recognizer.recognize_google(audio).lower()
        except Exception as e:
            print(f"Error during listening: {e}")
            return None

    def save_audio(self, text: str, filename="output_audio.wav"):
        """Save the spoken text as an audio file"""
        print(f"Saving audio as {filename}...")
        if self.engine:
            temp_file = "temp_audio.mp3"
            self.engine.save_to_file(text, temp_file)
            time.sleep(1)
            os.rename(temp_file, filename)
            print(f"Audio saved to {filename}")

    def play_audio(self, filename="output_audio.wav", device=None):
        """Play a previously saved audio file with optional device"""
        logger.debug(f"Attempting to play audio file: {filename} on device: {device}")
        try:
            if device:
                ret = os.system(f"paplay --device={device} {filename} || aplay -D {device} {filename}")
            else:
                ret = os.system(f"paplay {filename} || aplay {filename}")
            if ret != 0:
                logger.warning("Audio playback failed. Please check your audio configuration.")
        except Exception as e:
            logger.error(f"Error playing audio file: {e}")

    def validate_audio_device(self, device_name):
        """Validate if the given audio device exists"""
        devices = sr.Microphone.list_microphone_names()
        if device_name not in devices:
            print(f"Error: Audio device '{device_name}' not found.")
            return False
        return True

    def random_greeting(self):
        """Generate a random greeting based on the time of day"""
        greetings = [
            "Good morning, how can I assist you today?",
            "Good afternoon, how may I help you?",
            "Good evening, how are you today?",
            "Hello, what can I do for you?",
        ]
        self.speak(random.choice(greetings))

    def adjust_voice_tone(self, text: str):
        """Adjust the tone of the voice depending on context"""
        if "angry" in text:
            self.change_mood("angry")
        elif "happy" in text:
            self.change_mood("happy")
        elif "sad" in text:
            self.change_mood("sad")
        else:
            self.change_mood("neutral")

    def farewell(self):
        """Say farewell and end the session"""
        self.speak("Goodbye, take care!")
        if self.engine:
            self.engine.stop()
