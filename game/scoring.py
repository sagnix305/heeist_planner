# game/scoring.py


class Scoring:

    def __init__(self):

        self.score = 0
        self.attempts = 3

    def add_mission_success_score(self):

        points_earned = 100

        self.score += points_earned

        return points_earned

    def deduct_hint_score(self):

        hint_cost = 25
        points_deducted = min(
            hint_cost,
            self.score
        )

        self.score = max(
            0,
            self.score - hint_cost
        )

        return points_deducted

    def lose_attempt(self):

        if self.attempts > 0:

            self.attempts -= 1

        return self.attempts

    def get_score(self):

        return self.score

    def get_attempts(self):

        return self.attempts

    def has_attempts_left(self):

        return self.attempts > 0

    def reset(self):

        self.score = 0
        self.attempts = 3