import os
import sys
import platform
import requests
from utils.logger import get_logger

logger = get_logger("music_player")

class MusicPlayerPlugin:
    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args:
            return "Available commands: play <file>, stop, releases"
            
        command = args[0].lower()
        if command == "play" and len(args) > 1:
            return self.play_music(" ".join(args[1:]))
        elif command == "stop":
            return self.stop_music()
        elif command == "releases":
            return self.get_new_releases()
        else:
            return f"Unknown command: {command}"

    def play_music(self, music_file):
        """Play music file with platform-specific commands"""
        if not os.path.exists(music_file):
            logger.error(f"Music file not found: {music_file}")
            return f"Error: File '{music_file}' not found"
            
        system = platform.system()
        try:
            if system == "Windows":
                os.system(f'start "" "{music_file}"')
            elif system == "Darwin":  # macOS
                os.system(f'open "{music_file}"')
            else:  # Linux and others
                os.system(f'xdg-open "{music_file}"')
                
            logger.info(f"Playing music: {music_file}")
            return f"Playing music: {music_file}"
        except Exception as e:
            logger.error(f"Failed to play music: {str(e)}")
            return f"Error playing music: {str(e)}"

    def get_new_releases(self):
        """Get new music releases from Spotify API"""
        try:
            config = load_config()
            token = config.get("spotify_token")
            if not token or token == "YOUR_SPOTIFY_TOKEN":
                return "Spotify API not configured. Set 'spotify_token' in config.json for new releases."
            response = requests.get(
                "https://api.spotify.com/v1/browse/new-releases",
                headers={"Authorization": f"Bearer {token}"}
            )
            releases = response.json().get("albums", {}).get("items", [])
            logger.info(f"Fetched {len(releases)} new releases")
            return "\n".join([f"🎵 {release['name']}" for release in releases]) or "No new releases found"
        except Exception as e:
            logger.error(f"Failed to fetch new releases: {str(e)}")
            return "Failed to fetch new releases"

    def stop_music(self):
        """Stop music playback with platform-specific commands"""
        system = platform.system()
        try:
            if system == "Windows":
                os.system("taskkill /f /im Music.UI.exe")  # Windows Media Player
            elif system == "Darwin":  # macOS
                os.system("osascript -e 'tell application \"Music\" to stop'")
            else:  # Linux
                os.system("pkill vlc")  # Common Linux player
            
            logger.info("Stopped music playback")
            return "Music stopped."
        except Exception as e:
            logger.error(f"Failed to stop music: {str(e)}")
            return "Error stopping music"

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    player = MusicPlayerPlugin()
    return player.run(*args, **kwargs)
