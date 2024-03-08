class GameStats:
    """Sigue las estadísticas de Alien Invasion."""

    def __init__ (self, ai_game):
        """Inicializa las estadísticas."""
        self.settings = ai_game.settings
        self.reset_stats()

        #La puntuación más alta nunca debe reiniciarse.
        self.high_score = 0

    def reset_stats (self):
        #Inicializa las estadísticas que pueden cambiar durante el juego.
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1