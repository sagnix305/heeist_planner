# gui/game_screen.py

import tkinter as tk
from tkinter import ttk, messagebox

from csp.solver import (
    get_level_configuration,
    validate_player_plan
)
from game.game_manager import GameManager


class GameScreen:

    def __init__(self, root):

        self.root = root

        if not hasattr(self.root, "game_manager"):

            self.root.game_manager = GameManager()

        self.game_manager = self.root.game_manager
        self.assignment_boxes = {}
        self.timer_after_id = None
        self.hint_used = False

        self.create_game_screen()

        self.root.bind_all(
            "<MouseWheel>",
            self.on_mouse_wheel
        )

    def create_game_screen(self):

        self.stop_timer_updates()

        self.assignment_boxes = {}
        self.mission_completed = False
        self.hint_used = False

        for widget in self.root.winfo_children():

            widget.destroy()

        self.canvas = tk.Canvas(
            self.root,
            bg="#eaf0f5",
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            self.root,
            orient="vertical",
            command=self.canvas.yview
        )

        self.canvas.configure(
            yscrollcommand=scrollbar.set
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        self.scrollable_frame = tk.Frame(
            self.canvas,
            bg="#eaf0f5"
        )

        self.canvas_window = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.scrollable_frame.bind(
            "<Configure>",
            self.update_scroll_region
        )

        self.canvas.bind(
            "<Configure>",
            self.resize_scrollable_frame
        )

        self.create_game_content()

    def update_scroll_region(self, event=None):

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def resize_scrollable_frame(self, event):

        self.canvas.itemconfig(
            self.canvas_window,
            width=event.width
        )

    def on_mouse_wheel(self, event):

        self.canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    # =====================================================
    # TIMER
    # =====================================================

    def start_timer_updates(self):

        self.game_manager.start_timer()

        self.update_timer_label()

        self.timer_after_id = self.root.after(
            1000,
            self.tick_timer
        )

    def stop_timer_updates(self):

        self.game_manager.stop_timer()

        if self.timer_after_id is not None:

            try:

                self.root.after_cancel(
                    self.timer_after_id
                )

            except tk.TclError:

                pass

            self.timer_after_id = None

    def tick_timer(self):

        self.game_manager.update_timer()

        self.update_timer_label()

        if self.game_manager.is_time_up():

            self.check_plan_button.config(
                state="disabled"
            )

            self.next_level_button.config(
                state="disabled"
            )

            self.hint_button.config(
                state="disabled"
            )

            messagebox.showerror(
                "Time Up",
                "The mission timer reached zero.\n\n"
                "Click RESTART GAME to try again."
            )

            return

        self.timer_after_id = self.root.after(
            1000,
            self.tick_timer
        )

    def update_timer_label(self):

        self.timer_label.config(
            text=(
                "TIME: "
                + self.game_manager.get_time()
            )
        )

    # =====================================================
    # GAME CONTENT
    # =====================================================

    def create_game_content(self):

        level_id = self.game_manager.get_current_level_id()

        self.level_data = get_level_configuration(
            level_id
        )

        if self.level_data is None:

            messagebox.showerror(
                "Mission Error",
                "Rules for this mission could not be loaded."
            )

            return

        main_frame = tk.Frame(
            self.scrollable_frame,
            bg="#eaf0f5",
            padx=25,
            pady=25
        )

        main_frame.pack(
            fill="both",
            expand=True
        )

        # =================================================
        # HEADER
        # =================================================

        header = tk.Frame(
            main_frame,
            bg="#172033",
            padx=20,
            pady=16
        )

        header.pack(
            fill="x",
            pady=(0, 18)
        )

        tk.Label(
            header,
            text="HEIST PLANNER",
            font=("Arial", 22, "bold"),
            fg="white",
            bg="#172033"
        ).pack(side="left")

        tk.Label(
            header,
            text=self.game_manager.get_current_mission_title(),
            font=("Arial", 14, "bold"),
            fg="#ffd166",
            bg="#172033"
        ).pack(side="right")

        self.attempts_label = tk.Label(
            header,
            text=(
                "ATTEMPTS: "
                + str(self.game_manager.get_attempts())
            ),
            font=("Arial", 11, "bold"),
            fg="#fca5a5",
            bg="#172033"
        )

        self.attempts_label.pack(
            side="right",
            padx=15
        )

        self.timer_label = tk.Label(
            header,
            text=(
                "TIME: "
                + self.game_manager.get_time()
            ),
            font=("Arial", 11, "bold"),
            fg="#93c5fd",
            bg="#172033"
        )

        self.timer_label.pack(
            side="right",
            padx=15
        )

        self.score_label = tk.Label(
            header,
            text=(
                "SCORE: "
                + str(self.game_manager.get_score())
            ),
            font=("Arial", 11, "bold"),
            fg="#86efac",
            bg="#172033"
        )

        self.score_label.pack(
            side="right",
            padx=15
        )

        # =================================================
        # MISSION DETAILS
        # =================================================

        mission_frame = tk.LabelFrame(
            main_frame,
            text="CURRENT MISSION",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=15,
            pady=12
        )

        mission_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        tk.Label(
            mission_frame,
            text=self.game_manager.get_current_mission_name(),
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#172033"
        ).pack(anchor="w")

        tk.Label(
            mission_frame,
            text=self.game_manager.get_current_mission_description(),
            font=("Arial", 12),
            bg="white",
            wraplength=900,
            justify="left"
        ).pack(
            anchor="w",
            pady=(8, 5)
        )

        tk.Label(
            mission_frame,
            text=(
                "Difficulty: "
                + self.game_manager.get_current_mission_difficulty()
            ),
            font=("Arial", 11, "bold"),
            bg="white",
            fg="#c2410c"
        ).pack(anchor="w")

        # =================================================
        # OPERATION MAP
        # =================================================

        map_frame = tk.LabelFrame(
            main_frame,
            text="OPERATION MAP",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=10,
            pady=10
        )

        map_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        self.create_mission_map(map_frame)

        # =================================================
        # MISSION RULES
        # =================================================

        rules_frame = tk.LabelFrame(
            main_frame,
            text="MISSION RULES",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=15,
            pady=10
        )

        rules_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        rules_text = ""

        for number, rule in enumerate(
            self.level_data["rules"],
            start=1
        ):

            rules_text += (
                str(number)
                + ". "
                + rule
                + "\n"
            )

        tk.Label(
            rules_frame,
            text=rules_text,
            font=("Arial", 11),
            bg="white",
            justify="left",
            anchor="w"
        ).pack(anchor="w")

        # =================================================
        # TEAM
        # =================================================

        team_frame = tk.LabelFrame(
            main_frame,
            text="YOUR HEIST TEAM",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=15,
            pady=12
        )

        team_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        for column, member in enumerate(
            self.level_data["team_members"]
        ):

            member_card = tk.Label(
                team_frame,
                text=member,
                font=("Arial", 11, "bold"),
                bg="#dbeafe",
                fg="#172033",
                padx=12,
                pady=9,
                bd=1,
                relief="solid"
            )

            member_card.grid(
                row=0,
                column=column,
                padx=5,
                pady=5
            )

        # =================================================
        # ASSIGNMENTS
        # =================================================

        assignment_frame = tk.LabelFrame(
            main_frame,
            text="ASSIGN TEAM MEMBERS",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=15
        )

        assignment_frame.pack(
            fill="x",
            pady=(0, 15)
        )

        for row, task in enumerate(
            self.level_data["tasks"]
        ):

            tk.Label(
                assignment_frame,
                text=task + ":",
                font=("Arial", 12, "bold"),
                bg="white",
                width=20,
                anchor="w"
            ).grid(
                row=row,
                column=0,
                padx=10,
                pady=8,
                sticky="w"
            )

            assignment_box = ttk.Combobox(
                assignment_frame,
                values=self.level_data["team_members"],
                state="readonly",
                width=28
            )

            assignment_box.grid(
                row=row,
                column=1,
                padx=10,
                pady=8,
                sticky="w"
            )

            assignment_box.set("Choose team member")

            self.assignment_boxes[task] = assignment_box

        # =================================================
        # BUTTONS
        # =================================================

        button_frame = tk.Frame(
            main_frame,
            bg="#eaf0f5"
        )

        button_frame.pack(
            pady=(5, 20)
        )

        self.check_plan_button = tk.Button(
            button_frame,
            text="CHECK PLAN",
            font=("Arial", 12, "bold"),
            bg="#2563eb",
            fg="white",
            activebackground="#1d4ed8",
            activeforeground="white",
            width=18,
            padx=5,
            pady=8,
            command=self.check_plan
        )

        self.check_plan_button.grid(
            row=0,
            column=0,
            padx=10,
            pady=5
        )

        self.hint_button = tk.Button(
            button_frame,
            text="HINT (-25)",
            font=("Arial", 12, "bold"),
            bg="#ca8a04",
            fg="white",
            activebackground="#a16207",
            activeforeground="white",
            width=18,
            padx=5,
            pady=8,
            command=self.give_hint
        )

        self.hint_button.grid(
            row=0,
            column=1,
            padx=10,
            pady=5
        )

        self.next_level_button = tk.Button(
            button_frame,
            text="NEXT MISSION",
            font=("Arial", 12, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            width=18,
            padx=5,
            pady=8,
            state="disabled",
            command=self.go_to_next_mission
        )

        self.next_level_button.grid(
            row=0,
            column=2,
            padx=10,
            pady=5
        )

        tk.Button(
            button_frame,
            text="RESTART GAME",
            font=("Arial", 12, "bold"),
            bg="#dc2626",
            fg="white",
            activebackground="#b91c1c",
            activeforeground="white",
            width=18,
            padx=5,
            pady=8,
            command=self.restart_game
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=5
        )

        tk.Button(
            button_frame,
            text="BACK TO MENU",
            font=("Arial", 12, "bold"),
            bg="#475569",
            fg="white",
            activebackground="#334155",
            activeforeground="white",
            width=18,
            padx=5,
            pady=8,
            command=self.back_to_menu
        ).grid(
            row=1,
            column=1,
            padx=10,
            pady=5
        )

        self.start_timer_updates()

    def create_mission_map(self, parent):

        map_canvas = tk.Canvas(
            parent,
            width=900,
            height=280,
            bg="#172033",
            highlightthickness=0
        )

        map_canvas.pack(
            fill="x",
            expand=True
        )

        tasks = self.level_data["tasks"]

        map_canvas.create_text(
            450,
            24,
            text="MISSION ROUTE",
            font=("Arial", 13, "bold"),
            fill="#ffd166"
        )

        map_canvas.create_line(
            165, 105,
            350, 105,
            fill="#94a3b8",
            width=4
        )

        map_canvas.create_line(
            520, 105,
            705, 105,
            fill="#94a3b8",
            width=4
        )

        map_canvas.create_line(
            350, 105,
            350, 205,
            fill="#94a3b8",
            width=4
        )

        map_canvas.create_line(
            520, 105,
            520, 205,
            fill="#94a3b8",
            width=4
        )

        map_canvas.create_line(
            350, 205,
            520, 205,
            fill="#94a3b8",
            width=4
        )

        locations = [
            (75, 70, 255, 140, tasks[0], "#2563eb"),
            (350, 70, 530, 140, tasks[1], "#9333ea"),
            (625, 70, 805, 140, tasks[2], "#dc2626"),
            (260, 170, 440, 240, tasks[3], "#16a34a"),
            (455, 170, 635, 240, tasks[4], "#ea580c")
        ]

        for x1, y1, x2, y2, label, color in locations:

            map_canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=color,
                outline="#f8fafc",
                width=2
            )

            map_canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=label,
                font=("Arial", 11, "bold"),
                fill="white",
                width=145
            )

        map_canvas.create_text(
            450,
            260,
            text=(
                "Plan the route. Assign the right specialist "
                "to each location."
            ),
            font=("Arial", 10, "italic"),
            fill="#cbd5e1"
        )

    def update_game_status(self):

        self.score_label.config(
            text=(
                "SCORE: "
                + str(self.game_manager.get_score())
            )
        )

        self.attempts_label.config(
            text=(
                "ATTEMPTS: "
                + str(self.game_manager.get_attempts())
            )
        )

    def give_hint(self):

        if self.mission_completed:

            messagebox.showinfo(
                "Mission Complete",
                "This mission is already complete."
            )

            return

        if self.game_manager.is_time_up():

            messagebox.showwarning(
                "Time Up",
                "The timer has reached zero. Click RESTART GAME."
            )

            return

        if not self.game_manager.has_attempts_left():

            messagebox.showwarning(
                "No Attempts Left",
                "Click RESTART GAME to begin again."
            )

            return

        if self.hint_used:

            messagebox.showinfo(
                "Hint Already Used",
                "You have already used the hint for this mission."
            )

            return

        allowed_assignments = self.level_data[
            "allowed_assignments"
        ]

        for task in self.level_data["tasks"]:

            assignment_box = self.assignment_boxes[task]

            if assignment_box.get() == "Choose team member":

                valid_member = allowed_assignments[task][0]

                assignment_box.set(valid_member)

                self.hint_used = True

                points_deducted = self.game_manager.use_hint()

                self.update_game_status()

                self.hint_button.config(
                    state="disabled"
                )

                messagebox.showinfo(
                    "Hint Used",
                    "Hint: assign "
                    + valid_member
                    + " to "
                    + task
                    + ".\n\n"
                    + str(points_deducted)
                    + " points deducted."
                )

                return

        messagebox.showinfo(
            "No Hint Needed",
            "Every task already has an assignment."
        )

    def check_plan(self):

        if self.mission_completed:

            messagebox.showinfo(
                "Mission Complete",
                "This mission is already complete. Click NEXT MISSION."
            )

            return

        if not self.game_manager.has_attempts_left():

            messagebox.showwarning(
                "No Attempts Left",
                "Click RESTART GAME to begin again."
            )

            return

        player_plan = {}

        for task, assignment_box in self.assignment_boxes.items():

            selected_member = assignment_box.get()

            if selected_member == "Choose team member":

                messagebox.showwarning(
                    "Incomplete Plan",
                    "Please assign a team member to every task."
                )

                return

            player_plan[task] = selected_member

        is_valid, result_message = validate_player_plan(
            player_plan,
            self.game_manager.get_current_level_id()
        )

        if is_valid:

            self.mission_completed = True

            self.hint_button.config(
                state="disabled"
            )

            self.stop_timer_updates()

            points_earned = self.game_manager.record_success()

            self.update_game_status()

            result_message += (
                "\n\nYou earned "
                + str(points_earned)
                + " points."
            )

            if self.game_manager.has_next_level():

                self.next_level_button.config(
                    state="normal"
                )

                result_message += (
                    "\n\nClick NEXT MISSION to continue."
                )

            else:

                result_message += (
                    "\n\nYou completed the final mission!"
                )

            messagebox.showinfo(
                "Mission Successful",
                result_message
            )

        else:

            attempts_left = self.game_manager.record_failed_attempt()

            self.update_game_status()

            if attempts_left == 0:

                self.check_plan_button.config(
                    state="disabled"
                )

                self.hint_button.config(
                    state="disabled"
                )

                self.stop_timer_updates()

                result_message += (
                    "\n\nNo attempts remain."
                    "\nClick RESTART GAME to begin again."
                )

            else:

                result_message += (
                    "\n\nAttempts remaining: "
                    + str(attempts_left)
                )

            messagebox.showerror(
                "Plan Invalid",
                result_message
            )

    def go_to_next_mission(self):

        if self.game_manager.complete_current_level():

            messagebox.showinfo(
                "Next Mission",
                "The next mission is ready."
            )

            self.create_game_screen()

            self.canvas.yview_moveto(0)

        else:

            messagebox.showinfo(
                "Game Complete",
                "You have completed every mission!"
            )

    def restart_game(self):

        self.game_manager.start_new_game()

        self.create_game_screen()

        self.canvas.yview_moveto(0)

    def back_to_menu(self):

        self.stop_timer_updates()

        self.root.unbind_all("<MouseWheel>")

        from gui.main_menu import MainMenu

        MainMenu(self.root)