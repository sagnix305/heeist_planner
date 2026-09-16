# game/level_manager.py

import json
import os


class LevelManager:

    def __init__(self):

        self.current_level_index = 0
        self.levels = self.load_levels()

    # =====================================================
    # LOAD LEVELS
    # =====================================================

    def load_levels(self):

        project_root = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

        levels_file = os.path.join(
            project_root,
            "data",
            "levels.json"
        )

        try:

            with open(
                levels_file,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            return data["levels"]

        except FileNotFoundError:

            print("ERROR: levels.json was not found.")
            return []

        except json.JSONDecodeError:

            print("ERROR: levels.json contains invalid JSON.")
            return []

        except KeyError:

            print("ERROR: levels.json must contain a 'levels' list.")
            return []

    # =====================================================
    # GET CURRENT LEVEL
    # =====================================================

    def get_current_level(self):

        if not self.levels:

            return None

        return self.levels[
            self.current_level_index
        ]

    # =====================================================
    # GET CURRENT LEVEL ID
    # =====================================================

    def get_current_level_id(self):

        level = self.get_current_level()

        if level is None:

            return None

        return level["id"]

    # This extra method keeps compatibility with earlier code.
    def get_current_level_number(self):

        return self.get_current_level_id()

    # =====================================================
    # GET CURRENT LEVEL DETAILS
    # =====================================================

    def get_current_level_name(self):

        level = self.get_current_level()

        if level is None:

            return None

        return level["name"]

    def get_current_level_description(self):

        level = self.get_current_level()

        if level is None:

            return None

        return level["description"]

    def get_current_level_difficulty(self):

        level = self.get_current_level()

        if level is None:

            return None

        return level["difficulty"]

    # =====================================================
    # MOVE TO NEXT LEVEL
    # =====================================================

    def next_level(self):

        if not self.levels:

            return False

        if self.current_level_index < len(self.levels) - 1:

            self.current_level_index += 1
            return True

        return False

    # This extra method keeps compatibility with earlier code.
    def move_to_next_level(self):

        return self.next_level()

    # =====================================================
    # CHECK FOR NEXT LEVEL
    # =====================================================

    def has_next_level(self):

        if not self.levels:

            return False

        return (
            self.current_level_index
            < len(self.levels) - 1
        )

    # =====================================================
    # RESET LEVELS
    # =====================================================

    def reset(self):

        self.current_level_index = 0

    # This extra method keeps compatibility with earlier code.
    def reset_levels(self):

        self.reset()

    # =====================================================
    # GET TOTAL LEVELS
    # =====================================================

    def get_total_levels(self):

        return len(self.levels)