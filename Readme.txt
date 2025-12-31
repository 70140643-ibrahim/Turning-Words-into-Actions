Title: Turning Words Into Action

Ibrahim Voice Assistant is a lightweight voice-controlled automation system built in Python. The assistant listens to spoken commands and converts them into real computer actions using built-in OS integrations.

Purpose

To allow users to control applications, browse the web, and retrieve information hands-free using speech recognition and system command execution.

Core Functional Components

Voice Input: Captured through microphone using speech_recognition

Speech Processing: Voice converted to text via Google Speech API

Command Execution: Text commands routed to system functions

Output: Responses spoken using macOS say TTS voice (Samantha)

Background Listening: GUI mode keeps voice recognition active using threads

System Interaction: Opens websites/apps, plays local music, tells time, fetches Wikipedia summaries, and displays system info

Fail-Safe Design: If GUI fails to launch, system automatically switches to console mode

Supported Capabilities
Category	Examples
Web Automation	Open YouTube, Google, Facebook, Instagram, etc.
App Control	Launch VS Code, Chrome, Notes, Spotify, Terminal
Local Tasks	Play music from system folders
Information Retrieval	Read Wikipedia summaries
System Utility	Tell time, show OS version/architecture
Session Control	Exit or stop assistant by voice
Technology Stack

Language: Python 3

GUI: Tkinter

TTS: macOS system voice (say)

Speech Recognition: Google API via speech_recognition

External Data: Wikipedia summaries

Project Outcome

A single-file assistant that:

Takes spoken commands

Understands intent

And performs real system automation tasks

While keeping UI responsive through background voice threads
