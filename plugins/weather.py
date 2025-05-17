import requests
from utils.config_loader import load_config
config = load_config()

class WeatherPlugin:
    def __init__(self):
        self.api_key = config.get("api_keys", {}).get("weather")
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"

    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args:
            return "Please provide a city name (e.g. 'weather London')"
        
        # Extract city name from natural language queries
        query = " ".join(args).lower()
        
        # Common weather query patterns
        patterns = [
            "weather in ",
            "weather at ",
            "weather for ",
            "how is the weather in ",
            "what's the weather in ",
            "temperature in "
        ]
        
        # Try to extract city name from patterns
        city_name = query
        for pattern in patterns:
            if pattern in query:
                city_name = query.split(pattern)[-1].strip()
                break
                
        # Remove question marks and other punctuation
        city_name = city_name.split("?")[0].strip()
        
        return self.get_weather(city_name)

    def get_weather(self, city_name):
        if not self.api_key:
            return "Weather API key not configured. Please set weather_api_key in config.json"

        complete_url = f"{self.base_url}q={city_name}&appid={self.api_key}&units=metric"
        
        try:
            response = requests.get(complete_url)
            response.raise_for_status()
            data = response.json()

            if not isinstance(data, dict):
                return "Invalid weather data received"

            if data.get("cod") == "404":
                return f"City {city_name} not found."

            if "main" not in data or "weather" not in data:
                return "Unexpected weather data format received"

            main_data = data["main"]
            weather_data = data["weather"][0]

            temperature = main_data.get("temp", "unknown")
            weather_description = weather_data.get("description", "unknown conditions")
            return f"The temperature in {city_name} is {temperature}°C with {weather_description}."

        except requests.exceptions.RequestException as e:
            return f"Failed to fetch weather data: {str(e)}"
        except (KeyError, IndexError) as e:
            return "Unexpected weather data format received"
        except Exception as e:
            return f"An error occurred: {str(e)}"

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    weather = WeatherPlugin()
    return weather.run(*args, **kwargs)
