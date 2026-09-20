import tkinter as tk
from integrated_text_speech import speak_text


class AccessibleVirtualKeyboard(tk.Tk):

    def __init__(self):
        super().__init__()

        # ---------------- WINDOW ----------------

        self.title("GazeMate - Assistive Keyboard")
        self.geometry("1200x750")
        self.minsize(1000, 650)
        self.configure(bg="#071426")

        self.font_size = 20
        self.letter_buttons = []

        # ---------------- COLORS ----------------

        self.bg = "#071426"
        self.panel = "#0D1D35"
        self.key = "#1B3155"
        self.key_hover = "#294873"
        self.white = "#F4F7FF"
        self.cyan = "#39D5FF"
        self.blue = "#4169E1"

        # ---------------- MAIN CONTAINER ----------------

        main = tk.Frame(
            self,
            bg=self.bg
        )

        main.pack(
            fill=tk.BOTH,
            expand=True,
            padx=25,
            pady=20
        )

        # ---------------- HEADER ----------------

        header = tk.Frame(
            main,
            bg=self.bg
        )

        header.pack(
            fill=tk.X,
            pady=(0, 15)
        )

        logo = tk.Label(
            header,
            text="◉",
            font=("Arial", 42, "bold"),
            fg=self.cyan,
            bg=self.bg
        )

        logo.pack(
            side=tk.LEFT,
            padx=(5, 12)
        )

        title_frame = tk.Frame(
            header,
            bg=self.bg
        )

        title_frame.pack(
            side=tk.LEFT
        )

        title = tk.Label(
            title_frame,
            text="GazeMate",
            font=("Arial", 30, "bold"),
            fg=self.white,
            bg=self.bg
        )

        title.pack(
            anchor="w"
        )

        subtitle = tk.Label(
            title_frame,
            text="Look  •  Type  •  Communicate",
            font=("Arial", 12),
            fg="#7FB7E8",
            bg=self.bg
        )

        subtitle.pack(
            anchor="w"
        )

        tagline = tk.Label(
            header,
            text="Your Eyes. Your Voice. Your World.",
            font=("Arial", 14),
            fg="#A9C7E8",
            bg=self.bg
        )

        tagline.pack(
            side=tk.RIGHT,
            padx=10
        )

        # ---------------- TEXT DISPLAY ----------------

        text_panel = tk.Frame(
            main,
            bg=self.panel,
            highlightbackground=self.cyan,
            highlightthickness=2
        )

        text_panel.pack(
            fill=tk.X,
            pady=(0, 15)
        )

        text_left = tk.Frame(
            text_panel,
            bg=self.panel
        )

        text_left.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        self.text_display = tk.Text(
            text_left,
            height=2,
            font=("Arial", 23, "bold"),
            bg=self.panel,
            fg=self.white,
            insertbackground=self.cyan,
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=0,
            padx=20,
            pady=15
        )

        self.text_display.pack(
            fill=tk.BOTH,
            expand=True
        )

        self.text_display.insert(
            "1.0",
            "Your message will appear here..."
        )

        self.text_display.config(
            fg="#6685A8"
        )

        self.text_display.bind(
            "<FocusIn>",
            self._remove_placeholder
        )

        # ---------------- SPEAK BUTTON ----------------

        speak_button = tk.Button(
            text_panel,
            text="🔊",
            font=("Arial", 22, "bold"),
            bg="#3157C9",
            fg=self.white,
            activebackground="#4B72E8",
            activeforeground=self.white,
            relief=tk.FLAT,
            bd=0,
            width=4,
            height=2,
            command=self._on_speak
        )

        speak_button.pack(
            side=tk.RIGHT,
            padx=10,
            pady=10
        )

        # ---------------- QUICK PHRASES ----------------

        quick_frame = tk.Frame(
            main,
            bg=self.bg
        )

        quick_frame.pack(
            fill=tk.X,
            pady=(0, 15)
        )

        quick_phrases = [
            ("HELP!", "I need help!", "#E94B65"),
            ("WATER", "I need water.", "#258FE8"),
            ("PAIN", "I am in pain.", "#F2A63B"),
            ("YES", "Yes.", "#35C98A"),
            ("NO", "No.", "#E75B9A")
        ]

        for label, message, color in quick_phrases:

            button = tk.Button(
                quick_frame,
                text=label,
                font=("Arial", 15, "bold"),
                bg=color,
                fg=self.white,
                activebackground="#FFFFFF",
                activeforeground="#111111",
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                command=lambda text=message:
                    self._on_quick_phrase(text)
            )

            button.pack(
                side=tk.LEFT,
                fill=tk.BOTH,
                expand=True,
                padx=5,
                ipady=12
            )

            self._add_hover(
                button,
                color
            )

        # ---------------- KEYBOARD PANEL ----------------

        keyboard_panel = tk.Frame(
            main,
            bg=self.panel,
            highlightbackground="#19345B",
            highlightthickness=2
        )

        keyboard_panel.pack(
            fill=tk.BOTH,
            expand=True,
            pady=(0, 15)
        )

        self.keys_frame = keyboard_panel

        # Keyboard layout

        self.layout = [

            [
                "1", "2", "3", "4", "5",
                "6", "7", "8", "9", "0"
            ],

            [
                "Q", "W", "E", "R", "T",
                "Y", "U", "I", "O", "P"
            ],

            [
                "A", "S", "D", "F", "G",
                "H", "J", "K", "L"
            ],

            [
                "Z", "X", "C", "V", "B",
                "N", "M"
            ]
        ]

        self._build_keyboard()

        # ---------------- STATUS BAR ----------------

        status = tk.Frame(
            main,
            bg=self.bg
        )

        status.pack(
            fill=tk.X
        )

        status_label = tk.Label(
            status,
            text="●  GazeMate Ready",
            font=("Arial", 11),
            fg="#56D6A1",
            bg=self.bg
        )

        status_label.pack(
            side=tk.LEFT
        )

        version = tk.Label(
            status,
            text="Eye-Gaze Assistive Keyboard",
            font=("Arial", 10),
            fg="#6685A8",
            bg=self.bg
        )

        version.pack(
            side=tk.RIGHT
        )

    # ======================================================
    # BUILD KEYBOARD
    # ======================================================

    def _build_keyboard(self):

        for row_number, row in enumerate(self.layout):

            row_frame = tk.Frame(
                self.keys_frame,
                bg=self.panel
            )

            row_frame.pack(
                fill=tk.BOTH,
                expand=True,
                padx=20,
                pady=4
            )

            for char in row:

                button = tk.Button(
                    row_frame,
                    text=char,
                    font=("Arial", self.font_size, "bold"),
                    bg=self.key,
                    fg=self.white,
                    activebackground=self.key_hover,
                    activeforeground=self.white,
                    relief=tk.FLAT,
                    bd=0,
                    cursor="hand2",
                    command=lambda c=char:
                        self._on_key_click(c)
                )

                button.pack(
                    side=tk.LEFT,
                    fill=tk.BOTH,
                    expand=True,
                    padx=4,
                    pady=2
                )

                self.letter_buttons.append(
                    button
                )

                self._add_hover(
                    button,
                    self.key
                )

        # ---------------- ACTION BUTTONS ----------------

        action_frame = tk.Frame(
            self.keys_frame,
            bg=self.panel
        )

        action_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=(8, 12)
        )

        actions = [

            (
                "SPACE",
                self._on_space,
                "#4D45D8"
            ),

            (
                "←  BACK",
                self._on_backspace,
                "#E84F83"
            ),

            (
                "CLEAR",
                self._on_clear,
                "#F2A63B"
            ),

            (
                "🔊  SPEAK ALL",
                self._on_speak,
                "#35C99A"
            )
        ]

        for text, command, color in actions:

            button = tk.Button(
                action_frame,
                text=text,
                font=("Arial", 14, "bold"),
                bg=color,
                fg=self.white,
                activebackground="#FFFFFF",
                activeforeground="#111111",
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                command=command
            )

            button.pack(
                side=tk.LEFT,
                fill=tk.BOTH,
                expand=True,
                padx=5,
                ipady=10
            )

            self._add_hover(
                button,
                color
            )

    # ======================================================
    # HOVER EFFECT
    # ======================================================

    def _add_hover(self, button, original_color):

        def enter(event):

            button.configure(
                relief=tk.RAISED,
                bd=2
            )

        def leave(event):

            button.configure(
                relief=tk.FLAT,
                bd=0
            )

        button.bind(
            "<Enter>",
            enter
        )

        button.bind(
            "<Leave>",
            leave
        )

    # ======================================================
    # PLACEHOLDER
    # ======================================================

    def _remove_placeholder(self, event=None):

        current = self.text_display.get(
            "1.0",
            tk.END
        ).strip()

        if current == "Your message will appear here...":

            self.text_display.delete(
                "1.0",
                tk.END
            )

            self.text_display.config(
                fg=self.white
            )

    # ======================================================
    # KEY FUNCTIONS
    # ======================================================

    def _on_key_click(self, char):

        self._remove_placeholder()

        self.text_display.insert(
            tk.END,
            char
        )

        self.text_display.see(
            tk.END
        )

    def _on_space(self):

        self._remove_placeholder()

        self.text_display.insert(
            tk.END,
            " "
        )

        self.text_display.see(
            tk.END
        )

    def _on_backspace(self):

        current_text = self.text_display.get(
            "1.0",
            tk.END
        ).rstrip("\n")

        if current_text:

            self.text_display.delete(
                "end-2c",
                tk.END
            )

    def _on_clear(self):

        self.text_display.delete(
            "1.0",
            tk.END
        )

    # ======================================================
    # QUICK PHRASES
    # ======================================================

    def _on_quick_phrase(self, text):

        self.text_display.delete(
            "1.0",
            tk.END
        )

        self.text_display.config(
            fg=self.white
        )

        self.text_display.insert(
            tk.END,
            text
        )

        speak_text(text)

    # ======================================================
    # SPEAK
    # ======================================================

    def _on_speak(self):

        text = self.text_display.get(
            "1.0",
            tk.END
        ).strip()

        if (
            text
            and text != "Your message will appear here..."
        ):

            speak_text(text)


# ==========================================================
# RUN
# ==========================================================

if __name__ == "__main__":

    app = AccessibleVirtualKeyboard()

    app.mainloop()