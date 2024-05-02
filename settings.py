class Settings:

    def __init__(self):
        # Static settings
        self.screen_width = 1510
        self.screen_height = 780
        self.bg_color = (230, 230, 230)

        self.space_ship_limit = 3

        self.bullets_width = 3
        self.bullets_height = 15
        self.bullets_color = (60, 60, 60)

        self.fleet_drop_speed = 10

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        # Dynamic settings
        self.space_ship_speed = 1.2
        self.bullets_speed = 1.5
        self.alien_speed = 0.5

        self.fleet_direction = 1  # 1: derecha, -1: izquierda

        self.alien_points = 30

    def increase_difficulty(self):
        self.space_ship_speed *= self.speedup_scale
        self.bullets_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
