import unittest
from unittest.mock import patch, MagicMock
from core.plugin_manager import PluginManager

class TestPluginManager(unittest.TestCase):
    def setUp(self):
        self.pm = PluginManager()

    def test_list_plugins(self):
        plugins = self.pm.list_plugins()
        self.assertIsInstance(plugins, list)

    @patch('importlib.import_module')
    def test_load_plugins_success(self, mock_import):
        mock_module = MagicMock()
        mock_module.run = MagicMock()
        mock_import.return_value = mock_module
        pm = PluginManager()
        self.assertIn('weather', pm.plugins)

    @patch('importlib.import_module')
    def test_load_plugins_failure(self, mock_import):
        mock_import.side_effect = ImportError("Module not found")
        pm = PluginManager()
        # Should not crash, just log error

    def test_execute_plugin_success(self):
        with patch.object(self.pm, 'plugins', {'test': MagicMock(run=MagicMock(return_value="Success"))}):
            result = self.pm.execute('test', ['arg'])
            self.assertEqual(result, "Success")

    def test_execute_plugin_not_found(self):
        result = self.pm.execute('nonexistent', [])
        self.assertIn("not found", result)

    def test_execute_plugin_error(self):
        mock_plugin = MagicMock()
        mock_plugin.run.side_effect = Exception("Plugin error")
        with patch.object(self.pm, 'plugins', {'test': mock_plugin}):
            result = self.pm.execute('test', [])
            self.assertIn("failed", result.lower())

    def test_smart_dispatch_weather(self):
        plugin, response = self.pm.smart_dispatch("What's the weather like?")
        self.assertEqual(plugin, "weather")

    def test_smart_dispatch_unknown(self):
        plugin, response = self.pm.smart_dispatch("Unknown command")
        self.assertIsNone(plugin)
        self.assertIn("couldn't find", response)

if __name__ == '__main__':
    unittest.main()
