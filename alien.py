import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, ai_game):
        """Inicializamos el alien y lo situamos en su posición inicial"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        # Guardamos la posición horizontal exacta del alien
        self.x = float(self.rect.x)

    def check_edges(self):
        """Devuelve True si la parte derecha de nuestro rectangle (rect) es mayor o igual que la parte derecha
        del borde la pantalla o si su parte izquierda es menor o igual a 0 (parte izquierda de la pantalla"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Movemos los aliens hacia la derecha"""
        self.x += self.settings.alien_speed * self.settings.fleet_direction
        self.rect.x = self.x