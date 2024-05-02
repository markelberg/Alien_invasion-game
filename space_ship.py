import pygame

class SpaceShip:
    def __init__(self, ai_game):
        """Inicializamos la nave y configuramos su posición inicial"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Cargamos la imagen de la nave
        self.image = pygame.image.load('images/space_ship.bmp')
        self.rect = self.image.get_rect()

        # Cada nave nueva la colocamos en el centro-inferior de la pantalla
        self.rect.midbottom = self.screen_rect.midbottom

        # Casteo para que el atributo x y rect acepten floats
        self.x = float(self.rect.x)

        # Flag de movimiento
        self.moving_right = False
        self.moving_left = False
        self.moving_down = False
        self.moving_up = False

    def update(self):
        """Actualizamos la posición de la nave en función de la flag de movimiento"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.space_ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.space_ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.rect.y += self.settings.space_ship_speed
        if self.moving_up and self.rect.top > 0:
            self.rect.y -= self.settings.space_ship_speed

        # Actualizamos el objeto rect de self.x
        self.rect.x = self.x

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
