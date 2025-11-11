import unittest
from unittest.mock import patch, MagicMock
from core.brain import Brain

class TestBrain(unittest.TestCase):
    @patch('utils.config_loader.load_config')
    @patch('ollama.chat')
    def test_respond_to_query_ollama(self, mock_chat, mock_load_config):
        mock_load_config.return_value = {"use_model": "ollama", "ollama_model": "llama3.2"}
        mock_chat.return_value = {'message': {'content': 'Ollama response'}}
        brain = Brain()
        response = brain.respond_to_query("Hello", {})
        self.assertEqual(response, "Ollama response")

    @patch('utils.config_loader.load_config')
    @patch('core.brain.openai.OpenAI')
    def test_respond_to_query_openai(self, mock_openai, mock_load_config):
        mock_load_config.return_value = {"use_model": "openai", "llm_model": "gpt-3.5-turbo"}
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Test response"
        mock_client.chat.completions.create.return_value = mock_response
        brain = Brain()
        response = brain.respond_to_query("Hello", {})
        self.assertEqual(response, "Test response")



    @patch('utils.config_loader.load_config')
    @patch('core.brain.anthropic.Anthropic')
    def test_respond_to_query_claude(self, mock_anthropic, mock_load_config):
        mock_load_config.return_value = {"use_model": "claude"}
        mock_client = MagicMock()
        mock_anthropic.return_value = mock_client
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Claude response")]
        mock_client.messages.create.return_value = mock_response
        brain = Brain()
        response = brain.respond_to_query("Hello", {})
        self.assertEqual(response, "Claude response")

    @patch('utils.config_loader.load_config')
    @patch('ollama.chat')
    def test_respond_to_query_exception(self, mock_chat, mock_load_config):
        mock_load_config.return_value = {"use_model": "ollama", "ollama_model": "llama3.2"}
        mock_chat.side_effect = Exception("API error")
        brain = Brain()
        response = brain.respond_to_query("Hello", {})
        self.assertIn("⚠️", response)

    @patch('utils.config_loader.load_config')
    @patch('ollama.chat')
    def test_memory_update(self, mock_chat, mock_load_config):
        mock_load_config.return_value = {"use_model": "ollama", "ollama_model": "llama3.2"}
        mock_chat.return_value = {'message': {'content': 'Test response'}}
        brain = Brain()
        memory = {}
        brain.respond_to_query("Test query", memory)
        self.assertIn("context", memory)

    @patch('utils.config_loader.load_config')
    def test_plugin_invocation(self, mock_load_config):
        mock_load_config.return_value = {"use_model": "ollama", "ollama_model": "llama3.2"}
        brain = Brain()
        response = brain.respond_to_query("PLUGIN: weather get_weather", {})
        self.assertEqual(response, "PLUGIN: weather get_weather")

if __name__ == '__main__':
    unittest.main()
