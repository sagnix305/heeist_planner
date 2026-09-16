import tkinter as tk

from gui.widgets import create_button, create_title


class MainMenu:

    def __init__(self, root):

        self.root = root

        self.root.title("Heist Planner")
        self.root.geometry("1000x700")
        self.root.minsize(900, 600)
        self.root.resizable(True, True)

        self.create_menu()

    def create_menu(self):

        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container
        main_frame = tk.Frame(self.root)

        main_frame.pack(
            expand=True,
            fill="both"
        )

        # Game title
        title = create_title(
            main_frame,
            "💎 HEIST PLANNER"
        )

        title.pack(pady=(120, 10))

        # Subtitle
        subtitle = tk.Label(
            main_frame,
            text="Plan the perfect heist",
            font=("Arial", 14)
        )

        subtitle.pack(pady=10)

        # Start button
        start_button = create_button(
            main_frame,
            "START GAME",
            self.start_game,
            width=20
        )

        start_button.pack(pady=15)

        # How to play button
        help_button = create_button(
            main_frame,
            "HOW TO PLAY",
            self.show_help,
            width=20
        )

        help_button.pack(pady=10)

        # Exit button
        exit_button = create_button(
            main_frame,
            "EXIT",
            self.root.destroy,
            width=20
        )

        exit_button.pack(pady=10)

    def start_game(self):

        from gui.game_screen import GameScreen

        GameScreen(self.root)

    def show_help(self):

        help_window = tk.Toplevel(self.root)

        help_window.title("How to Play")

        help_window.geometry("600x400")

        instructions = """
HOW TO PLAY

You are the leader of a heist team.

Your goal is to assign the correct team
members to different tasks.

Every mission contains several constraints.

You must satisfy ALL constraints
to successfully complete the heist.

Choose your assignments and click
CHECK PLAN.

Good luck!
"""

        label = tk.Label(
            help_window,
            text=instructions,
            font=("Arial", 12),
            justify="left",
            padx=20,
            pady=20
        )

        label.pack()