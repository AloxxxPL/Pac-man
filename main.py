import turtle
import random
import os
# import winsound
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, ENEMY_NUMBER, ENEMY_MOVE_SPEED, PLAYER_MOVE_SPEED
from renderer import Wall, Pellet, PowerPellet, UiPen
from actors import Player, Enemy
from mazes import maze_levels


def init_screen():
    "Konfiguracja głównego ekranu gry"
    # Tworzy główny ekran gry
    screen = turtle.Screen()
    screen.tracer(0)
    screen.setup(SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10)
    screen.bgcolor("black")
    return screen


def bind_controls(screen, player):
    "Powiązania klawiatury i myszy"
    # Poinformuj ekran o wciskaniu klawiszy i kliknięć myszy
    screen.listen()
    # Przypisz sterowanie
    screen.onkeypress(player.turn_right, "Right")
    screen.onkeypress(player.turn_left, "Left")
    screen.onkeypress(player.turn_up, "Up")
    screen.onkeypress(player.turn_down, "Down")


class LevelManager:
    "Zarządza poziomami gry i trudnością wrogów"

    def __init__(self):
        self.current_level = 0
        self.max_level = len(maze_levels) - 1

    def get_current_maze(self):
        "Zwróć mapę bieżącego poziomu"
        return maze_levels[self.current_level]

    def next_level(self):
        "Przejdź na następny poziom. Zwróć True jeśli jest, False jeśli koniec gry"
        if self.current_level < self.max_level:
            self.current_level += 1
            return True
        return False

    def is_game_won(self):
        "Sprawdź czy gracz wygrał (ukończył ostatni level)"
        return self.current_level == self.max_level

    def get_enemy_speed(self):
        "Zwróć prędkość wrogów dla bieżącego levelu"
        base_speed = ENEMY_MOVE_SPEED
        level_bonus = self.current_level * 2
        max_speed = PLAYER_MOVE_SPEED
        return min(base_speed + level_bonus, max_speed)


def load_next_level(screen, player, level_manager, score_pen, lives_pen, ui_pen):
    "Wyczyść scenę i załaduj następny level"
    # Wyczyść wszystkie obiekty ze sceny
    screen.clear()

    # Załaduj nową mapę i stwórz nowe obiekty renderowania
    current_maze = level_manager.get_current_maze()
    wall_pen = Wall(current_maze)
    pellet_pen = Pellet(current_maze)
    power_pen = PowerPellet(current_maze)

    wall_pen.draw()
    pellet_pen.draw()
    power_pen.draw()
    ui_pen.draw_ui_area()

    # Resetuj gracza na nową mapę (score się nie zmienia!)
    player_start_coor = random.choice(pellet_pen.pellets)
    player_start_x = player_start_coor[0]
    player_start_y = player_start_coor[1]
    player.goto(player_start_x, player_start_y)
    player.state = "stop"

    # Resetuj wrogów z nową prędkością
    enemies = []
    enemy_colors = ["green_enemy.gif", "pink_enemy.gif", "red_enemy.gif"]
    for _ in range(ENEMY_NUMBER):
        # Znajdź bezpieczne pozycje dla wrogów (daleko od gracza)
        safe_spots = []
        for pellet in pellet_pen.pellets:
            if player.distance(pellet) > CELL_SIZE * 5:
                safe_spots.append(pellet)
        if not safe_spots:
            safe_spots = pellet_pen.pellets
        enemy_start_x, enemy_start_y = random.choice(safe_spots)
        enemy = Enemy(enemy_start_x, enemy_start_y, wall_pen.walls, player)
        enemy.shape(random.choice(enemy_colors))
        enemy.move_speed = level_manager.get_enemy_speed()
        enemies.append(enemy)

    # Resetuj UI
    new_score_pen = UiPen()
    new_lives_pen = UiPen()

    # Uruchom grę na nowym levelu
    screen.ontimer(lambda: bind_controls(screen, player), 2500)
    for enemy in enemies:
        screen.ontimer(enemy.start_move, 2500)

    game_loop(
        screen, player, new_score_pen, new_lives_pen,
        pellet_pen, power_pen,
        player_start_x, player_start_y, enemies, level_manager
    )


def game_loop(screen, player, score_pen, lives_pen, pellet_pen, power_pen, player_start_x, player_start_y, enemies, level_manager, _ui_cache=[None, None, None, None], _super_mode_timer=[0], _enemy_freeze_timers=[{}], _enemy_spawn_positions=[{}]):
    "Aktualizacje w czasie rzeczywistym"
    super_mode_timer = _super_mode_timer[0]
    enemy_freeze_timers = _enemy_freeze_timers[0]
    enemy_spawn_positions = _enemy_spawn_positions[0]

    if not enemy_spawn_positions:
        for enemy in enemies:
            enemy_spawn_positions[enemy] = (round(enemy.xcor()), round(enemy.ycor()))

    # Decrement super mode timer
    if super_mode_timer > 0:
        super_mode_timer -= 1
        if super_mode_timer <= 0:
            player.super_mode_active = False

    # Decrement and clean up freeze timers
    for enemy in list(enemy_freeze_timers.keys()):
        enemy_freeze_timers[enemy] -= 1
        if enemy_freeze_timers[enemy] <= 0:
            del enemy_freeze_timers[enemy]

    # Aktualizuj wynik, życia i komunikaty gry – tylko gdy coś się zmieniło
    ui_state = (player.score, player.lives, len(pellet_pen.stamps), len(power_pen.stamps))
    if ui_state != (_ui_cache[0], _ui_cache[1], _ui_cache[2], _ui_cache[3]):
        score_pen.write_score(player.score, player.lives, pellet_pen.stamps, power_pen.stamps)
        lives_pen.write_lives(player.lives, pellet_pen.stamps, power_pen.stamps)
        _ui_cache[0], _ui_cache[1], _ui_cache[2], _ui_cache[3] = ui_state
    # Kolizja: gracz-kulka
    for (px, py), stamp_id in list(pellet_pen.stamps.items()):
        if player.distance(px, py) < CELL_SIZE / 2:
            os.system("aplay eat.wav > /dev/null 2>&1 &")
            # winsound.PlaySound("eat.wav", winsound.SND_ASYNC)
            pellet_pen.clearstamp(stamp_id)
            del pellet_pen.stamps[(px, py)]
            player.score += 2
    # Kolizja: gracz-kulka mocy
    for (px, py), stamp_id in list(power_pen.stamps.items()):
        if player.distance(px, py) < CELL_SIZE / 2:
            os.system("aplay eat.wav > /dev/null 2>&1 &")
            # winsound.PlaySound("eat.wav", winsound.SND_ASYNC)
            power_pen.clearstamp(stamp_id)
            del power_pen.stamps[(px, py)]
            player.score += 50
            # Przyspieszenie
            player.move_speed += 3
            screen.ontimer(player.reset_speed, 3000)
    # Aktualizuj gracza
    player.move()
    player.check_wall_collision()
    # Aktualizuj wrogów
    for enemy in enemies:
        enemy.move()
        enemy.check_wall_collision()
        enemy.go_after_player()
        # Kolizja: gracz-wróg
        if enemy.distance(player) < CELL_SIZE / 2:
            os.system("aplay death.wav > /dev/null 2>&1 &")
            # winsound.PlaySound("death.wav", winsound.SND_ASYNC)
            # Upewnij się, że gracz nie odradza się blisko wroga
            safe_spots = []
            for pellet in pellet_pen.pellets:
                if all(enemy.distance(pellet) > CELL_SIZE * 5 for enemy in enemies):
                    safe_spots.append(pellet)
            if not safe_spots:
                safe_spots = list(pellet_pen.pellets)
            player.goto(random.choice(safe_spots))
            player.lives -= 1        
    # Koniec levelu – sprawdź czy był ostatni
    if len(power_pen.stamps) == 0 and len(pellet_pen.stamps) == 0:
        player.state = "stop"
        for enemy in enemies:
            enemy.hideturtle()
            enemy.state = "stop"

        # Próba przejścia na następny level
        if level_manager.next_level():
            # Następny level dostępny — załaduj nową mapę
            screen.ontimer(
                lambda: load_next_level(
                    screen, player, level_manager,
                    score_pen, lives_pen, UiPen()
                ),
                2000
            )
        else:
            # Koniec gry — wyświetl win screen
            ui_pen = UiPen()
            ui_pen.write_final_win(player.score)
            screen.ontimer(screen.bye, 3000)
    # Koniec gry – zatrzymaj wszystko i zamknij grę
    if player.lives == 0:
        player.state = "stop"
        player.hideturtle()
        for enemy in enemies:
            enemy.state = "stop"
        screen.ontimer(screen.bye, 3000)
    # Aktualizuj ekran
    screen.update()
    # Store state in mutable defaults for next frame
    _super_mode_timer[0] = super_mode_timer
    _enemy_freeze_timers[0] = enemy_freeze_timers
    # Powtarzaj funkcję co 16 ms
    screen.ontimer(
        lambda: game_loop(
            screen,
            player,
            score_pen,
            lives_pen,
            pellet_pen,
            power_pen,
            player_start_x,
            player_start_y,
            enemies,
            level_manager
        ),
        1000 // 60
    )


def main():
    "Główna funkcja – konfiguracja gry"
    # Utwórz ekran i zarejestruj kształty
    screen = init_screen()
    screen.register_shape("pac.gif")
    screen.register_shape("up.gif")
    screen.register_shape("down.gif")
    screen.register_shape("left.gif")
    screen.register_shape("right.gif")
    screen.register_shape("green_enemy.gif")
    screen.register_shape("pink_enemy.gif")
    screen.register_shape("red_enemy.gif")
    screen.register_shape("wall.gif")

    # Utwórz LevelManager
    level_manager = LevelManager()

    # Załaduj pierwszą mapę
    current_maze = level_manager.get_current_maze()

    # Utwórz instancje renderowania
    wall_pen = Wall(current_maze)
    pellet_pen = Pellet(current_maze)
    power_pen = PowerPellet(current_maze)
    ui_pen = UiPen()
    score_pen = UiPen()
    lives_pen = UiPen()

    # Wywołaj metody instancji i pobierz atrybuty
    wall_pen.draw()
    walls = wall_pen.walls
    pellet_pen.draw()
    pellets = pellet_pen.pellets
    power_pen.draw()
    ui_pen.draw_ui_area()

    # Pozycja startowa gracza
    player_start_coor = random.choice(pellet_pen.pellets)
    player_start_x = player_start_coor[0]
    player_start_y = player_start_coor[1]

    # Utwórz Pac-Mana
    player = Player(walls)
    player.goto(player_start_x, player_start_y)

    # Utwórz wrogów
    enemy_colors = ["green_enemy.gif", "pink_enemy.gif", "red_enemy.gif"]
    enemies = []
    for _ in range(ENEMY_NUMBER):
        # Upewnij się, że wróg nie odradza się blisko gracza
        safe_spots = []
        for pellet in pellets:
            if player.distance(pellet) > CELL_SIZE * 5:
                safe_spots.append(pellet)
        if not safe_spots:
            safe_spots = pellets
        enemy_start_x, enemy_start_y = random.choice(safe_spots)
        enemy = Enemy(enemy_start_x, enemy_start_y, walls, player)
        enemy.shape(random.choice(enemy_colors))
        enemies.append(enemy)

    # Ustawienia startu gry
    os.system("aplay start_up.wav > /dev/null 2>&1 &")
    screen.ontimer(lambda: bind_controls(screen, player), 2500)
    for enemy in enemies:
        screen.ontimer(enemy.start_move, 2500)

    # Włącz aktualizacje w czasie rzeczywistym
    game_loop(screen, player, score_pen, lives_pen, pellet_pen, power_pen, player_start_x, player_start_y, enemies, level_manager)
    screen.mainloop()

if __name__ == "__main__":
    main()