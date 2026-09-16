# main.py

import tkinter as tk

from gui.main_menu import MainMenu
from game.game_manager import GameManager


def main():

    root = tk.Tk()

    root.title("Heist Planner")
    root.geometry("1100x700")
    root.minsize(900, 600)

    # One shared manager for the entire game.
    # Later, GameScreen will use this to display
    # the active mission and move to the next one.
    root.game_manager = GameManager()

    MainMenu(root)

    root.mainloop()


if __name__ == "__main__":
    main()