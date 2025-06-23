import unittest
from unittest.mock import patch, MagicMock
from core.brain import Brain

class TestBrain(unittest.TestCase):
    @patch('openai.Completion.create')
    def test_respond_to_query_openai(self, mock_create):
        mock_create.return_value = {
            "choices": [{"text": "Test response"}]
        }
        brain = Brain()
        brain.USE_MODEL = "openai"
        brain.client = MagicMock()
        brain.client.Completion.create = mock_create
        response = brain.respond_to_query("Hello")
        self.assertEqual(response, "Test response")

    @patch('anthropic.Anthropic')
    def test_respond_to_query_claude(self, mock_anthropic):
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="Claude response")]
        mock_client = mock_anthropic.return_value
        mock_client.messages.create.return_value = mock_response
        brain = Brain()
        brain.USE_MODEL = "claude"
        brain.client = mock_client
        response = brain.respond_to_query("Hello")
        self.assertEqual(response, "Claude response")

    @patch('openai.Completion.create')
    def test_respond_to_query_exception(self, mock_create):
        mock_create.side_effect = Exception("API error")
        brain = Brain()
        brain.USE_MODEL = "openai"
        brain.client = MagicMock()
        brain.client.Completion.create = mock_create
        response = brain.respond_to_query("Hello")
        self.assertIn("⚠️", response)

if __name__ == '__main__':
    unittest.main()
