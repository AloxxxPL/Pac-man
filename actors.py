import math
import random
from constants import (CELL_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, UI_HEIGHT,
                       PLAYER_MOVE_SPEED, ENEMY_MOVE_SPEED, ENEMY_RADAR)

# Direction → (dx, dy) in pygame coords (y grows downward)
_DIR_VECTOR = {
    "right": (1, 0),
    "left":  (-1, 0),
    "up":    (0, -1),
    "down":  (0,  1),
}

_MAZE_BOTTOM = SCREEN_HEIGHT
_MAZE_TOP    = UI_HEIGHT


class Actor:
    def __init__(self, x, y, wall_grid):
        self.x = float(x)
        self.y = float(y)
        self.direction = "right"
        self.state = "stop"
        self.wall_grid = wall_grid

    def distance(self, other):
        return math.hypot(self.x - other.x, self.y - other.y)

    def distance_xy(self, x, y):
        return math.hypot(self.x - x, self.y - y)

    def _wrap(self):
        if self.x < 0:
            self.x = SCREEN_WIDTH
        elif self.x > SCREEN_WIDTH:
            self.x = 0
        if self.y < _MAZE_TOP:
            self.y = _MAZE_BOTTOM
        elif self.y > _MAZE_BOTTOM:
            self.y = _MAZE_TOP

    def _move_forward(self, speed):
        dx, dy = _DIR_VECTOR[self.direction]
        self.x += dx * speed
        self.y += dy * speed
        self._wrap()

    def check_wall_collision(self):
        rx = round(self.x)
        ry = round(self.y)
        half = round(CELL_SIZE / 2)
        nearby = self.wall_grid.get_nearby_walls(rx, ry, radius_cells=2)
        for wx, wy in nearby:
            dx = rx - wx
            dy = ry - wy
            if abs(dx) >= CELL_SIZE * 2 or abs(dy) >= CELL_SIZE * 2:
                continue
            self._resolve_wall(dx, dy, wx, wy, half)

    def _resolve_wall(self, dx, dy, wx, wy, half):
        d = self.direction
        if d == "right":
            if -half < dx + half < half and -half <= dy <= half:
                self.x = wx - CELL_SIZE
                self._on_wall_hit()
            elif -half < dx + half < half and dy < -half and abs(dy) < CELL_SIZE:
                self.y = wy - CELL_SIZE
            elif -half < dx + half < half and dy > half and abs(dy) < CELL_SIZE:
                self.y = wy + CELL_SIZE
        elif d == "left":
            if -half < dx - half < half and -half <= dy <= half:
                self.x = wx + CELL_SIZE
                self._on_wall_hit()
            elif -half < dx - half < half and dy < -half and abs(dy) < CELL_SIZE:
                self.y = wy - CELL_SIZE
            elif -half < dx - half < half and dy > half and abs(dy) < CELL_SIZE:
                self.y = wy + CELL_SIZE
        elif d == "up":
            if -half <= dx <= half and -half < dy - half < half:
                self.y = wy + CELL_SIZE
                self._on_wall_hit()
            elif dx > half and abs(dx) < CELL_SIZE and -half < dy - half < half:
                self.x = wx + CELL_SIZE
            elif dx < -half and abs(dx) < CELL_SIZE and -half < dy - half < half:
                self.x = wx - CELL_SIZE
        elif d == "down":
            if -half <= dx <= half and -half < dy + half < half:
                self.y = wy - CELL_SIZE
                self._on_wall_hit()
            elif dx > half and abs(dx) < CELL_SIZE and -half < dy + half < half:
                self.x = wx + CELL_SIZE
            elif dx < -half and abs(dx) < CELL_SIZE and -half < dy + half < half:
                self.x = wx - CELL_SIZE

    def _on_wall_hit(self):
        pass


class Player(Actor):
    def __init__(self, wall_grid):
        super().__init__(0, 0, wall_grid)
        self.move_speed = PLAYER_MOVE_SPEED
        self.lives = 3
        self.score = 0
        self.super_mode_active = False
        # sprite key used by renderer
        self.sprite = "pac"

    def move(self):
        self._update_sprite()
        if self.state != "stop":
            self._move_forward(self.move_speed)

    def _update_sprite(self):
        if self.state == "stop":
            self.sprite = "pac"
        else:
            self.sprite = self.direction  # "right"/"left"/"up"/"down"

    def _on_wall_hit(self):
        self.state = "stop"

    def turn_right(self):
        self.direction = "right"
        self.state = "move"

    def turn_left(self):
        self.direction = "left"
        self.state = "move"

    def turn_up(self):
        self.direction = "up"
        self.state = "move"

    def turn_down(self):
        self.direction = "down"
        self.state = "move"

    def reset_speed(self):
        self.move_speed = PLAYER_MOVE_SPEED


class Enemy(Actor):
    def __init__(self, start_x, start_y, wall_grid, player: Player):
        super().__init__(start_x, start_y, wall_grid)
        self.walls = set()
        for walls_list in wall_grid.grid.values():
            self.walls.update(walls_list)
        self.player = player
        self.move_speed = ENEMY_MOVE_SPEED
        self.sprite = "green_enemy"

    def move(self):
        if self.state != "stop":
            self._move_forward(self.move_speed)

    def _on_wall_hit(self):
        self.start_move()

    def start_move(self):
        rx = round(self.x)
        ry = round(self.y)
        candidates = [
            ("right", (rx + CELL_SIZE, ry)),
            ("left",  (rx - CELL_SIZE, ry)),
            ("up",    (rx, ry - CELL_SIZE)),
            ("down",  (rx, ry + CELL_SIZE)),
        ]
        valid = [(d, pos) for d, pos in candidates if pos not in self.walls]
        if not valid:
            valid = candidates
        chosen_dir, _ = random.choice(valid)
        self.direction = chosen_dir
        self.state = "move"

    def go_after_player(self):
        px = round(self.player.x)
        py = round(self.player.y)
        ex = round(self.x)
        ey = round(self.y)
        half = CELL_SIZE / 2
        dist = self.distance(self.player)

        if dist > ENEMY_RADAR:
            return

        if self.direction in ("right", "left"):
            if py < ey and abs(px - ex) < half:
                self.direction = "up"
            elif py > ey and abs(px - ex) < half:
                self.direction = "down"
        elif self.direction in ("up", "down"):
            if px > ex and abs(py - ey) < half:
                self.direction = "right"
            elif px < ex and abs(py - ey) < half:
                self.direction = "left"

        if py == ey and px > ex:
            self.direction = "right"
        elif py == ey and px < ex:
            self.direction = "left"
        elif px == ex and py < ey:
            self.direction = "up"
        elif px == ex and py > ey:
            self.direction = "down"
