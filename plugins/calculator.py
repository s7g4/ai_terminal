from core.plugin_template import BasePlugin
import requests
import urllib.parse
import re

class CalculatorPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.mathjs_url = "https://api.mathjs.org/v4/"

    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args:
            return "Please provide a calculation (e.g. 'calculate 2+2')"
        
        # Parse voice command
        intent, expression = self.parse_voice_command(" ".join(args))
        
        try:
            result = self.calculate_with_mathjs(expression)
            return f"Result: {result}"
        except Exception as e:
            return self.handle_error(e)

    def calculate_with_mathjs(self, expression):
        # Clean expression first
        clean_expr = re.sub(r'[^0-9+\-*/().]', '', expression)
        encoded_expr = urllib.parse.quote(clean_expr)
        url = f"{self.mathjs_url}?expr={encoded_expr}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception("Failed to get a valid response from math.js API")

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    calculator = CalculatorPlugin()
    return calculator.run(*args, **kwargs)
