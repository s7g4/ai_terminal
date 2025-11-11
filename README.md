# Jarvis AI Terminal

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Jarvis AI Terminal** is a fully functional, AI-powered terminal assistant that integrates a range of capabilities from task automation, memory management, AI-driven actions, to various plugins for productivity, entertainment, system control, and more. The system is designed to learn, adapt, and respond intelligently to commands.

---

## Table of Contents

- [Jarvis AI Terminal](#jarvis-ai-terminal)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
    - [Core Features:](#core-features)
  - [Installation](#installation)
    - [Requirements:](#requirements)
    - [Steps:](#steps)
  - [Usage](#usage)
  - [Available Commands](#available-commands)
  - [Plugin Commands](#plugin-commands)
  - [Customization](#customization)
  - [Additional Features](#additional-features)
  - [Troubleshooting](#troubleshooting)
  - [Contributing](#contributing)
  - [License](#license)
  - [Acknowledgements](#acknowledgements)

---

## Features

### Core Features:
1. **Natural Language Understanding**: 
   - Powered by **OpenAI GPT-4** and **Claude-3-Sonnet** for understanding and generating responses.
   
2. **Voice Interface**:
   - **Text-to-Speech (TTS)**: Uses `gTTS` for reliable online voice responses with fallback to `espeak` when offline.
   - **Speech-to-Text (STT)**: Convert spoken commands into text for hands-free interactions.

3. **Enhanced Memory Management**:
   - Persistent memory storage with new MemoryManager class.
   - Context-aware interaction history (last 20 conversations).
   - Scheduled task persistence across restarts.
   - Configurable memory limits and pruning.
   - JSON-based storage with automatic backup.

4. **Plugins**:
   - A robust plugin system with over 17 plugins for web searching, productivity tools, AI tools, entertainment, system control, and more.
   - **Web Search**: Automatically fetches up-to-date results when the local data is exhausted.
   - **AI Tools**: Various built-in tools for machine learning, prompt generation, and more.
   - **Email Manager**: Manage emails directly from the terminal.
   - **Movie Recommender**: Get personalized movie recommendations.
   - **Music Player**: Play your favorite music with voice command integration.
   - **System Control**: Manage system processes, files, and more from the terminal.

5. **Self-Sufficiency**:
   - AI is self-sufficient and can auto-install tools and dependencies when needed.
   - Can handle commands such as “create a project in Next.js” or “play a song” without additional setup.

6. **CLI Interface**:
   - Simple, intuitive command-line interface that supports both text and voice inputs.

7. **Dynamic Plugin Loading**:
   - Automatically loads required plugins based on the task without needing manual intervention.
   - Auto-updates plugins if newer versions are available.

8. **Customizable Personality**:
   - Jarvis’s persona, tone, and mood can be customized to fit different user preferences. It can act confident, humorous, or serious depending on context.

9. **Alias Commands**:
   - Define and use custom aliases for frequently used commands.
   
10. **APIs for Dynamic Data**:
    - Integrates with various web APIs (e.g., Google Search API, email, weather, and movie APIs) to provide up-to-date results.

---

## Installation

### Requirements:
- Python 3.8+ (ensure you have a compatible version installed).
- Virtualenv (for environment isolation).

### Steps:
1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/jarvis-ai-terminal.git
   cd jarvis-ai-terminal
   ```

2. Create a virtual environment:

   ```bash
   python3 -m venv jarvis_env
   source jarvis_env/bin/activate  # On Windows: jarvis_env\Scripts\activate
   ```

3. Install required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables in a `.env` file (e.g., API keys, Google Search API, OpenAI, etc.).

5. Create and configure your default settings in `config.json` and `memory.json`.

---

## Usage

Once the system is set up and running, you can start Jarvis AI Terminal by running:

```bash
python main.py
```

---

## Available Commands

1. AI Interaction:

   - "What can you do?" → Displays a list of available features.
   - "Hey Jarvis, tell me a joke" → Jarvis can tell jokes, make small talk, and more.

2. Voice Commands:

   - "play music" → Start playing music (you can specify a song or genre).
   - "open weather" → Fetch the current weather.
   - "check my email" → Check email inbox.

3. System Control:

   - "start a project" → Creates a new project based on the template you specify (Next.js, Flask, etc.).
   - "kill process <process_name>" → Kill a running process.

4. Plugin-based Commands:

   - "show weather" → Get the current weather.
   - "movie recommendations" → Get personalized movie suggestions.
   - "email manager" → Manage your email inbox.

5. Interactive CLI:

   Edit the configuration interactively by running `python config_loader.py`.

---

## Plugin Commands

1. Productivity:

   - "todo": Add/remove tasks from your todo list.
   - "calendar": Check upcoming events or appointments.
   - "email_manager": Manage emails.

2. Development:

   - "git_helper": Get git status, commit history, and other git-related actions.
   - "repo_explorer": Explore project files and directories.
   - "code_explainer": Explain code snippets.

3. Entertainment:

   - "movie_recommender": Get movie recommendations based on your preferences.
   - "music_player": Play music or manage your playlist.

4. AI Tools:

   - "ai_agent": Access machine learning tools, prompts, and more.
   - "ml_generator": Generate machine learning models.
   - "prompt_engineer": Engineer AI prompts.

5. Cybersecurity:

   - "port_scanner": Scan and report open ports on your local or remote machine.
   - "hash_cracker": Attempt to crack hashes using various algorithms.
   - "vuln_detector": Scan for vulnerabilities in your system.

---

## Customization

1. Personality:

   - You can change Jarvis's tone, mood, and behavior through the `personality.json` file.
   - Adjust Jarvis’s tone (e.g., confident, friendly, serious) to match your preferences.

2. Voice:

   - Jarvis can speak to you using the `pyttsx3` TTS engine. Adjust settings like speech rate, volume, and voice ID in the `config.json`.

3. Aliases:

   - Add your own command aliases to `config.json` for faster, customized command input.

4. Web Search:

   - Jarvis uses the Google Custom Search API to fetch up-to-date information from the web when local data is exhausted.

---

## Additional Features

- Web Search: Fetch up-to-date information from the web using Google Custom Search API or any other search engine.
- Auto-Install Tools: Jarvis can automatically install missing tools or dependencies if a command requires them.
- Mood and Emotion Control: Jarvis can adapt its mood based on the context of the interaction (neutral, happy, sad, etc.).
- Auto-Migrate Config Versions: The system will auto-migrate config versions to ensure compatibility as the system evolves.
- CLI Config Editor: Allows users to interactively edit and update configuration files.

---

## Troubleshooting

- Ensure your microphone and speakers are properly configured and accessible.
- Verify that your API keys are correctly set in the `.env` file.
- If you encounter issues with voice recognition, try restarting the application or your system.
- Check the `logs/jarvis_terminal.log` file for detailed error messages.
- For plugin-related issues, ensure the plugins directory exists and contains valid plugin files.

---

## Audio Setup for PipeWire and Microphone Input

To ensure proper audio input handling with PipeWire replacing PulseAudio and JACK, follow these steps:

1. Run the provided setup script to check and enable PipeWire services, install recommended packages, and remove conflicting JACK packages:

```bash
bash setup_audio.sh
```

2. After running the script, it is recommended to reboot your system:

```bash
reboot
```

3. To list available input devices in Python, you can use the script:

```bash
python3 core/list_input_devices_pyaudio.py
```

4. The microphone test script `core/test_mic.py` already lists available microphones and selects an appropriate device index. If you encounter errors like `'NoneType' object has no attribute 'close'`, ensure you select the correct input device index from the list.

5. To force your application to use the PulseAudio or PipeWire backend, set the input device index accordingly in your code, for example:

```python
input_device_index = device_index_of('pulse')  # get from listing step
```

Replace `device_index_of('pulse')` with the actual device index obtained from the listing.

These steps should help resolve audio input issues related to PipeWire and device selection.
python3 core/list_input_devices_pyaudio.py

---

## Contributing

We welcome contributions to make Jarvis AI Terminal smarter and more functional! To contribute:

1. Fork this repository.

2. Create a new branch (`git checkout -b feature/your-feature-name`).

3. Commit your changes (`git commit -am 'Add new feature'`).

4. Push to the branch (`git push origin feature/your-feature-name`).

5. Create a new Pull Request.

---

## License

MIT License. See LICENSE for more information.

---

## Acknowledgements

- OpenAI GPT-4 for natural language understanding.
- Claude-3-Sonnet by Anthropic for advanced AI interaction.
- Ollama for local LLM integration (e.g., llama3.2).
- pyttsx3 and gTTS for text-to-speech functionality.
- Flask for building the plugin system.
- BeautifulSoup4 and Selenium for web scraping capabilities.

## Roadmap and Future Improvements

The project is functional in text mode with Ollama integration, but several areas remain for completion and enhancement. Below is a list of pending tasks and suggested improvements:

### Pending Tasks:
- **Virtual Environment Setup**: Re-enable and fix the `check_environment()` function in `main.py` to properly detect and guide setup of `jarvis_env` on Windows (address permission/copy errors during venv creation).
- **Voice Mode Compatibility**: Resolve Python 3.14 incompatibilities (e.g., Pydantic V1 warnings in OpenAI, skipped 'voice_assistant' plugin). Test and fully implement speech-to-text (SpeechRecognition) and text-to-speech (pyttsx3/gTTS) with microphone input using sounddevice or PyAudio alternatives.
- **Audio Setup**: Integrate and automate `setup_audio.sh` for Windows (e.g., via PowerShell equivalent). Fix device selection in `core/voice.py` and `core/test_mic.py` for PipeWire/PulseAudio on Linux and WASAPI on Windows.
- **Plugin Fixes**:
  - Test and fix all plugins (e.g., email_manager requires API keys; music_player may need local file access or streaming API).
  - Implement missing plugins like voice_assistant.
  - Add error handling for plugin execution failures.
- **Testing Coverage**: Expand unit tests in `tests/` to cover brain.py, voice.py, plugin_manager.py, and end-to-end interactions. Run `pytest` and aim for 80%+ coverage.
- **Memory and Config Persistence**: Ensure `data/memory.json` and `data/personality.json` handle concurrent access and backups. Add migration for config versions.
- **Ollama Integration**: Document Ollama setup (e.g., `ollama pull llama3.2`) and fallback to other models if local server is unavailable.

### Suggested Improvements:
- **Multi-Model Support**: Enhance `core/brain.py` to dynamically switch between Ollama (local), OpenAI, and Anthropic based on config or availability. Add streaming responses for better UX.
- **Error Handling and Logging**: Improve global exception handling in main.py and plugins. Use loguru more extensively for structured logs in `logs/jarvis_terminal.log`.
- **Security Enhancements**: Sanitize user inputs to prevent injection in plugins (e.g., system_control, file_manager). Add API key validation and .env loading.
- **Performance Optimizations**: Cache AI responses, limit context history in brain.py, and optimize plugin loading (lazy-load non-essential plugins).
- **UI/UX Enhancements**: Add a simple TUI (e.g., using rich or textual) for better text mode interaction. Support command history and tab completion.
- **Plugin Expansion**: Add new plugins for code execution (sandboxed), calendar integration (Google Calendar API), or image generation (DALL-E via OpenAI).
- **Documentation**: 
  - Add inline docstrings to all modules.
  - Create a plugins.md file detailing each plugin's commands and dependencies.
  - Update installation for Windows-specific issues (e.g., Git Bash vs. CMD).
- **Deployment and Packaging**: Create a setup.py or pyproject.toml for pip installable package. Add Docker support for easy deployment.
- **Cross-Platform Compatibility**: Test on macOS/Linux/Windows fully, especially audio and venv creation.
- **Advanced Features**: Implement long-term memory with vector embeddings (e.g., via FAISS), multi-turn conversations, or integration with external tools like VSCode extensions.

Contributions to these areas are welcome! Prioritize voice mode and testing for a more complete release.
