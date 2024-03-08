import sys
import pygame

from time import sleep
from modulos.settings import Settings
from modulos.ship import Ship
from modulos.bullet import Bullet
from modulos.alien import Alien
from modulos.game_stats import GameStats
from modulos.scoreboard import Scoreboard
from modulos.button import Button

class AlienInvasion:
    #Clase general para manejar los recursos y el comportamiento del juego.

    def __init__ (self):
        #Inicializa el juego y crea recursos.
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        #Crea una instancia para almacenar estadísticas del juego.
        self.stats = GameStats(self)
        #Creamos un marcador.
        self.sb = Scoreboard(self)

        #Inicia Alien Invasion en un estado activo.
        self.game_active = False

        #Crea el botón de Play.
        self.play_button = Button(self, "Play")


    def run_game (self):
        #Inicializa el bucle principal para el juego.
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
            self._update_screen()
            self.clock.tick(60)

    def _check_events (self):
        #Responde a pulsaciones de teclas y eventos de ratón.
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

    def _check_keydown_events (self, event):
        #Responde a pulsaciones de teclas
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        #elif event.key == pygame.K_UP:
            #self.ship.moving_up = True
        #elif event.key == pygame.K_DOWN:
            #self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_j:
            self._start_game()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events (self, event):
        #Responde a liberaciones de teclas
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        #elif event.key == pygame.K_UP:
            #self.ship.moving_up = False
        #elif event.key == pygame.K_DOWN:
            #self.ship.moving_down = False

    def _check_play_button (self, mouse_pos):
        """Inicia un juego nuevo cuando el jugador hace click en Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.settings.initialize_dynamic_settings()
            self._start_game()

        #Restablece las estadísticas del juego.
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()


    def _start_game (self):
        #Restablece las estadísticasa del juego.
        self.stats.reset_stats()
        self.game_active = True

        #Se deshace de los aliens y las balas que quedan.
        self.aliens.empty()
        self.bullets.empty()

        #Crea una flota nueva y centra la nave.
        self._create_fleet()
        self.ship.center_ship()

        #Oculta el cursor del ratón.
        pygame.mouse.set_visible(False)

    def _fire_bullet (self):
        #Crea una nueva bala y la añade al grupo de balas
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets (self):
        """Actualiza la posición de las balas y se deshace de las viejas."""
        #Actualiza las posiciones de las balas
        self.bullets.update()
        #Se deshace de las balas que han desaparecido.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullets_aliens_collisions()

    def _check_bullets_aliens_collisions (self):
        #Responde a colisiones entre balas y aliens
        #Elimina cualquier bala y alien que hayan colisionado.
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            #Se deshace de las balas existentes y crea una nueva flota.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            #Incrementa el nivel.
            self.stats.level += 1
            self.sb.prep_level()
                
    def _update_aliens (self):
        #Actualiza la posición de los aliens
        self._check_fleet_edges()
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Busca aliens que hayan llegado a la parte inferior de la pantalla.
        self._check_aliens_bottom()

    def _create_fleet (self):
        #Crea la flota de aliens.
        #Crea un alien y sigue creando alienígenas hasta que no queda espacio
        #El espaciado entre aliens es de uno de ancho y uno de alto
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 8 * alien_height):
            while current_x < self.settings.screen_width - 2 * alien_width:
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width

            #Fila terminada resetea x e incrementa y
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien (self, x_position, y_position):
            new_alien = Alien(self)
            new_alien.x = x_position
            new_alien.y = y_position
            new_alien.rect.x = x_position
            new_alien.rect.y = y_position
            self.aliens.add(new_alien)

    def _ship_hit (self):
        #Responde a un impacto de un alien en la nave
        if self.stats.ships_left > 0:
            #Decrementa ships_left y actualiza el marcador.
            self.stats.ships_left -= 1
            self.sb.prep_ships()

            #Vacía la lista de aliens y balas
            self.aliens.empty()
            self.bullets.empty()

            #Crea una nueva flota y centra la nave
            self._create_fleet()
            self.ship.center_ship()

            #Pausa
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_fleet_edges (self):
        #Responde adecuadamente si algún alienígena ha llegado a un borde.
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction (self):
        #Baja toda la flota y cambia la dirección de la flota.
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom (self):
        #Comprueba si algún alien ha llegado a la parte inferior de la pantalla.
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #Trata este caso igual que si la nave fuera golpeada.
                self._ship_hit()
                break

    def _update_screen (self):
        #Actualiza las imágenes en la pantalla y cambia a la pantalla nueva
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        #Dibuja la información de la puntuación.
        self.sb.show_score()
        #Dibuja el botón para jugar si el juego está inactivo.
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


#-----------------------------------------------------------------------------
if __name__ == '__main__':
    #Hace una instancia del juego y lo ejecuta.
    ai = AlienInvasion()
    ai.run_game()