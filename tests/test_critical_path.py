import unittest
import sys
import os
from unittest.mock import patch, MagicMock

# Add project root to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.brain import Brain
from core.voice import Voice
from core.plugin_manager import PluginManager

class TestCriticalPath(unittest.TestCase):

    def setUp(self):
        self.brain = Brain()
        self.voice = Voice()
        self.plugins = PluginManager()

    @patch.object(Voice, 'speak')
    def test_voice_speak(self, mock_speak):
        self.voice.speak("Hello")
        mock_speak.assert_called_with("Hello")

    @patch.object(Voice, 'listen', return_value="test command")
    def test_voice_listen(self, mock_listen):
        command = self.voice.listen()
        self.assertEqual(command, "test command")

    def test_brain_respond_to_query(self):
        response = self.brain.respond_to_query("Hello")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

    def test_plugin_manager_load(self):
        self.assertTrue(len(self.plugins.plugins) > 0)

    def test_plugin_manager_dispatch(self):
        # Assuming smart_dispatch returns a tuple (bool, response)
        result = self.plugins.smart_dispatch("test command")
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)

if __name__ == '__main__':
    unittest.main()
