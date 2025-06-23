from core.plugin_template import BasePlugin
import requests

class CurrencyConverterPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.validate_config(['api_keys.currency'])

    def run(self, *args, **kwargs):
        """Main execution method for the plugin"""
        if not args:
            return "Usage: convert <from> <to> <amount> (e.g. 'convert USD EUR 100')"
        
        # Parse voice command
        intent, query = self.parse_voice_command(" ".join(args))
        parts = query.split()
        
        if len(parts) != 3:
            return "Please specify: from_currency, to_currency, and amount"
            
        from_currency, to_currency, amount = parts
        try:
            amount = float(amount)
            return self.convert_currency(from_currency.upper(), to_currency.upper(), amount)
        except ValueError:
            return self.handle_error("Amount must be a number")

    def convert_currency(self, from_currency, to_currency, amount):
        try:
            url = f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
            headers = {"Authorization": f"Bearer {self.config['api_keys']['currency']}"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            rate = response.json()['rates'].get(to_currency)
            if rate:
                return f"{amount} {from_currency} = {amount * rate:.2f} {to_currency}"
            return f"Conversion rate for {to_currency} not found."
        except Exception as e:
            return self.handle_error(e)

# Module-level run function required by plugin manager
def run(*args, **kwargs):
    converter = CurrencyConverterPlugin()
    return converter.run(*args, **kwargs)
