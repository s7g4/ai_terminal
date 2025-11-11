import unittest
from unittest.mock import patch, MagicMock
from core.voice import Voice
import sys

class TestVoice(unittest.TestCase):
    def setUp(self):
        with patch('speech_recognition.Recognizer'):
            self.voice = Voice()

    @patch('speech_recognition.Recognizer')
    def test_listen_success(self, mock_recognizer):
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.recognize_google.return_value = "test speech"
        with patch('speech_recognition.Microphone') as mock_mic:
            mock_mic_instance = MagicMock()
            mock_mic.return_value.__enter__.return_value = mock_mic_instance
            mock_mic_instance.__enter__.return_value = mock_mic_instance
            result = self.voice.listen()
            self.assertEqual(result, "test speech")

    @patch('speech_recognition.Recognizer')
    def test_listen_failure(self, mock_recognizer):
        mock_recognizer_instance = MagicMock()
        mock_recognizer.return_value = mock_recognizer_instance
        mock_recognizer_instance.recognize_google.side_effect = Exception("Recognition failed")
        with patch('speech_recognition.Microphone') as mock_mic:
            mock_mic_instance = MagicMock()
            mock_mic.return_value.__enter__.return_value = mock_mic_instance
            mock_mic_instance.__enter__.return_value = mock_mic_instance
            result = self.voice.listen()
            self.assertIsNone(result)

    def test_speak_with_engine(self):
        self.voice.engine = MagicMock()
        self.voice.speak("Hello")
        self.voice.engine.say.assert_called_with("Hello")
        self.voice.engine.runAndWait.assert_called_once()

    def test_speak_without_engine(self):
        self.voice.engine = None
        # Should not raise exception
        self.voice.speak("Hello")

    def test_change_mood(self):
        self.voice.engine = MagicMock()
        self.voice.change_mood("happy")
        self.voice.engine.setProperty.assert_called()

    def test_python_3_14_compatibility(self):
        # Test that recognizer is None if SpeechRecognition fails
        voice_no_recognizer = Voice()
        if voice_no_recognizer.recognizer is None:
            result = voice_no_recognizer.listen()
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
