import unittest
from unittest.mock import patch, MagicMock
from core.plugin_manager import PluginManager

class TestPluginManager(unittest.TestCase):
    def setUp(self):
        self.pm = PluginManager()

    def test_list_plugins(self):
        plugins = self.pm.list_plugins()
        self.assertIsInstance(plugins, list)

    @patch('core.plugin_manager.importlib.import_module')
    def test_load_plugins(self, mock_import_module):
        mock_module = MagicMock()
        mock_module.run = MagicMock(return_value="run called")
        mock_import_module.return_value = mock_module

        pm = PluginManager()
        self.assertIn(mock_module, pm.plugins.values())

    def test_execute_plugin(self):
        # Add a dummy plugin
        class DummyPlugin:
            def run(self, command):
                return f"Executed {command}"
        self.pm.plugins['dummy'] = DummyPlugin()
        result = self.pm.execute('dummy', 'test command')
        self.assertEqual(result, "Executed test command")

    def test_execute_plugin_not_found(self):
        result = self.pm.execute('nonexistent', 'test')
        self.assertEqual(result, "Plugin 'nonexistent' not found.")

    def test_get_plugin_help(self):
        class DummyPlugin:
            def help(self):
                return "Help text"
        self.pm.plugins['dummy'] = DummyPlugin()
        help_text = self.pm.get_plugin_help('dummy')
        self.assertEqual(help_text, "Help text")

    def test_get_plugin_help_no_help(self):
        class DummyPlugin:
            pass
        self.pm.plugins['dummy'] = DummyPlugin()
        help_text = self.pm.get_plugin_help('dummy')
        self.assertEqual(help_text, "No help available for 'dummy'.")

    def test_smart_dispatch(self):
        # Add a dummy plugin with run method
        class DummyPlugin:
            def run(self, command):
                return "response"
        self.pm.plugins['dummy'] = DummyPlugin()
        plugin_name, response = self.pm.smart_dispatch("weather forecast")
        self.assertEqual(plugin_name, "weather")
        self.assertIsInstance(response, str)

if __name__ == '__main__':
    unittest.main()
