import random
import json
from utils.config_loader import load_personality
from utils.logger import get_logger
logger = get_logger("personality")

class Personality:
    def __init__(self):
        self.state = "neutral"
        self.mood = "professional"
        self.voice_tone = "neutral"
        self.identity = "JARVIS"
        self.personalities = load_personality()
        self.voice_engine = "gTTS"  # Set to use gTTS for voice output

    def speak(self, text):
        """Convert text to speech using gTTS."""
        try:
            from gtts import gTTS
            import os
            import tempfile
            import subprocess
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
                temp_path = f.name
            
            # Generate speech
            tts = gTTS(text=text, lang='en')
            tts.save(temp_path)
            
            # Play audio (try multiple players)
            players = ['mpg123', 'mpg321', 'ffplay', 'play']
            for player in players:
                try:
                    subprocess.run([player, temp_path], check=True)
                    break
                except (FileNotFoundError, subprocess.CalledProcessError):
                    continue
            
            # Clean up
            os.unlink(temp_path)
            
        except Exception as e:
            logger.error(f"Failed to speak: {e}")

    def format_response(self, text):
        """Apply mood, tone, and persona to the assistant's reply."""
        style = self.get_current_style()

        if self.mood == "funny":
            text = f"😎 {text} Btw, I crack jokes too."
        elif self.mood == "serious":
            text = f"[In a firm tone]: {text}"
        elif self.mood == "sarcastic":
            text = f"Oh really? Here's what I found: {text}"
        elif self.mood == "friendly":
            text = f"Hey there! 😊 {text}"
        elif self.mood == "military":
            text = f"[Commander voice]: {text}, sir."
        elif self.mood == "sci-fi":
            text = f"[⚙️ AI CORE]: {text}"

        return f"{style}\n{text}"

    def get_current_style(self):
        return f"{self.identity} ({self.mood.capitalize()} | Tone: {self.voice_tone})"

    def update_mood(self, new_mood):
        """Change AI's personality mode."""
        allowed_moods = self.personalities.get("moods", [])
        if new_mood in allowed_moods:
            self.mood = new_mood
            logger.info(f"Mood changed to: {new_mood}")
        else:
            logger.warning(f"Invalid mood: {new_mood}")

    def switch_identity(self, identity):
        """Switch between identities like Jarvis or Friday."""
        allowed_ids = self.personalities.get("identities", [])
        if identity in allowed_ids:
            self.identity = identity
            logger.info(f"Identity switched to: {identity}")
        else:
            logger.warning(f"Invalid identity: {identity}")

    def react_to_emotion(self, sentiment):
        """Change tone based on user sentiment (angry, sad, happy, etc)."""
        tone_map = {
            "angry": "apologetic",
            "sad": "comforting",
            "happy": "cheerful",
            "neutral": "calm"
        }
        self.voice_tone = tone_map.get(sentiment, "calm")
        logger.info(f"Adjusted tone to: {self.voice_tone}")

    def randomize(self):
        """Randomly pick a mood and identity for diversity."""
        self.mood = random.choice(self.personalities.get("moods", ["neutral"]))
        self.identity = random.choice(self.personalities.get("identities", ["JARVIS"]))
        self.voice_tone = random.choice(["calm", "cheerful", "firm", "intense", "witty"])
        logger.info(f"Randomized to {self.identity}, mood: {self.mood}, tone: {self.voice_tone}")

def get_personality_response(user_input):
    """Process user input through personality layer and return formatted response"""
    personality = Personality()
    
    # Simple mood detection from input
    if any(word in user_input.lower() for word in ["happy", "joy", "great"]):
        personality.mood = "happy"
    elif any(word in user_input.lower() for word in ["sad", "upset", "angry"]):
        personality.mood = "sad"
    
    # Format the response with personality
    return personality.format_response(user_input)
