import turtle
from mazes import calculate_maze_data, maze_level_1


class Pen(turtle.Turtle):

    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.speed(0)
        # Pobieranie wszystkich współrzędnych z poziomu labiryntu
        self.walls, self.pellets, self.power_pellets = calculate_maze_data(
            maze_level_1)


class Wall(Pen):

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.shapesize(1.2)
        self.pencolor("white")
        self.fillcolor("dodger blue")

    def draw(self):
        "Rysowanie ściany na ekranie"
        for x, y in self.walls:
            self.goto(x, y)
            self.stamp()


class Pellet(Pen):
    "Kulka dla Pac-Mana do zjedzenia"

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(0.35, 0.35)
        self.pencolor("white")
        self.fillcolor("gold")

    def draw(self):
        "Rysowanie kulki na ekranie"
        for x, y in self.pellets:
            self.goto(x, y)
            # Stemplowanie kulki
            self.stamp()

class PowerPellet(Pen):
    
    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.shapesize(0.8, 0.8)
        self.pencolor("white")
        self.fillcolor("chartreuse")

    def draw(self):
        "Rysowanie kulki mocy na ekranie"
        for x, y in self.power_pellets:
            self.goto(x, y)
            # Stemplowanie kulki mocy
            self.stamp()