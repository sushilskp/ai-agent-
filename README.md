# AI Voice Assistant

A simple AI assistant you can control by voice commands.

## Features
- 🎙️ Voice input with `speech_recognition`
- 🔊 Voice output with `pyttsx3`
- 🤖 AI responses using OpenAI (when `OPENAI_API_KEY` is configured)
- 🧠 Built-in commands:
  - "what time is it"
  - "open youtube"
  - "open google"
  - "exit" / "quit" / "stop"
- ⌨️ Text fallback mode when microphone/speech service is unavailable

## Setup
1. Create a virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. (Optional) Set your OpenAI API key for AI chat:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

## Run

```bash
python3 assistant.py
```

## Notes
- `PyAudio` may require system audio packages depending on your OS.
- If voice input cannot initialize, the assistant automatically switches to typed input.
