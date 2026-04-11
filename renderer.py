import turtle
from mazes import calculate_maze_data, maze_level_1
from constants import CELL_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH


class Pen(turtle.Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.color("silver")
        self.speed(0)
        # Pobierz wszystkie współrzędne z poziomu labiryntu
        self.walls, self.pellets, self.power_pellets = calculate_maze_data(
            maze_level_1)


class Wall(Pen):

    def __init__(self):
        super().__init__()
        self.shape("wall.gif")
        
    def draw(self):
        "Rysuj ścianę na ekranie"
        for x, y in self.walls:
            self.goto(x, y)
            self.stamp()

class Pellet(Pen):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(0.35, 0.35)
        self.pencolor("white")
        self.fillcolor("gold")
        self.stamps = {}

    def draw(self):
        "Rysuj kulkę na ekranie"
        for x, y in self.pellets:
            self.goto(x, y)
            # Ostempluj kulkę i zapisz id stempla współrzędnej w zmiennej
            stamp_id = self.stamp()
            # Dodaj współrzędną do słownika i przypisz ją do zapisanego stamp_id
            self.stamps[(x, y)] = stamp_id

class PowerPellet(Pen):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(0.8, 0.8)
        self.pencolor("white")
        self.fillcolor("chartreuse")
        self.stamps = {}

    def draw(self):
        "Rysuj kulkę mocy na ekranie"
        for x, y in self.power_pellets:
            self.goto(x, y)
            # Ostempluj kulkę mocy i zapisz id stempla współrzędnej w zmiennej
            stamp_id = self.stamp()
            # Dodaj współrzędną do słownika i przypisz ją do zapisanego stamp_id
            self.stamps[(x, y)] = stamp_id

class UiPen(Pen):

    def __init__(self):
        super().__init__()
        self.font = ("Courier", 30, "normal")

    def draw_ui_area(self):
        "Rysuj obramowanie interfejsu użytkownika"
        self.pensize(2)
        x = 0.9 * SCREEN_WIDTH / 2
        top_y = 0.98 * SCREEN_HEIGHT / 2
        bottom_y = top_y - 1.5 * CELL_SIZE
        self.goto(x, top_y)
        self.pendown()
        self.goto(-x, top_y)
        self.goto(-x, bottom_y)
        self.goto(x, bottom_y)
        self.goto(x, top_y)


    def write_score(self, score, lives, pellet_stamps, power_stamps):
        "Wypisz wynik na ekranie"
        self.clear()
        msg = f"Score: {score}"
        self.goto(-0.7 * SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 2 * CELL_SIZE)
        self.write(msg, False, "left", self.font)
        # Koniec gry
        if lives <= 0:
            self.clear()
            self.color("red")
            self.write(
                f"Game Over!     Final Score: {score}", False, "left", self.font)
        # Wygrana gra
        if len(pellet_stamps) == 0 and len(power_stamps) == 0:
            self.clear()
            self.color("yellow")
            self.write(
                f"You Won!     Final Score: {score}", False, "left", self.font)


    def write_lives(self, lives, pellet_stamps, power_stamps):
        "Wypisz życia na ekranie"
        self.clear()
        msg = f"Lives: {lives}"
        self.goto(0.7 * SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 2 * CELL_SIZE)
        self.write(msg, False, "right", self.font)   
        if lives == 0 or (len(pellet_stamps) == 0 and len(power_stamps) == 0):
            self.reset()