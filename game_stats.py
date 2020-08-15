import json

class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()

        self.game_flag = False
        self.high_score = self._read_high_score()

    def _read_high_score(self):
        high_score_file = self.settings.high_score_file

        with open(high_score_file) as file_object:
            high_score = json.load(file_object)

        return high_score

    def reset_stats(self):
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1