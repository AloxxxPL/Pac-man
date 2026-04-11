import turtle
import random
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from renderer import Wall, Pellet, PowerPellet
from actors import Player


def init_screen():
    "Konfiguracja głównego ekranu gry"
    # Tworzenie głównego ekranu gry
    screen = turtle.Screen()
    screen.tracer(0)
    screen.setup(SCREEN_WIDTH + 10, SCREEN_HEIGHT + 10)
    screen.bgcolor("black")
    return screen


def bind_controls(screen, player):
    "Przypisania klawiszy i myszy"
    # Informowanie ekranu o nasłuchiwaniu kliknięć klawiatury lub myszy
    screen.listen()
    # Przypisywanie sterowania
    screen.onkeypress(player.turn_right, "Right")
    screen.onkeypress(player.turn_left, "Left")
    screen.onkeypress(player.turn_up, "Up")
    screen.onkeypress(player.turn_down, "Down")


def game_loop(screen, player):
    "Aktualizacje w czasie rzeczywistym"
    # Aktualizacja gracza
    player.move()
    # Aktualizacja ekranu
    screen.update()
    # Powtarzanie funkcji co 16ms
    screen.ontimer(lambda: game_loop(
        screen, player), 1000 // 60)


def main():
    "Funkcja główna – konfiguracja gry"
    # Tworzenie ekranu
    screen = init_screen()
    # Tworzenie instancji renderowania
    wall_pen = Wall()
    pellet_pen = Pellet()
    power_pen = PowerPellet()
    # Wywołanie funkcji instancji
    wall_pen.draw()
    pellet_pen.draw()
    power_pen.draw()
    # Pozycja startowa gracza (na losowej kulce)
    player_start_coor = random.choice(pellet_pen.pellets)
    player_start_x = player_start_coor[0]
    player_start_y = player_start_coor[1]
    # Tworzenie Pac-Mana
    player = Player()
    player.goto(player_start_x, player_start_y)
    # Przypisywanie sterowania
    bind_controls(screen, player)
    # Włączanie aktualizacji w czasie rzeczywistym
    game_loop(screen, player)
    # Utrzymywanie głównego ekranu otwartego
    screen.mainloop()

# Zapewnia, że gra uruchamia się tylko gdy main.py jest uruchamiany bezpośrednio, a nie importowany
if __name__ == "__main__":
    main()
