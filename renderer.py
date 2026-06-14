import pygame
from constants import CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, UI_HEIGHT


def load_sprites():
    """Load all GIF sprites and return as dict of pygame.Surface."""
    names = ["pac", "right", "left", "up", "down",
             "green_enemy", "pink_enemy", "red_enemy", "wall"]
    sprites = {}
    for name in names:
        path = name + ".gif"
        try:
            surf = pygame.image.load(path).convert_alpha()
            surf = pygame.transform.scale(surf, (CELL_SIZE, CELL_SIZE))
        except Exception:
            # Fallback: coloured square so the game still runs without asset files
            surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            colour = {
                "pac": (255, 255, 0), "right": (255, 255, 0),
                "left": (255, 255, 0), "up": (255, 255, 0),
                "down": (255, 255, 0), "green_enemy": (0, 200, 0),
                "pink_enemy": (255, 105, 180), "red_enemy": (220, 0, 0),
                "wall": (0, 0, 180),
            }.get(name, (128, 128, 128))
            surf.fill(colour)
        sprites[name] = surf
    return sprites


class Renderer:
    def __init__(self, screen: pygame.Surface, sprites: dict):
        self.screen = screen
        self.sprites = sprites
        self._font_large = pygame.font.SysFont("Courier", 28, bold=False)
        self._font_med   = pygame.font.SysFont("Courier", 36, bold=True)

    # ------------------------------------------------------------------ walls
    def draw_walls(self, walls):
        img = self.sprites["wall"]
        half = CELL_SIZE // 2
        for x, y in walls:
            self.screen.blit(img, (x - half, y - half))

    # ---------------------------------------------------------------- pellets
    def draw_pellets(self, pellets):
        for x, y in pellets:
            pygame.draw.circle(self.screen, (255, 215, 0), (int(x), int(y)), 5)

    def draw_power_pellets(self, power_pellets):
        for x, y in power_pellets:
            pygame.draw.circle(self.screen, (124, 252, 0), (int(x), int(y)), 10)

    # ----------------------------------------------------------------- actors
    def draw_actor(self, actor, sprite_key):
        img = self.sprites.get(sprite_key, self.sprites["pac"])
        half = CELL_SIZE // 2
        self.screen.blit(img, (int(actor.x) - half, int(actor.y) - half))

    def draw_player(self, player):
        self.draw_actor(player, player.sprite)

    def draw_enemies(self, enemies):
        for enemy in enemies:
            self.draw_actor(enemy, enemy.sprite)

    # ----------------------------------------------------------------------- UI
    def draw_ui(self, score, lives):
        # Background bar
        pygame.draw.rect(self.screen, (0, 0, 0),
                         (0, 0, SCREEN_WIDTH, UI_HEIGHT))
        pygame.draw.line(self.screen, (180, 180, 180),
                         (0, UI_HEIGHT - 2), (SCREEN_WIDTH, UI_HEIGHT - 2), 2)

        score_surf = self._font_large.render(f"Score: {score}", True, (255, 255, 255))
        lives_surf = self._font_large.render(f"Lives: {lives}", True, (255, 255, 255))
        self.screen.blit(score_surf, (20, (UI_HEIGHT - score_surf.get_height()) // 2))
        self.screen.blit(lives_surf,
                         (SCREEN_WIDTH - lives_surf.get_width() - 20,
                          (UI_HEIGHT - lives_surf.get_height()) // 2))

    def draw_message(self, text, colour=(255, 255, 0)):
        surf = self._font_med.render(text, True, colour)
        x = (SCREEN_WIDTH - surf.get_width()) // 2
        y = (SCREEN_HEIGHT - surf.get_height()) // 2
        self.screen.blit(surf, (x, y))

    # --------------------------------------------------------- full frame draw
    def draw_frame(self, walls, pellets, power_pellets, player, enemies, score, lives):
        self.screen.fill((0, 0, 0))
        self.draw_walls(walls)
        self.draw_pellets(pellets)
        self.draw_power_pellets(power_pellets)
        self.draw_enemies(enemies)
        self.draw_player(player)
        self.draw_ui(score, lives)
        pygame.display.flip()
