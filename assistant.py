#!/usr/bin/env python3
"""Voice-controlled AI assistant.

Features:
- Voice input using `speech_recognition` (Google Web Speech API)
- Optional GPT responses via OpenAI API if OPENAI_API_KEY is set
- Text-to-speech output via `pyttsx3`
- Built-in command handling (time, open websites, exit)
- Text fallback mode for environments without a microphone
"""

from __future__ import annotations

import datetime as dt
import os
import webbrowser


EXIT_WORDS = {"exit", "quit", "stop", "bye"}


class VoiceAssistant:
    def __init__(self) -> None:
        self.tts_engine = None
        self.sr = None
        self.recognizer = None
        self.microphone = None
        self.client = None

        self._setup_tts()
        self._setup_speech_recognition()
        self._setup_openai()

    def _setup_tts(self) -> None:
        try:
            import pyttsx3

            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty("rate", 175)
        except Exception:
            self.tts_engine = None

    def _setup_speech_recognition(self) -> None:
        try:
            import speech_recognition as sr

            self.sr = sr
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
        except Exception:
            self.sr = None
            self.recognizer = None
            self.microphone = None

    def _setup_openai(self) -> None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return

        try:
            from openai import OpenAI

            self.client = OpenAI(api_key=api_key)
        except Exception:
            self.client = None

    def speak(self, message: str) -> None:
        print(f"Assistant: {message}")
        if self.tts_engine:
            self.tts_engine.say(message)
            self.tts_engine.runAndWait()

    def listen(self) -> str:
        if self.recognizer and self.microphone and self.sr:
            with self.microphone as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
                audio = self.recognizer.listen(source)
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.strip()
            except self.sr.UnknownValueError:
                self.speak("Sorry, I couldn't understand that.")
                return ""
            except self.sr.RequestError:
                self.speak("Speech service unavailable. Switching to text input.")

        return input("You (type command): ").strip()

    def ask_llm(self, prompt: str) -> str | None:
        if not self.client:
            return None
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful voice assistant. Keep responses short.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.4,
            )
            return response.choices[0].message.content or ""
        except Exception:
            return "I couldn't reach the AI service right now."

    def handle_command(self, command: str) -> bool:
        text = command.lower().strip()
        if not text:
            return True

        if text in EXIT_WORDS:
            self.speak("Goodbye!")
            return False

        if "time" in text:
            now = dt.datetime.now().strftime("%I:%M %p")
            self.speak(f"The current time is {now}.")
            return True

        if "open youtube" in text:
            webbrowser.open("https://youtube.com")
            self.speak("Opening YouTube.")
            return True

        if "open google" in text:
            webbrowser.open("https://google.com")
            self.speak("Opening Google.")
            return True

        ai_reply = self.ask_llm(command)
        if ai_reply:
            self.speak(ai_reply)
        else:
            self.speak(
                "I can help with commands like: what time is it, open youtube, open google, or general AI chat if OPENAI_API_KEY is configured."
            )
        return True

    def run(self) -> None:
        self.speak("Hello! I'm your AI assistant. Say a command.")
        running = True
        while running:
            cmd = self.listen()
            running = self.handle_command(cmd)


def main() -> int:
    assistant = VoiceAssistant()
    assistant.run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
