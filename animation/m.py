import tkinter as tk
from datetime import datetime


class ModernClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Digital Clock")
        self.root.geometry("600x350")
        self.root.resizable(False, False)

        # Center window
        self.center_window()

        # Colors (modern dark theme)
        self.bg = "#0b1220"
        self.card = "#111b2e"
        self.text = "#38bdf8"
        self.subtext = "#94a3b8"

        self.root.configure(bg=self.bg)

        # Main title
        self.title = tk.Label(
            root,
            text="DIGITAL CLOCK",
            font=("Segoe UI", 18, "bold"),
            bg=self.bg,
            fg="white"
        )
        self.title.pack(pady=20)

        # Card frame (like image design)
        self.card_frame = tk.Frame(
            root,
            bg=self.card,
            width=450,
            height=180
        )
        self.card_frame.pack(pady=10)
        self.card_frame.pack_propagate(False)

        # Time label (big digital style)
        self.time_label = tk.Label(
            self.card_frame,
            text="00:00:00",
            font=("Consolas", 48, "bold"),
            bg=self.card,
            fg=self.text
        )
        self.time_label.pack(expand=True)

        # AM/PM label
        self.ampm_label = tk.Label(
            self.card_frame,
            text="",
            font=("Segoe UI", 14, "bold"),
            bg=self.card,
            fg=self.subtext
        )
        self.ampm_label.pack()

        # Date label
        self.date_label = tk.Label(
            root,
            text="",
            font=("Segoe UI", 12),
            bg=self.bg,
            fg=self.subtext
        )
        self.date_label.pack(pady=15)

        self.update_clock()

    def center_window(self):
        self.root.update_idletasks()
        w, h = 600, 350
        x = (self.root.winfo_screenwidth() // 2) - (w // 2)
        y = (self.root.winfo_screenheight() // 2) - (h // 2)
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def update_clock(self):
        now = datetime.now()

        # Time (12-hour format like modern UI)
        time_str = now.strftime("%I:%M:%S")
        ampm = now.strftime("%p")

        # Clean leading zero
        time_str = time_str.lstrip("0")

        # Date
        date_str = now.strftime("%A, %d %B %Y")

        self.time_label.config(text=time_str)
        self.ampm_label.config(text=ampm)
        self.date_label.config(text=date_str)

        self.root.after(1000, self.update_clock)


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernClock(root)
    root.mainloop()