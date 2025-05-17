import requests

class JokeTellerPlugin:
    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        return self.tell_joke()

    def tell_joke(self):
        url = "https://v2.jokeapi.dev/joke/Any?type=single"
        response = requests.get(url)
        joke_data = response.json()
        if joke_data['error']:
            return "Couldn't fetch a joke right now."
        return joke_data["joke"]

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    teller = JokeTellerPlugin()
    return teller.run(*args, **kwargs)
