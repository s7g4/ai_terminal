import requests
import random
from utils.config_loader import load_config
from utils.logger import get_logger

logger = get_logger("movie_recommender")

class MovieRecommenderPlugin:
    def __init__(self):
        config = load_config()
        self.api_key = config.get("tmdb_api_key", "d67af61c17c439b10daaf2eb5bb1f745")
        self.base_url = "https://api.themoviedb.org/3"

    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        genre = args[0] if args else "action"
        return self.get_movie_recommendation(genre)

    def get_movie_recommendation(self, genre="action"):
        try:
            search_url = f"{self.base_url}/search/movie"
            params = {
                "api_key": self.api_key,
                "query": genre,
                "language": "en-US",
                "include_adult": False
            }
            response = requests.get(search_url, params=params)
            data = response.json()

            if data.get("results"):
                movie = random.choice(data["results"])
                title = movie.get("title", "Unknown Title")
                year = movie.get("release_date", "N/A")[:4]
                logger.info(f"Recommended movie: {title}")
                return f"🎬 Movie Recommendation: {title} ({year})"

            logger.warning(f"No movies found for genre: {genre}")
            return "No movies found. Try a different genre."

        except Exception as e:
            logger.error(f"Failed to fetch movie: {e}")
            return f"Failed to fetch movie: {e}"

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    recommender = MovieRecommenderPlugin()
    return recommender.run(*args, **kwargs)
