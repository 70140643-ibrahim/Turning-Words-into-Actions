# Hellllllo Jiiiiii Yea Hai Ibrahim Voice Assistant.
import os, sys, subprocess, datetime, platform, webbrowser, threading, wikipedia
import speech_recognition as sr

def speak(text):
    print(f"Ibrahim: {text}")
    subprocess.run(["say", "-v", "Samantha", text])

# This Part Will deal with Speech Okay...
recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen_once():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        cmd = recognizer.recognize_google(audio, language="en-in").lower()
        print(f"You said: {cmd}")
        return cmd
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
    except sr.RequestError:
        speak("Network error.")
    return ""

# Here I have added some commands We can Also add more....
SITES = {
    "youtube": "https://youtube.com",
    "google": "https://google.com",
    "facebook": "https://facebook.com",
    "instagram": "https://instagram.com",
    "twitter": "https://twitter.com",
    "linkedin": "https://linkedin.com",
}
APPS = {
    "code": "Visual Studio Code",
    "safari": "Safari",
    "chrome": "Google Chrome",
    "firefox": "Firefox",
    "terminal": "Terminal",
    "notes": "Notes",
    "calculator": "Calculator",
    "spotify": "Spotify",
}

def open_web_or_app(name):
    name = name.lower()
    if name in SITES:
        webbrowser.open(SITES[name])
        speak(f"Opening {name}")
    elif name in APPS:
        subprocess.run(["open", "-a", APPS[name]])
        speak(f"Launching {APPS[name]}")
    else:
        speak(f"I don't know how to open {name}")

def play_music():
    for d in [os.path.expanduser("~/Music"), os.path.expanduser("~/Downloads")]:
        if os.path.isdir(d):
            songs = [f for f in os.listdir(d) if f.lower().endswith(('.mp3', '.wav', '.m4a', '.flac'))]
            if songs:
                subprocess.run(["open", os.path.join(d, songs[0])])
                speak("Playing music")
                return
    speak("No music files found.")

def tell_time():
    speak(f"The time is {datetime.datetime.now().strftime('%H:%M')}")

def search_wikipedia(query):
    speak("Searching Wikipedia…")
    topic = query.replace("wikipedia", "").replace("wiki", "").strip()
    try:
        summary = wikipedia.summary(topic, sentences=2)
        speak("According to Wikipedia:")
        speak(summary)
    except:
        speak("I couldn't find anything on that topic.")

def list_dirs():
    speak("Your main directories: Desktop, Documents, Downloads, Pictures, Movies, Applications")

def system_info():
    speak(f"{platform.system()} {platform.version()} {platform.architecture()[0]}")

def handle_command(cmd):
    cmd = cmd.lower()
    if any(k in cmd for k in ("wikipedia", "wiki")):
        search_wikipedia(cmd)
    elif "time" in cmd:
        tell_time()
    elif cmd.startswith("open "):
        open_web_or_app(cmd.split("open ", 1)[1].strip())
    elif "play music" in cmd:
        play_music()
    elif "list directories" in cmd or "show directories" in cmd:
        list_dirs()
    elif "system info" in cmd:
        system_info()
    elif any(k in cmd for k in ("exit", "quit", "goodbye", "stop")):
        speak("Goodbye! Have a great day.")
        return False
    else:
        speak("Try: open YouTube, play music, time, Wikipedia …")
    return True

# Fall Back voice ko deal kr raha ha....
def console_mode():
    speak("Hello! I am Ibrahim. How can I help?")
    while True:
        cmd = listen_once()
        if cmd and not handle_command(cmd):
            break

# Chota Mota Ui add kra
def gui_mode():
    import tkinter as tk
    from tkinter import ttk

    class IbrahimGUI:
        def __init__(self, root):
            self.root = root
            root.title("Ibrahim Assistant")
            root.geometry("500x600")
            root.configure(bg="#1e1e1e")
            self.listening = False
            self.build_widgets()
            self.speak_line("Press Start to talk.")

        def build_widgets(self):
            style = ttk.Style()
            style.theme_use("clam")
            style.configure("TButton", foreground="#fff", background="#3c3c3c", borderwidth=0)
            style.map("TButton", background=[("active", "#555")])

            header = tk.Label(self.root, text="Ibrahim Assistant", bg="#1e1e1e", fg="#00ff99",
                              font=("SF Pro Display", 18, "bold"))
            header.pack(pady=10)

            self.txt = tk.Text(self.root, wrap="word", bg="#2b2b2b", fg="#f0f0f0", insertbackground="#fff",
                               font=("SF Pro Display", 12), border=0)
            self.txt.pack(fill="both", expand=True, padx=15, pady=10)

            btn_frm = tk.Frame(self.root, bg="#1e1e1e")
            btn_frm.pack(pady=5)
            self.start_btn = ttk.Button(btn_frm, text="▶ Start", command=self.start)
            self.start_btn.grid(row=0, column=0, padx=5)
            self.stop_btn = ttk.Button(btn_frm, text="⏹ Stop", command=self.stop, state="disabled")
            self.stop_btn.grid(row=0, column=1, padx=5)
            ttk.Button(btn_frm, text="🗑 Clear", command=lambda: self.txt.delete(1.0, "end")).grid(row=0, column=2, padx=5)

            opts = tk.Frame(self.root, bg="#1e1e1e")
            opts.pack(pady=5)
            self.top_var = tk.BooleanVar()
            tk.Checkbutton(opts, text="Always on top", variable=self.top_var, bg="#1e1e1e", fg="#ccc",
                           selectcolor="#1e1e1e", command=self.toggle_top).pack(side="left")
            tk.Label(opts, text="Transparency", bg="#1e1e1e", fg="#ccc").pack(side="left", padx=(15, 5))
            self.alpha = tk.Scale(opts, from_=30, to=100, orient="horizontal", bg="#1e1e1e", fg="#ccc",
                                  highlightthickness=0, command=self.set_alpha)
            self.alpha.set(100)
            self.alpha.pack(side="left")

        def toggle_top(self):
            self.root.attributes("-topmost", self.top_var.get())

        def set_alpha(self, val):
            self.root.attributes("-alpha", int(val) / 100)

        def start(self):
            if self.listening:
                return
            self.listening = True
            self.start_btn.config(state="disabled")
            self.stop_btn.config(state="normal")
            threading.Thread(target=self.listen_loop, daemon=True).start()

        def stop(self):
            self.listening = False
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")

        def user_line(self, text):
            self.txt.insert("end", text + "\n", "user")
            self.txt.tag_config("user", foreground="#00ffff")
            self.txt.see("end")

        def speak_line(self, text):
            self.txt.insert("end", text + "\n", "bot")
            self.txt.tag_config("bot", foreground="#00ff99")
            self.txt.see("end")
            speak(text)

        def listen_loop(self):
            with mic as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
            while self.listening:
                try:
                    with mic as source:
                        audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)
                    cmd = recognizer.recognize_google(audio, language="en-in").lower()
                    self.user_line(f"You: {cmd}")
                    cont = handle_command(cmd)
                    if not cont:
                        self.stop()
                        break
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    pass
                except Exception as e:
                    print("Listen error:", e)

    root = tk.Tk()
    IbrahimGUI(root)
    root.mainloop()


if __name__ == "__main__":
    try:
        # test tk quickly
        import tkinter as tk
        _t = tk.Tk()
        _t.destroy()
        gui_mode()
    except Exception as tk_err:
        print("GUI not available (%s) – falling back to console." % tk_err)
        console_mode()
        
        #Alhumdulilah....