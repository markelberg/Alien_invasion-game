import pygame.font
from pygame.sprite import Group
from space_ship import SpaceShip

class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.high_score = 0
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        self.space_ships_left = self.settings.space_ship_limit
        self.score = 0
        self.level = 1


class Scoreboard:
    """Clase para crear nuestra puntuación"""
    def __init__(self, ai_game):
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)


        self.prep_score()
        self.prep_high_score()
        self.prep_level()

    def prep_score(self):
        # Casteamos el score a str y lo renderizamos en una imagen que se muestra en la esquina superior derecha
        score_str = str(self.stats.score)
        score_str = 'Score: ' + score_str
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        high_score_str = str(self.stats.high_score)
        high_score_str = 'High Score: ' + high_score_str
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def check_high_score(self):
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)

    def prep_level(self):
        level_str = str(self.stats.level)
        level_str = 'Level: ' + level_str
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 40
