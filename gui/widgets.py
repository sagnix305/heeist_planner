import tkinter as tk


def create_button(parent, text, command, width=20):
    button = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 12, "bold"),
        width=width,
        padx=10,
        pady=8,
        cursor="hand2"
    )

    return button


def create_title(parent, text):
    label = tk.Label(
        parent,
        text=text,
        font=("Arial", 24, "bold"),
        pady=10
    )

    return label


def create_character_card(parent, name, role):
    frame = tk.Frame(
        parent,
        bd=2,
        relief="groove",
        padx=15,
        pady=10
    )

    name_label = tk.Label(
        frame,
        text=name,
        font=("Arial", 12, "bold")
    )

    role_label = tk.Label(
        frame,
        text=role,
        font=("Arial", 10)
    )

    name_label.pack()
    role_label.pack()

    return frame