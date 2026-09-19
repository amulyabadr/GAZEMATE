import tkinter as tk

from integrated_text_speech import speak_text


class AccessibleVirtualKeyboard(tk.Tk):

    def __init__(self):

        super().__init__()

        self.title(
            "GazeMate - Basic Keyboard"
        )

        self.geometry(
            "1000x650"
        )

        self.minsize(
            800,
            550
        )

        self.configure(
            bg="white"
        )

        self.font_size = 16

        self.bg = "white"
        self.panel = "white"
        self.key = "lightgray"
        self.key_hover = "gray"
        self.text_color = "black"

        # ---------------- TEXT DISPLAY ----------------

        self.text_display = tk.Text(
            self,
            height=3,
            font=("Arial", 20),
            bg="white",
            fg="black",
            wrap=tk.WORD,
            relief=tk.SOLID,
            bd=1
        )

        self.text_display.pack(
            fill=tk.X,
            padx=20,
            pady=20
        )

        # ---------------- QUICK PHRASES ----------------

        quick_frame = tk.Frame(
            self,
            bg="white"
        )

        quick_frame.pack(
            fill=tk.X,
            padx=20,
            pady=5
        )

        quick_phrases = [
            ("HELP", "I need help."),
            ("WATER", "I need water."),
            ("PAIN", "I am in pain."),
            ("YES", "Yes."),
            ("NO", "No.")
        ]

        for label, message in quick_phrases:

            button = tk.Button(
                quick_frame,
                text=label,
                font=("Arial", 12),
                bg="lightgray",
                fg="black",
                relief=tk.RAISED,
                bd=1,
                command=lambda text=message:
                    self._on_quick_phrase(text)
            )

            button.pack(
                side=tk.LEFT,
                fill=tk.BOTH,
                expand=True,
                padx=3,
                ipady=5
            )

        # ---------------- KEYBOARD ----------------

        self.keys_frame = tk.Frame(
            self,
            bg="white"
        )

        self.keys_frame.pack(
            fill=tk.BOTH,
            expand=True,
            padx=20,
            pady=10
        )

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

    # ======================================================
    # BUILD KEYBOARD
    # ======================================================

    def _build_keyboard(self):

        for row in self.layout:

            row_frame = tk.Frame(
                self.keys_frame,
                bg="white"
            )

            row_frame.pack(
                fill=tk.BOTH,
                expand=True,
                pady=3
            )

            for char in row:

                button = tk.Button(
                    row_frame,
                    text=char,
                    font=("Arial", self.font_size),
                    bg="lightgray",
                    fg="black",
                    activebackground="gray",
                    activeforeground="white",
                    relief=tk.RAISED,
                    bd=1,
                    command=lambda c=char:
                        self._on_key_click(c)
                )

                button.pack(
                    side=tk.LEFT,
                    fill=tk.BOTH,
                    expand=True,
                    padx=2,
                    pady=2
                )

        # ---------------- ACTION BUTTONS ----------------

        action_frame = tk.Frame(
            self.keys_frame,
            bg="white"
        )

        action_frame.pack(
            fill=tk.X,
            pady=5
        )

        actions = [

            ("SPACE", self._on_space),
            ("BACK", self._on_backspace),
            ("CLEAR", self._on_clear),
            ("SPEAK", self._on_speak)
        ]

        for text, command in actions:

            button = tk.Button(
                action_frame,
                text=text,
                font=("Arial", 12),
                bg="lightgray",
                fg="black",
                relief=tk.RAISED,
                bd=1,
                command=command
            )

            button.pack(
                side=tk.LEFT,
                fill=tk.BOTH,
                expand=True,
                padx=3,
                ipady=7
            )

    # ======================================================
    # KEY FUNCTIONS
    # ======================================================

    def _on_key_click(self, char):

        self.text_display.insert(
            tk.END,
            char
        )

        self.text_display.see(
            tk.END
        )

    def _on_space(self):

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

        if text:

            speak_text(text)


if __name__ == "__main__":

    app = AccessibleVirtualKeyboard()

    app.mainloop()