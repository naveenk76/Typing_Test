import tkinter as tk
from tkinter import font
import random
import time

# Sample texts for typing test
SAMPLE_TEXTS = [
    "The quick brown fox jumps over the lazy dog near the river bank while the sun sets slowly in the west.",
    "Programming is the art of telling another human what one wants the computer to do in a precise manner.",
    "Success is not final failure is not fatal it is the courage to continue that truly counts in life.",
    "The beautiful mountains stood tall against the horizon as birds flew gracefully across the cloudy sky.",
    "Learning to code opens doors to creativity and problem solving that can change the world around us.",
    "A journey of a thousand miles begins with a single step taken with determination and patience each day.",
    "Technology has transformed the way people communicate work and live their lives in the modern era.",
    "Reading books regularly helps improve vocabulary concentration and imagination in a wonderful way.",
]

class TypingSpeedTest:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("900x650")
        self.root.configure(bg="#1e1e2e")
        self.root.resizable(False, False)

        # State variables
        self.sample_text = ""
        self.start_time = None
        self.test_started = False
        self.test_finished = False
        self.time_limit = 60
        self.timer_id = None
        self.correct_chars = 0
        self.total_typed = 0

        self.setup_ui()
        self.load_new_text()

    def setup_ui(self):
        # Fonts
        self.title_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.text_font = font.Font(family="Consolas", size=16)
        self.label_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.stat_font = font.Font(family="Helvetica", size=14, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")

        # Title
        title = tk.Label(
            self.root, text="⌨  Typing Speed Test",
            font=self.title_font, bg="#1e1e2e", fg="#89b4fa"
        )
        title.pack(pady=(20, 10))

        # Stats frame
        stats_frame = tk.Frame(self.root, bg="#1e1e2e")
        stats_frame.pack(pady=10)

        self.timer_label = tk.Label(
            stats_frame, text="Time: 60s", font=self.stat_font,
            bg="#1e1e2e", fg="#f9e2af", width=12
        )
        self.timer_label.pack(side=tk.LEFT, padx=10)

        self.wpm_label = tk.Label(
            stats_frame, text="WPM: 0", font=self.stat_font,
            bg="#1e1e2e", fg="#a6e3a1", width=12
        )
        self.wpm_label.pack(side=tk.LEFT, padx=10)

        self.accuracy_label = tk.Label(
            stats_frame, text="Accuracy: 100%", font=self.stat_font,
            bg="#1e1e2e", fg="#cba6f7", width=15
        )
        self.accuracy_label.pack(side=tk.LEFT, padx=10)

        # Text display area (using Text widget for per-char coloring)
        self.text_frame = tk.Frame(self.root, bg="#313244", bd=2, relief=tk.FLAT)
        self.text_frame.pack(pady=15, padx=30, fill=tk.BOTH)

        self.display = tk.Text(
            self.text_frame, wrap=tk.WORD, height=6,
            font=self.text_font, bg="#313244", fg="#cdd6f4",
            bd=0, padx=20, pady=20, cursor="arrow",
            spacing1=5, spacing3=5
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        self.display.config(state=tk.DISABLED)

        # Tag styles for character feedback
        self.display.tag_config("correct", foreground="#a6e3a1")
        self.display.tag_config("incorrect", foreground="#f38ba8", underline=True)
        self.display.tag_config("current", background="#585b70", foreground="#ffffff")
        self.display.tag_config("pending", foreground="#6c7086")

        # Input field
        input_label = tk.Label(
            self.root, text="Type here:", font=self.label_font,
            bg="#1e1e2e", fg="#cdd6f4"
        )
        input_label.pack(pady=(5, 5), anchor="w", padx=30)

        self.entry = tk.Text(
            self.root, height=3, font=self.text_font,
            bg="#313244", fg="#cdd6f4", insertbackground="#89b4fa",
            bd=0, padx=15, pady=10, wrap=tk.WORD
        )
        self.entry.pack(pady=(0, 15), padx=30, fill=tk.BOTH)

        # Bind key events
        self.entry.bind("<KeyRelease>", self.on_key_release)
        self.entry.bind("<Return>", lambda e: "break")  # prevent newlines

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#1e1e2e")
        btn_frame.pack(pady=(0, 20))

        self.restart_btn = tk.Button(
            btn_frame, text="↻  Restart Test", font=self.button_font,
            bg="#89b4fa", fg="#1e1e2e", bd=0, padx=20, pady=8,
            cursor="hand2", activebackground="#74c7ec",
            command=self.restart_test
        )
        self.restart_btn.pack(side=tk.LEFT, padx=5)

        self.quit_btn = tk.Button(
            btn_frame, text="✕  Quit", font=self.button_font,
            bg="#f38ba8", fg="#1e1e2e", bd=0, padx=20, pady=8,
            cursor="hand2", activebackground="#eba0ac",
            command=self.root.quit
        )
        self.quit_btn.pack(side=tk.LEFT, padx=5)

        # Status message
        self.status_label = tk.Label(
            self.root, text="Start typing to begin the test...",
            font=self.label_font, bg="#1e1e2e", fg="#6c7086"
        )
        self.status_label.pack(pady=(0, 15))

    def load_new_text(self):
        self.sample_text = random.choice(SAMPLE_TEXTS)
        self.display.config(state=tk.NORMAL)
        self.display.delete("1.0", tk.END)
        self.display.insert("1.0", self.sample_text)
        self.display.config(state=tk.DISABLED)
        self.color_pending_all()

    def color_pending_all(self):
        self.display.tag_remove("correct", "1.0", tk.END)
        self.display.tag_remove("incorrect", "1.0", tk.END)
        self.display.tag_remove("current", "1.0", tk.END)
        self.display.tag_add("pending", "1.0", tk.END)
        self.display.tag_add("current", "1.0", "1.1")

    def update_display_colors(self, typed):
        """Color each character based on typed input."""
        self.display.config(state=tk.NORMAL)
        self.display.tag_remove("correct", "1.0", tk.END)
        self.display.tag_remove("incorrect", "1.0", tk.END)
        self.display.tag_remove("current", "1.0", tk.END)
        self.display.tag_remove("pending", "1.0", tk.END)

        for i, ch in enumerate(self.sample_text):
            idx1 = f"1.{i}"
            idx2 = f"1.{i+1}"
            if i < len(typed):
                if typed[i] == ch:
                    self.display.tag_add("correct", idx1, idx2)
                else:
                    self.display.tag_add("incorrect", idx1, idx2)
            elif i == len(typed):
                self.display.tag_add("current", idx1, idx2)
            else:
                self.display.tag_add("pending", idx1, idx2)

        if len(typed) >= len(self.sample_text):
            # End of text reached
            self.display.tag_add("current", f"1.{len(self.sample_text)}", f"1.{len(self.sample_text)}")

        self.display.config(state=tk.DISABLED)

    def on_key_release(self, event):
        if self.test_finished:
            return

        # Ignore special keys
        if event.keysym in ("Shift_L", "Shift_R", "Control_L", "Control_R",
                            "Alt_L", "Alt_R", "Caps_Lock", "Tab", "Escape"):
            return

        typed = self.entry.get("1.0", "end-1c")

        # Start timer on first keypress
        if not self.test_started and typed:
            self.start_test()

        self.total_typed = len(typed)
        self.update_display_colors(typed)
        self.update_stats(typed)

        # Auto-finish when text is complete
        if len(typed) >= len(self.sample_text):
            self.finish_test()

    def start_test(self):
        self.test_started = True
        self.start_time = time.time()
        self.status_label.config(text="Test in progress... Keep typing!", fg="#f9e2af")
        self.update_timer()

    def update_timer(self):
        if not self.test_started or self.test_finished:
            return

        elapsed = time.time() - self.start_time
        remaining = max(0, self.time_limit - elapsed)
        self.timer_label.config(text=f"Time: {int(remaining)}s")

        if remaining <= 0:
            self.finish_test()
            return

        # Change color when time is low
        if remaining <= 10:
            self.timer_label.config(fg="#f38ba8")
        elif remaining <= 20:
            self.timer_label.config(fg="#fab387")

        self.timer_id = self.root.after(100, self.update_timer)

    def update_stats(self, typed):
        correct = sum(1 for i, ch in enumerate(typed)
                      if i < len(self.sample_text) and ch == self.sample_text[i])
        self.correct_chars = correct

        # Accuracy
        if len(typed) > 0:
            accuracy = (correct / len(typed)) * 100
        else:
            accuracy = 100
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.0f}%")

        # WPM (standard: 5 chars = 1 word)
        if self.start_time:
            elapsed_min = max((time.time() - self.start_time) / 60, 1/60)
            wpm = (correct / 5) / elapsed_min
            self.wpm_label.config(text=f"WPM: {int(wpm)}")

    def finish_test(self):
        if self.test_finished:
            return
        self.test_finished = True
        self.test_started = False

        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        typed = self.entry.get("1.0", "end-1c")
        correct = sum(1 for i, ch in enumerate(typed)
                      if i < len(self.sample_text) and ch == self.sample_text[i])
        accuracy = (correct / len(typed) * 100) if typed else 0

        elapsed_min = (time.time() - self.start_time) / 60 if self.start_time else 1/60
        wpm = (correct / 5) / max(elapsed_min, 1/60)

        self.wpm_label.config(text=f"WPM: {int(wpm)}")
        self.accuracy_label.config(text=f"Accuracy: {accuracy:.0f}%")
        self.timer_label.config(text="Time: 0s")

        # Disable typing
        self.entry.config(state=tk.DISABLED)

        # Show result message
        self.status_label.config(
            text=f"✓ Test Complete!  Final WPM: {int(wpm)}  |  Accuracy: {accuracy:.0f}%",
            fg="#a6e3a1"
        )

    def restart_test(self):
        # Cancel any running timer
        if self.timer_id:
            try:
                self.root.after_cancel(self.timer_id)
            except Exception:
                pass
            self.timer_id = None

        # Reset state
        self.test_started = False
        self.test_finished = False
        self.start_time = None
        self.correct_chars = 0
        self.total_typed = 0

        # Reset entry
        self.entry.config(state=tk.NORMAL)
        self.entry.delete("1.0", tk.END)
        self.entry.focus_set()

        # Reset labels
        self.timer_label.config(text="Time: 60s", fg="#f9e2af")
        self.wpm_label.config(text="WPM: 0", fg="#a6e3a1")
        self.accuracy_label.config(text="Accuracy: 100%", fg="#cba6f7")
        self.status_label.config(text="Start typing to begin the test...", fg="#6c7086")

        # Load fresh text
        self.load_new_text()


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedTest(root)
    root.mainloop()