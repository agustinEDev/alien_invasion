class Settings:
    #Clase para guardar toda la configuración de Aline Invasion.

    def __init__ (self):
        #Inicializa la configuración del juego.
        #Configuración de la pantalla.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.bullets_allowed = 10

        #Configuración de la nave
        self.ship_speed = 5.5
        self.ship_limit = 3

        #Configuración de las balas
        self.bullet_speed = 3.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        #Configuración de los alienígenas
        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        #Rapidez con la que se acelera el juego
        self.speedup_scale = 1.1

        #Lo rápido que aumenta el valor en puntos de los aliens.
        self.score_scale = 1.5

        #Configuración de la puntuación
        self.alien_points = 50

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings (self):
        """Inicializa las configuraciones que cambian durante el juego."""
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0

        #Dirección de 1 representa derecha; -1 representa izquierda.
        self.fleet_direction = 1

    def increase_speed (self):
        """Aumenta la velocidad de configuración y los valores en puntos de los aliens."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)