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