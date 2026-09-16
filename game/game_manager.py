# game/game_manager.py

from game.level_manager import LevelManager
from game.scoring import Scoring
from game.timer import GameTimer


class GameManager:

    def __init__(self):

        self.level_manager = LevelManager()
        self.scoring = Scoring()
        self.timer = GameTimer()

    def start_new_game(self):

        self.level_manager.reset()
        self.scoring.reset()
        self.timer.reset()

    def get_current_level(self):

        return self.level_manager.get_current_level()

    def get_current_level_id(self):

        return self.level_manager.get_current_level_id()

    def get_current_mission_name(self):

        return self.level_manager.get_current_level_name()

    def get_current_mission_description(self):

        return self.level_manager.get_current_level_description()

    def get_current_mission_difficulty(self):

        return self.level_manager.get_current_level_difficulty()

    def get_current_mission_title(self):

        level_id = self.get_current_level_id()
        mission_name = self.get_current_mission_name()

        if level_id is None or mission_name is None:

            return "No Mission Available"

        return f"Mission {level_id}: {mission_name}"

    def get_total_levels(self):

        return self.level_manager.get_total_levels()

    def has_next_level(self):

        return self.level_manager.has_next_level()

    def is_final_level(self):

        return not self.has_next_level()

    def complete_current_level(self):

        moved_to_next_level = self.level_manager.next_level()

        if moved_to_next_level:

            self.timer.reset()

        return moved_to_next_level

    def record_success(self):

        return self.scoring.add_mission_success_score()

    def use_hint(self):

        return self.scoring.deduct_hint_score()

    def record_failed_attempt(self):

        return self.scoring.lose_attempt()

    def get_score(self):

        return self.scoring.get_score()

    def get_attempts(self):

        return self.scoring.get_attempts()

    def has_attempts_left(self):

        return self.scoring.has_attempts_left()

    def start_timer(self):

        self.timer.start()

    def stop_timer(self):

        self.timer.stop()

    def update_timer(self):

        return self.timer.tick()

    def get_time(self):

        return self.timer.get_formatted_time()

    def is_time_up(self):

        return self.timer.is_time_up()