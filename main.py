import pygame
import random
from constants import (CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT,
                       ENEMY_NUMBER, ENEMY_MOVE_SPEED, PLAYER_MOVE_SPEED)
from renderer import Renderer, load_sprites
from actors import Player, Enemy
from mazes import maze_levels, calculate_maze_data
from spatial_grid import SpatialGrid


class LevelManager:
    def __init__(self):
        self.current_level = 0
        self.max_level = len(maze_levels) - 1

    def get_current_maze(self):
        return maze_levels[self.current_level]

    def next_level(self):
        if self.current_level < self.max_level:
            self.current_level += 1
            return True
        return False

    def is_game_won(self):
        return self.current_level == self.max_level

    def get_enemy_speed(self):
        return min(ENEMY_MOVE_SPEED + self.current_level * 2, PLAYER_MOVE_SPEED)


def _make_enemies(count, pellets, wall_grid, player, speed, sprite_names):
    enemies = []
    for _ in range(count):
        safe = [p for p in pellets if player.distance_xy(*p) > CELL_SIZE * 5] or list(pellets)
        sx, sy = random.choice(safe)
        e = Enemy(sx, sy, wall_grid, player)
        e.sprite = random.choice(sprite_names)
        e.move_speed = speed
        enemies.append(e)
    return enemies


class Game:
    SPRITE_NAMES = ["green_enemy", "pink_enemy", "red_enemy"]

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.sprites = load_sprites()
        self.renderer = Renderer(self.screen, self.sprites)
        self._load_sounds()

        self.level_manager = LevelManager()
        self.player = Player(None)  # wall_grid set in _load_level

        # Initialize before _load_level so it can overwrite correctly
        self.super_timer = 0
        self.freeze_timers = {}
        self.enemy_spawns = {}
        self.state = "countdown"
        self.state_timer = 150
        self.message = ""

        self._load_level(startup=True)

    # ----------------------------------------------------------------- setup
    def _load_sounds(self):
        self.sounds = {}
        for name in ("eat", "death", "start_up"):
            try:
                self.sounds[name] = pygame.mixer.Sound(f"{name}.wav")
            except Exception:
                self.sounds[name] = None

    def _play(self, name):
        s = self.sounds.get(name)
        if s:
            s.play()

    def _load_level(self, startup=False):
        maze = self.level_manager.get_current_maze()
        walls, pellets, power_pellets = calculate_maze_data(maze)
        self.walls = walls
        self.pellets = set(pellets)
        self.power_pellets = set(power_pellets)
        self.wall_grid = SpatialGrid(walls)

        # Place player
        start = random.choice(pellets)
        self.player.x, self.player.y = float(start[0]), float(start[1])
        self.player.state = "stop"
        self.player.wall_grid = self.wall_grid

        # Enemies
        self.enemies = _make_enemies(
            ENEMY_NUMBER, pellets, self.wall_grid, self.player,
            self.level_manager.get_enemy_speed(), self.SPRITE_NAMES
        )
        self.enemy_spawns = {e: (e.x, e.y) for e in self.enemies}
        self.freeze_timers = {}
        self.super_timer = 0

        if startup:
            self._play("start_up")

    # ----------------------------------------------------------------- input
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and self.state == "playing":
                if event.key == pygame.K_RIGHT:
                    self.player.turn_right()
                elif event.key == pygame.K_LEFT:
                    self.player.turn_left()
                elif event.key == pygame.K_UP:
                    self.player.turn_up()
                elif event.key == pygame.K_DOWN:
                    self.player.turn_down()
        return True

    # ----------------------------------------------------------------- update
    def _update(self):
        if self.state == "countdown":
            self.state_timer -= 1
            if self.state_timer <= 0:
                self.state = "playing"
                for e in self.enemies:
                    e.start_move()
            return

        if self.state != "playing":
            self.state_timer -= 1
            return

        # Super mode countdown
        if self.super_timer > 0:
            self.super_timer -= 1
            if self.super_timer == 0:
                self.player.super_mode_active = False

        # Freeze timers
        for e in list(self.freeze_timers):
            self.freeze_timers[e] -= 1
            if self.freeze_timers[e] <= 0:
                del self.freeze_timers[e]

        # Move player
        self.player.move()
        self.player.check_wall_collision()

        # Pellet collision
        for pos in list(self.pellets):
            if self.player.distance_xy(*pos) < CELL_SIZE / 2:
                self._play("eat")
                self.pellets.discard(pos)
                self.player.score += 2

        # Power pellet collision
        for pos in list(self.power_pellets):
            if self.player.distance_xy(*pos) < CELL_SIZE / 2:
                self._play("eat")
                self.power_pellets.discard(pos)
                self.player.score += 50
                self.player.super_mode_active = True
                self.super_timer = 900

        # Move enemies
        for e in self.enemies:
            if e in self.freeze_timers:
                continue
            e.move()
            e.check_wall_collision()
            e.go_after_player()

            if e.distance(self.player) < CELL_SIZE / 2:
                if self.player.super_mode_active:
                    self._play("eat")
                    sx, sy = self.enemy_spawns[e]
                    e.x, e.y = sx, sy
                    self.freeze_timers[e] = 300
                    self.player.score += 100
                else:
                    self._play("death")
                    safe = [p for p in self.pellets
                            if all(en.distance_xy(*p) > CELL_SIZE * 5 for en in self.enemies)]
                    if not safe:
                        safe = list(self.pellets) or [(self.player.x, self.player.y)]
                    self.player.x, self.player.y = random.choice(safe)
                    self.player.lives -= 1

        # Check win / loss
        if not self.pellets and not self.power_pellets:
            if self.level_manager.next_level():
                self.state = "next_level"
                self.state_timer = 120
            else:
                self.state = "win"
                self.state_timer = 180
            for e in self.enemies:
                e.state = "stop"
            self.player.state = "stop"

        if self.player.lives <= 0:
            self.state = "gameover"
            self.state_timer = 180
            self.player.state = "stop"
            for e in self.enemies:
                e.state = "stop"

    # ----------------------------------------------------------------- render
    def _render(self):
        self.renderer.draw_frame(
            self.walls,
            self.pellets,
            self.power_pellets,
            self.player,
            self.enemies,
            self.player.score,
            self.player.lives,
        )
        if self.state == "countdown":
            self.renderer.draw_message("GET READY!", (255, 255, 0))
        elif self.state == "win":
            self.renderer.draw_message(
                f"YOU WON ALL LEVELS!  Score: {self.player.score}", (255, 255, 0))
        elif self.state == "gameover":
            self.renderer.draw_message(
                f"GAME OVER  Score: {self.player.score}", (220, 0, 0))
        elif self.state == "next_level":
            self.renderer.draw_message("LEVEL CLEAR!", (0, 255, 128))
        pygame.display.flip()

    # ------------------------------------------------------------------- loop
    def run(self):
        running = True
        while running:
            running = self._handle_events()

            # Handle reset-speed timer via pygame USEREVENT
            self._update()
            self._render()

            # Transition: next level loads after short delay
            if self.state == "next_level" and self.state_timer <= 0:
                self._load_level()
                self.state = "countdown"
                self.state_timer = 150

            # End states: close after timer
            if self.state in ("win", "gameover") and self.state_timer <= 0:
                running = False

            self.clock.tick(60)

        pygame.quit()


def main():
    Game().run()


if __name__ == "__main__":
    main()
