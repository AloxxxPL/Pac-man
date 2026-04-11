import turtle
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE, ENEMY_NUMBER
from renderer import Wall, Pellet, PowerPellet, UiPen
from actors import Player, Enemy


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


def game_loop(screen, player, score_pen, lives_pen, pellet_pen, power_pen, player_start_x, player_start_y, enemies,
              _ui_cache=[None, None, None, None]):
    "Aktualizacje w czasie rzeczywistym"
    # Aktualizuj wynik, życia i komunikaty gry – tylko gdy coś się zmieniło
    ui_state = (player.score, player.lives, len(pellet_pen.stamps), len(power_pen.stamps))
    if ui_state != (_ui_cache[0], _ui_cache[1], _ui_cache[2], _ui_cache[3]):
        score_pen.write_score(player.score, player.lives, pellet_pen.stamps, power_pen.stamps)
        lives_pen.write_lives(player.lives, pellet_pen.stamps, power_pen.stamps)
        _ui_cache[0], _ui_cache[1], _ui_cache[2], _ui_cache[3] = ui_state
    # Kolizja: gracz-kulka
    for (px, py), stamp_id in list(pellet_pen.stamps.items()):
        if player.distance(px, py) < CELL_SIZE / 2 and (px, py) != (player_start_x, player_start_y):
            pellet_pen.clearstamp(stamp_id)
            del pellet_pen.stamps[(px, py)]
            player.score += 2
        # Pomiń punkty na starcie gry z pierwszej kulki
        elif player.distance(px, py) < CELL_SIZE / 2 and (px, py) == (player_start_x, player_start_y):
            pellet_pen.clearstamp(stamp_id)
            del pellet_pen.stamps[(px, py)]
    # Kolizja: gracz-kulka mocy
    for (px, py), stamp_id in list(power_pen.stamps.items()):
        if player.distance(px, py) < CELL_SIZE / 2:
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
            # Upewnij się, że gracz nie odradza się blisko wroga
            safe_spots = []
            for pellet in pellet_pen.pellets:
                if all(enemy.distance(pellet) > CELL_SIZE * 5 for enemy in enemies):
                    safe_spots.append(pellet)
            player.goto(random.choice(safe_spots))
            player.lives -= 1        
    # Wygrana gra – zatrzymaj wszystko i zamknij grę
    if len(power_pen.stamps) == 0 and len(pellet_pen.stamps) == 0:
        player.state = "stop"
        for enemy in enemies:
            enemy.hideturtle()
            enemy.state = "stop"
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
            enemies
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
    # Utwórz instancje renderowania
    wall_pen = Wall()
    pellet_pen = Pellet()
    power_pen = PowerPellet()
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
        enemy_start_x, enemy_start_y = random.choice(safe_spots)
        enemy = Enemy(enemy_start_x, enemy_start_y, walls, player)
        enemy.shape(random.choice(enemy_colors))
        enemies.append(enemy)
    # Ustawienia startu gry
    screen.ontimer(lambda: bind_controls(screen, player), 2500)
    for enemy in enemies:
        screen.ontimer(enemy.start_move, 2500)
    # Włącz aktualizacje w czasie rzeczywistym
    game_loop(screen, player, score_pen, lives_pen, pellet_pen, power_pen, player_start_x, player_start_y, enemies)
    screen.mainloop()

if __name__ == "__main__":
    main()