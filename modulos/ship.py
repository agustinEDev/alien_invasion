import pygame

class Ship:
    #Una clase para gestionar la nave.

    def __init__ (self, ai_game):
        #Inicializa la nave y configura su posición inicial.
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #Carga la imagen de la nave y obtiene su rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        #Coloca inicialmente cada nave nueva en el centro de la parte inferior de la pantalla.
        self.rect.midbottom = self.screen_rect.midbottom

        #Guarda un valor decimal para la posición horizontal exacta de la nave
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        #Banderas de movimiento; empiezan sin movimiento
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update (self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        elif self.moving_left and self.rect.x > self.screen_rect.left:
            self.x -= self.settings.ship_speed
        elif self.moving_up and self.rect.top > self.screen_rect.top:
            self.y -= self.settings.ship_speed
        elif self.moving_down and self.rect.y < self.screen_rect.bottom - self.rect.height:
            self.y += self.settings.ship_speed

        #Actualiza el objeto rect de self.x
        self.rect.x = self.x
        #Actualiza el objeto rect de self.y
        self.rect.y = self.y

    def blitme (self):
        #Dibuja la nave en su ubicación actual
        self.screen.blit(self.image, self.rect)


    def center_ship (self):
        #Centra la nave en la pantalla
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)