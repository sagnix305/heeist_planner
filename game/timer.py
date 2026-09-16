# game/timer.py


class GameTimer:

    def __init__(self, starting_seconds=180):

        self.starting_seconds = starting_seconds
        self.remaining_seconds = starting_seconds
        self.is_running = False

    def start(self):

        self.is_running = True

    def stop(self):

        self.is_running = False

    def reset(self):

        self.remaining_seconds = self.starting_seconds
        self.is_running = False

    def tick(self):

        if not self.is_running:

            return self.remaining_seconds

        if self.remaining_seconds > 0:

            self.remaining_seconds -= 1

        if self.remaining_seconds == 0:

            self.is_running = False

        return self.remaining_seconds

    def get_remaining_seconds(self):

        return self.remaining_seconds

    def is_time_up(self):

        return self.remaining_seconds == 0

    def get_formatted_time(self):

        minutes = self.remaining_seconds // 60
        seconds = self.remaining_seconds % 60

        return f"{minutes:02d}:{seconds:02d}"