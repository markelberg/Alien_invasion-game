import pygame
from pygame.sprite import Sprite

class Bullets(Sprite):

    def __init__(self, ai_game):
        """Creamos un objeto para la bala en la posición de la nave"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullets_color

        # Creamos una bala en la posición (0, 0) y luego establecemos su posición en la nave
        self.rect = pygame.Rect(0, 0, self.settings.bullets_width, self.settings.bullets_height)
        self.rect.midtop = ai_game.space_ship.rect.midtop

        # Guardamos la posición de la bala como valor decimal como hicimos con la nave
        self.y = float(self.rect.y)

    def update(self):
        # Movemos la bala hacia arriba
        self.y -= self.settings.bullets_speed
        # Actualizamos su posición
        self.rect.y = self.y

    def draw_bullets(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
