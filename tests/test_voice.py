import unittest
from unittest.mock import patch, MagicMock
from core.voice import Voice

class TestVoice(unittest.TestCase):
    @patch('core.voice.pyttsx3.init')
    def test_speak(self, mock_init):
        mock_engine = MagicMock()
        mock_init.return_value = mock_engine
        voice = Voice()
        voice.speak("Hello")
        mock_engine.say.assert_called_with("Hello")
        mock_engine.runAndWait.assert_called()

    @patch('core.voice.sr.Recognizer')
    @patch('core.voice.sr.Microphone')
    def test_listen_no_audio_devices(self, mock_microphone, mock_recognizer):
        mock_microphone.list_microphone_names.return_value = []
        voice = Voice()
        result = voice.listen()
        self.assertIsNone(result)

    @patch('core.voice.sr.Recognizer')
    @patch('core.voice.sr.Microphone')
    def test_listen_with_audio(self, mock_microphone, mock_recognizer):
        mock_microphone.list_microphone_names.return_value = ['Microphone 1']
        mock_recognizer_instance = mock_recognizer.return_value
        mock_recognizer_instance.recognize_google.return_value = "test command"
        voice = Voice()
        result = voice.listen()
        self.assertEqual(result, "test command")

if __name__ == '__main__':
    unittest.main()
