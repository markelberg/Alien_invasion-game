import sys
import pygame

from time import sleep
from settings import Settings
from space_ship import SpaceShip
from bullets import Bullets
from alien import Alien
from game_stats import GameStats, Scoreboard
from button import Button


class AlienInvasion:
    """Clase general para la gestión de los recursos y el comportamiento del juego"""
    def __init__(self):
        pygame.init()

        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("ALIEN INVASION")

        self.stats = GameStats(self)
        self.score = Scoreboard(self)
        self.space_ship = SpaceShip(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.play_button = Button(self, "PLAY")

    def run_game(self):
        """Bucle principal del juego"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.space_ship.update()
                self._update_bullets()
                self._bullet_alien_collision()
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Activamos el botón play"""
        if self.play_button.rect.collidepoint(mouse_pos):
            self.stats.reset_stats()
            self.stats.game_active = True
            self.score.prep_score()
            self.score.prep_level()
            sleep(0.5)
            pygame.mouse.set_visible(False)


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

    def _bullet_alien_collision(self):
        # Comprobamos si una bala a chocado con un alien y si es así, ambas desaparecen
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.score.prep_score()
            self.score.check_high_score()

        # Comprobamos si se han eliminado todos los aliens para subir la dificultad
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_difficulty()
            self.stats.level += 1
            self.score.prep_level()

    def _ship_collision(self):
        """Impacto entre nave y alien"""
        if self.stats.space_ships_left > 0:
            self.stats.space_ships_left -= 1

            self.aliens.empty()
            self.bullets.empty()
            self.stats.reset_stats()

            self._create_fleet()
            self.space_ship.center_ship()

            sleep(1)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def check_bottom_collision(self):
        """Comprobamos cuando un alien llega al final de la pantalla"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_collision()
                break

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.space_ship, self.aliens):
            self._ship_collision()

        self.check_bottom_collision()

    def _update_screen(self):
        """Actualiza la pantalla en cada iteración"""
        self.screen.fill(self.settings.bg_color)
        self.space_ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullets()  # Llamamos al metodo draw_bullet de bullets.py
        self.aliens.draw(self.screen)

        self.score.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()