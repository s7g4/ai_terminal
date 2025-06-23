import unittest
from unittest.mock import patch, MagicMock
from core.command_handler import CommandHandler

class TestCommandHandler(unittest.TestCase):
    def setUp(self):
        self.ch = CommandHandler()

    @patch.object(CommandHandler, 'respond')
    def test_handle_empty_command(self, mock_respond):
        result = self.ch.handle("")
        self.assertEqual(result, "No command provided.")
        mock_respond.assert_not_called()

    @patch.object(CommandHandler, 'respond')
    def test_handle_plugin_command(self, mock_respond):
        with patch.object(self.ch.plugins, 'smart_dispatch', return_value=('dummy', 'response')), \
            patch.object(self.ch.plugins, 'execute', return_value='response'):
            result = self.ch.handle("test command")
            self.assertIn('response', result)
            mock_respond.assert_called()

    @patch.object(CommandHandler, 'respond')
    def test_handle_ai_fallback(self, mock_respond):
        with patch.object(self.ch.plugins, 'smart_dispatch', side_effect=[(None, None), ('dummy', 'response')]), \
            patch.object(self.ch.brain, 'respond_to_query', side_effect=["dummy", "response"]), \
            patch.object(self.ch.plugins, 'execute', return_value='response'):
            result = self.ch.handle("test command")
            self.assertIn('response', result)
            mock_respond.assert_called()

if __name__ == '__main__':
    unittest.main()
