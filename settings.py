class Settings:
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.ship_limit = 3

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullet_allowed = 3

        self.fleet_drop_speed = 10
        self.speedup_scale = 1.1
        self.score_scale = 1.5
    
        self.initialize_file_paths()
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 1.0

        self.fleet_direction = 1

        self.alien_points = 50
    
    def initialize_file_paths(self):
        self.high_score_file = 'high_score.json'
        self.bullet_sound = 'sound_effects/bullet.wav'
        self.collide_sound = 'sound_effects/alien_hit.wav'
        self.game_music = 'sound_effects/alien_game.mp3'

    def medium_game_settings(self):
        self.ship_speed = 2.0
        self.bullet_speed = 2.0
        self.alien_speed = 1.5

        self.alien_points = 80

    def hard_game_settings(self):
        self.ship_speed = 2.5
        self.bullet_speed = 2.5
        self.alien_speed = 2.0

        self.alien_points = 120
    
    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)