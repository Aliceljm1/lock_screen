#!/usr/bin/env python3
"""Xiong Xiong Lock Screen Challenge

A fun educational program that simulates a "virus" lock screen.
Children learn Windows shortcuts by trying to "crack" this fake virus.

Usage:
    python lock_screen.py                  # default medium mode
    python lock_screen.py --level easy     # easy mode
    python lock_screen.py --level hard     # hard mode
"""

import tkinter as tk
from tkinter import messagebox
import argparse
import random
import string


class LockScreen:
    """Fake virus lock screen with difficulty levels."""

    DARK_BG = "#0a0a0a"
    RED = "#ff0000"
    DARK_RED = "#cc0000"
    LIGHT_RED = "#ff3333"
    ORANGE = "#ff6600"
    YELLOW = "#ffcc00"
    GREEN = "#00ff00"
    DARK_GREEN = "#00cc00"
    GRAY = "#888888"
    BAR_BG = "#333333"
    HINT_BG = "#1a0000"
    CONGRATS_BG = "#001a00"

    FAKE_STATUSES = [
        "Encrypting files...",
        "Scanning vulnerabilities...",
        "Stealing browser data...",
        "Uploading sensitive data...",
        "Infecting USB devices...",
        "Modifying registry...",
        "Installing backdoor...",
        "Disabling antivirus...",
        "Corrupting boot sector...",
        "Hijacking network...",
    ]

    CN_FONT = "Microsoft YaHei"
    MONO_FONT = "Consolas"

    def __init__(self, level="medium"):
        self.level = level
        self.root = tk.Tk()
        self.root.title("WARNING - VIRUS DETECTED")
        self.root.configure(bg=self.DARK_BG)
        self.congrats_shown = False
        self._progress_value = 0.0

        self._setup_window()
        self._create_ui()
        self._bind_keys()
        self._start_animations()

    # ── Window Setup ─────────────────────────────────────────

    def _setup_window(self):
        if self.level == "easy":
            self._setup_easy()
        elif self.level == "medium":
            self._setup_medium()
        else:
            self._setup_hard()

    def _setup_easy(self):
        """Easy: normal windowed mode, all close methods work."""
        w, h = 900, 700
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_medium(self):
        """Medium: fullscreen, no title bar, but Alt+F4 / Win+D still work."""
        self.root.attributes("-fullscreen", True)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    def _setup_hard(self):
        """Hard: fullscreen + topmost, Alt+F4 intercepted."""
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.protocol("WM_DELETE_WINDOW", self._on_hard_close_attempt)

    # ── UI Construction ──────────────────────────────────────

    def _create_ui(self):
        main = tk.Frame(self.root, bg=self.DARK_BG)
        main.place(relx=0.5, rely=0.5, anchor="center")

        # Warning title (blinks)
        self.warning_label = tk.Label(
            main,
            text="\u26a0  VIRUS DETECTED  \u26a0",
            font=(self.MONO_FONT, 44, "bold"),
            fg=self.RED,
            bg=self.DARK_BG,
        )
        self.warning_label.pack(pady=(0, 15))

        # Skull decoration
        tk.Label(
            main,
            text="\u2620   \u2620   \u2620",
            font=(self.MONO_FONT, 38),
            fg=self.DARK_RED,
            bg=self.DARK_BG,
        ).pack(pady=(0, 25))

        # Red separator
        self._separator(main)

        # Main challenge text (pulses)
        self.challenge_label = tk.Label(
            main,
            text="\u718a\u718a\uff0c\u5f00\u52a8\u8111\u7b4b\u7834\u89e3\u8fd9\u4e2a\u7a97\u53e3",
            font=(self.CN_FONT, 34, "bold"),
            fg=self.LIGHT_RED,
            bg=self.DARK_BG,
        )
        self.challenge_label.pack(pady=(30, 40))

        # Fake status line
        self.status_label = tk.Label(
            main,
            text="Initializing...",
            font=(self.MONO_FONT, 15),
            fg=self.ORANGE,
            bg=self.DARK_BG,
        )
        self.status_label.pack(pady=(0, 12))

        # Progress bar
        bar_frame = tk.Frame(main, bg=self.BAR_BG, height=28, width=520)
        bar_frame.pack(pady=(0, 8))
        bar_frame.pack_propagate(False)

        self.progress_bar = tk.Frame(bar_frame, bg=self.RED, height=28)
        self.progress_bar.place(x=0, y=0, relheight=1.0, relwidth=0.0)

        self.progress_text = tk.Label(
            main,
            text="0%",
            font=(self.MONO_FONT, 13),
            fg=self.ORANGE,
            bg=self.DARK_BG,
        )
        self.progress_text.pack(pady=(0, 35))

        # Red separator
        self._separator(main)

        # Random hex "code" display
        self.code_label = tk.Label(
            main,
            text="",
            font=(self.MONO_FONT, 9),
            fg=self.GREEN,
            bg=self.DARK_BG,
            justify="center",
        )
        self.code_label.pack(pady=(20, 25))

        # F1 hint text
        self.f1_label = tk.Label(
            main,
            text="[  \u6309 F1 \u83b7\u53d6\u63d0\u793a  ]",
            font=(self.CN_FONT, 15),
            fg=self.GRAY,
            bg=self.DARK_BG,
        )
        self.f1_label.pack(pady=(0, 12))

        # Difficulty indicator
        level_display = {"easy": "EASY", "medium": "MEDIUM", "hard": "HARD"}
        tk.Label(
            main,
            text=f"DIFFICULTY: {level_display[self.level]}",
            font=(self.MONO_FONT, 11),
            fg="#444444",
            bg=self.DARK_BG,
        ).pack()

    def _separator(self, parent):
        tk.Frame(parent, bg=self.RED, height=2, width=620).pack(pady=(0, 5))

    # ── Key Bindings ─────────────────────────────────────────

    def _bind_keys(self):
        self.root.bind("<F1>", self._show_hints)
        self.root.bind("<Escape>", self._on_escape)

        if self.level == "hard":
            # Secret exit: Ctrl+Shift+Q
            self.root.bind("<Control-Shift-q>", self._secret_exit)
            self.root.bind("<Control-Shift-Q>", self._secret_exit)

    def _on_escape(self, event=None):
        if self.level == "easy":
            self._on_close()

    # ── Hint Dialog ──────────────────────────────────────────

    def _show_hints(self, event=None):
        hint_win = tk.Toplevel(self.root)
        hint_win.title("TOP SECRET - HINTS")
        hint_win.configure(bg=self.HINT_BG)

        w, h = 580, 520
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        hint_win.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")
        hint_win.resizable(False, False)
        hint_win.grab_set()

        if self.level == "hard":
            hint_win.attributes("-topmost", True)

        # Title
        tk.Label(
            hint_win,
            text="\U0001f513  \u7834\u89e3\u63d0\u793a  \U0001f513",
            font=(self.CN_FONT, 22, "bold"),
            fg="#ff4444",
            bg=self.HINT_BG,
        ).pack(pady=(25, 20))

        hints = [
            ("1.", "Alt + F4", "\u5173\u95ed\u5f53\u524d\u7a97\u53e3"),
            ("2.", "Win + D", "\u663e\u793a\u684c\u9762"),
            ("3.", "Alt + Tab", "\u5207\u6362\u5230\u5176\u4ed6\u7a97\u53e3"),
            ("4.", "Ctrl + Alt + Del", "\u6253\u5f00\u5b89\u5168\u9009\u9879"),
            ("5.", "Ctrl + Shift + Esc", "\u76f4\u63a5\u6253\u5f00\u4efb\u52a1\u7ba1\u7406\u5668"),
            ("6.", "Win \u952e", "\u6253\u5f00\u5f00\u59cb\u83dc\u5355"),
        ]

        hint_frame = tk.Frame(hint_win, bg=self.HINT_BG)
        hint_frame.pack(padx=45, fill="x")

        for num, key, desc in hints:
            row = tk.Frame(hint_frame, bg=self.HINT_BG)
            row.pack(fill="x", pady=4)

            tk.Label(
                row, text=num, width=3,
                font=(self.MONO_FONT, 13, "bold"),
                fg=self.YELLOW, bg=self.HINT_BG, anchor="e",
            ).pack(side="left")

            tk.Label(
                row, text=f"  {key}",
                font=(self.MONO_FONT, 13, "bold"),
                fg="#ffffff", bg=self.HINT_BG, anchor="w", width=22,
            ).pack(side="left")

            tk.Label(
                row, text=desc,
                font=(self.CN_FONT, 13),
                fg=self.YELLOW, bg=self.HINT_BG, anchor="w",
            ).pack(side="left")

        # Hard mode extra hints
        if self.level == "hard":
            tk.Label(
                hint_win, text="",
                bg=self.HINT_BG,
            ).pack()

            for extra in [
                "\u26a0  \u56f0\u96be\u6a21\u5f0f: \u90e8\u5206\u65b9\u6cd5\u5df2\u88ab\u62e6\u622a!",
                "\U0001f4a1  \u8bd5\u8bd5\u4efb\u52a1\u7ba1\u7406\u5668\u7ed3\u675f\u8fdb\u7a0b...",
                "\U0001f4a1  \u6216\u8005\u627e\u5230\u9690\u85cf\u7684\u9000\u51fa\u7ec4\u5408\u952e...",
            ]:
                tk.Label(
                    hint_win, text=extra,
                    font=(self.CN_FONT, 12),
                    fg="#ff8800", bg=self.HINT_BG,
                ).pack(pady=2)

        # Close button
        tk.Button(
            hint_win,
            text="\u6211\u77e5\u9053\u4e86",
            font=(self.CN_FONT, 13, "bold"),
            fg="#ffffff",
            bg="#cc0000",
            activebackground="#ff0000",
            activeforeground="#ffffff",
            relief="flat",
            padx=30,
            pady=6,
            cursor="hand2",
            command=hint_win.destroy,
        ).pack(pady=(25, 15))

    # ── Close Handlers ───────────────────────────────────────

    def _on_close(self):
        self._show_congratulations()

    def _on_hard_close_attempt(self):
        messagebox.showwarning(
            "ACCESS DENIED",
            "\u54c8\u54c8, \u6ca1\u90a3\u4e48\u5bb9\u6613!\n\u518d\u60f3\u60f3\u5176\u4ed6\u529e\u6cd5\u5427~",
        )

    def _secret_exit(self, event=None):
        self._show_congratulations()

    # ── Congratulations Screen ───────────────────────────────

    def _show_congratulations(self):
        if self.congrats_shown:
            return
        self.congrats_shown = True

        # Clear all virus UI
        for widget in self.root.winfo_children():
            widget.destroy()

        # Switch to friendly windowed mode
        self.root.attributes("-fullscreen", False)
        self.root.attributes("-topmost", False)
        self.root.configure(bg=self.CONGRATS_BG)
        self.root.title("YOU WIN!")

        w, h = 540, 420
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        self.root.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")
        self.root.resizable(False, False)

        frame = tk.Frame(self.root, bg=self.CONGRATS_BG)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        # Trophy icon
        tk.Label(
            frame,
            text="\U0001f3c6",
            font=("Segoe UI Emoji", 64),
            bg=self.CONGRATS_BG,
        ).pack(pady=(0, 10))

        # Main congratulations
        tk.Label(
            frame,
            text="\u606d\u559c\u4f60!\n\u7b2c\u4e00\u4e2a\u75c5\u6bd2\u88ab\u4f60\u7834\u89e3\u4e86!",
            font=(self.CN_FONT, 26, "bold"),
            fg=self.GREEN,
            bg=self.CONGRATS_BG,
        ).pack(pady=(0, 15))

        # Encouragement
        tk.Label(
            frame,
            text="\u718a\u718a\u771f\u68d2!  \u4f60\u662f\u7535\u8111\u5c0f\u8fbe\u4eba!",
            font=(self.CN_FONT, 17),
            fg=self.DARK_GREEN,
            bg=self.CONGRATS_BG,
        ).pack(pady=(0, 30))

        # OK button
        tk.Button(
            frame,
            text="\u592a\u7b80\u5355\u4e86!",
            font=(self.CN_FONT, 14, "bold"),
            fg="#ffffff",
            bg="#006600",
            activebackground="#009900",
            activeforeground="#ffffff",
            relief="flat",
            padx=30,
            pady=8,
            cursor="hand2",
            command=self.root.destroy,
        ).pack()

        self.root.protocol("WM_DELETE_WINDOW", self.root.destroy)

    # ── Animations ───────────────────────────────────────────

    def _start_animations(self):
        self._animate_warning()
        self._animate_challenge()
        self._animate_progress()
        self._animate_code()
        self._animate_f1_hint()

    def _animate_warning(self):
        """Blink the warning title between red and hidden."""
        if self.congrats_shown:
            return
        try:
            cur = self.warning_label.cget("fg")
            nxt = self.DARK_BG if cur == self.RED else self.RED
            self.warning_label.configure(fg=nxt)
            self.root.after(700, self._animate_warning)
        except tk.TclError:
            pass

    def _animate_challenge(self):
        """Pulse the challenge text brightness."""
        if self.congrats_shown:
            return
        try:
            cur = self.challenge_label.cget("fg")
            nxt = "#ff6666" if cur == self.LIGHT_RED else self.LIGHT_RED
            self.challenge_label.configure(fg=nxt)
            self.root.after(1200, self._animate_challenge)
        except tk.TclError:
            pass

    def _animate_progress(self):
        """Fake progress bar that loops endlessly."""
        if self.congrats_shown:
            return
        try:
            self._progress_value += random.uniform(0.3, 1.8)
            if self._progress_value >= 99.0:
                self._progress_value = 0.0

            pct = self._progress_value / 100.0
            self.progress_bar.place(x=0, y=0, relheight=1.0, relwidth=pct)
            self.progress_text.configure(text=f"{int(self._progress_value)}%")

            if random.random() < 0.06:
                self.status_label.configure(
                    text=random.choice(self.FAKE_STATUSES)
                )

            self.root.after(180, self._animate_progress)
        except tk.TclError:
            pass

    def _animate_code(self):
        """Show random hex "hacker code" text."""
        if self.congrats_shown:
            return
        try:
            chars = string.hexdigits + "  "
            lines = [
                "".join(random.choice(chars) for _ in range(58))
                for _ in range(3)
            ]
            self.code_label.configure(text="\n".join(lines))
            self.root.after(120, self._animate_code)
        except tk.TclError:
            pass

    def _animate_f1_hint(self):
        """Blink the F1 hint text to draw attention."""
        if self.congrats_shown:
            return
        try:
            cur = self.f1_label.cget("fg")
            nxt = "#555555" if cur == self.GRAY else self.GRAY
            self.f1_label.configure(fg=nxt)
            self.root.after(1500, self._animate_f1_hint)
        except tk.TclError:
            pass

    # ── Run ──────────────────────────────────────────────────

    def run(self):
        self.root.mainloop()


def main():
    parser = argparse.ArgumentParser(
        description="Xiong Xiong Lock Screen Challenge - "
        "A fun fake virus for learning Windows shortcuts"
    )
    parser.add_argument(
        "--level",
        choices=["easy", "medium", "hard"],
        default="medium",
        help="Difficulty: easy / medium / hard (default: medium)",
    )
    args = parser.parse_args()

    LockScreen(level=args.level).run()


if __name__ == "__main__":
    main()
