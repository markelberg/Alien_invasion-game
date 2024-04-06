import sys
import pygame

from settings import Settings
from space_ship import SpaceShip
from bullets import Bullets
from alien import Alien


class AlienInvasion:
    """Clase general para la gestión de los recursos y el comportamiento del juego"""
    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("ALIEN INVASION")

        self.space_ship = SpaceShip(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

    def run_game(self):
        """Bucle principal del juego"""
        while True:
            self._check_events()
            self.space_ship.update()
            self._update_bullets()
            self._update_aliens()
            self._update_screen()

    def _check_events(self):
        """Gestión de pulsaciones (eventos) de teclas y ratón"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.space_ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.space_ship.moving_left = True
        elif event.key == pygame.K_DOWN:
            self.space_ship.moving_down = True
        elif event.key == pygame.K_UP:
            self.space_ship.moving_up = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE or pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.space_ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.space_ship.moving_left = False
        elif event.key == pygame.K_DOWN:
            self.space_ship.moving_down = False
        elif event.key == pygame.K_UP:
            self.space_ship.moving_up = False

    def _create_fleet(self):
        """Creamos la flota usando la clase Alien"""
        # Calculamos el espacio necesario para situar los aliens en los ejes x e y.
        alien = Alien(self)
        available_space_x = self.settings.screen_width - (2 * alien.rect.width)
        number_of_aliens = available_space_x // (2 * alien.rect.width)

        available_space_y = (self.settings.screen_height - (3 * alien.rect.height) - self.space_ship.rect.height)
        rows_of_aliens = available_space_y // (2 * alien.rect.height)

        # Dos bucles anidados: el exterior cuenta las filas que queremos desde 0 y el interior crea los aliens de cada fila.
        for row_number in range(rows_of_aliens):
            for alien_number in range(number_of_aliens):
                self._create_alien(alien_number, row_number)
    def _create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        # Bajamos una fila la flota y cambiamos su dirección
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _fire_bullet(self):
        """Creamos una nueva bala y la añadimos al rersto"""
        new_bullet = Bullets(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        # Borramos las balas que han desaparecido para que no sigan consumiendo memoria
        for bullets in self.bullets.copy():
            if bullets.rect.bottom <= 0:
                self.bullets.remove(bullets)
        # Comprobamos si una bala a chocado con un alien y si es así, ambas desaparecen
        pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

    def _update_screen(self):
        """Actualiza la pantalla en cada iteración"""
        self.screen.fill(self.settings.bg_color)
        self.space_ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullets()  # Llamamos al metodo draw_bullet de bullets.py
        self.aliens.draw(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()