import sys
import pygame

from modulos.settings import Settings
from modulos.ship import Ship
from modulos.bullet import Bullet
from modulos.alien import Alien

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


    def run_game (self):
        #Inicializa el bucle principal para el juego.
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
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

    def _check_keydown_events (self, event):
        #Responde a pulsaciones de teclas
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events (self, event):
        #Responde a liberaciones de teclas
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

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
            #print(len(self.bullets))

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

    def _update_screen (self):
        #Actualiza las imágenes en la pantalla y cambia a la pantalla nueva
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)
        pygame.display.flip()


#-----------------------------------------------------------------------------
if __name__ == '__main__':
    #Hace una instancia del juego y lo ejecuta.
    ai = AlienInvasion()
    ai.run_game()