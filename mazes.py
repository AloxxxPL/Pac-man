from constants import (CELL_SIZE, MAZE_GRID_ROWS, MAZE_GRID_COLUMNS, MAZE_LEVEL_START_X, MAZE_LEVEL_START_Y)

# Poziom labiryntu #1:
# Liczba wierszy musi być równa liczbie wierszy siatki minus 2 wiersze dla interfejsu użytkownika
# Liczba kolumn musi być identyczna z liczbą kolumn siatki
maze_level_1 = [
    "XXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXX",
    "X..............................OX",
    "X.XXX.XXX.XXXXXX.XXXXXX.XXX.XXX.X",
    "X.X X.X X.X    X.X    X.X X.X X.X",
    "X.XXX.X X.XXXXXX.XXXXXX.X X.XXX.X",
    "X.....XXX.X....X.X....X.XXX.....X",
    "XXXXX.......XX.X.X.XX.......XXXXX",
    "X.....XXXXX...........XXXXX.....X",
    "X.XXX.......XXXXXXXXX.......XXX.X",
    "X.....XXXXX...........XXXXX.....X",
    "X.XXX...O...XXXX.XXXX.......XXX.X",
    "X.X X.XXXXX.X  X.X  X.XXXXX.X X.X",
    "X.X X.X   X.X  X.X  X.X   X.X X.X",
    "X.X X.X   X.X  X.X  X.X   X.X X.X",
    "X.X X.XXXXX.X  X.X  X.XXXXX.X X.X",
    "X.XXX.......XXXX.XXXX...O...XXX.X",
    "X.....XXXXX...........XXXXX.....X",
    "X.XXX.......XXXXXXXXX.......XXX.X",
    "X.....XXXXX...........XXXXX.....X",
    "XXXXX.......XX.X.X.XX.......XXXXX",
    "X.....XXX.X....X.X....X.XXX.....X",
    "X.XXX.X X.XXXXXX.XXXXXX.X X.XXX.X",
    "X.X X.X X.X    X.X    X.X X.X X.X",
    "X.XXX.XXX.XXXXXX.XXXXXX.XXX.XXX.X",
    "XO..............................X",
    "XXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXX"
]

# Poziom labiryntu #2:
maze_level_2 = [
    "XXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXX",
    "XO.............................OX",
    "X.XXXXX.XXXXX.XXXXX.XXXXX.XXXXX.X",
    "X.X   X.X   X.X   X.X   X.X   X.X",
    "X.X XXX.X XXX.X XXX.X XXX.X XXX.X",
    "X.X   X   X   X   X   X   X   X.X",
    "X.XXXXX.XXXXX.XXXXX.XXXXX.XXXXX.X",
    "X.......................O.......X",
    "XXXXX.XXXXXXXXXXXXX.XXXXXXXXXXXXX",
    "X.....X.....X.....X.X.....X.....X",
    "X.XXX.X.XXX.X.XXX.X.X.XXX.X.XXX.X",
    "X.X X.X.X X.X.X X.X.X.X X.X.X X.X",
    "X.X X.X.X X.X.X X.X.X.X X.X.X X.X",
    "X.X XXX.X XXX.X XXX.X XXX.X XXX.X",
    "X.X   X   X   X   X   X   X   X.X",
    "X.XXX.XXXXX.XXXXX.XXXXX.XXXXX.X.X",
    "X.X X.X   X   X   X   X   X X.X  ",
    "X.X X.X.XXX.XXXXX.XXXXX.XXX.X.X X",
    "X.X   X.X     X     X   X   X.X  ",
    "XXX XXX.X XXXXX XXX XXX X X XXX X",
    "X.X   X.X         X X.X     X.X  ",
    "X.X XXX.X.X XXX XXX XXX X.X XXX.X",
    "X.X X X.X.X X     X X X.X.X X X.X",
    "X.X XXX.X.X XXXXX X X.X.X XXX.X.X",
    "XO.....X.....X...X.X.....X.....OX",
    "XXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXX"
]

# Poziom labiryntu #3:
maze_level_3 = [
    "XXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXX",
    "XO...................O.........OX",
    "X.XXX.XXX.XXX.XXX.XXX.XXX.XXX.X.X",
    "X.X X.X X.X X.X X.X X.X X.X X X.X",
    "X.X XXX.X XXX.X XXX.X XXX.X XXX X",
    "X.X   X.X X   X   X X   X.X X   X",
    "X.XXX X.X X.XXX.X.X.XXX.X.X X.XXX",
    "X.  X X.X X.  X X X.  X X.X X.  X",
    "XX.X XXX.X X.X XXX X.X XXX.X X.X ",
    "X..X     X X X   X X X     X X X ",
    "X.XXX.XXX.X X XXX.X X.XXX.X XXX.X",
    "X.X   X   X X X   X X.X   X X   X",
    "X.X XXX.XXX.X X XXX.X.X XXX XXX.X",
    "X.X X   X   X X X   X.X X   X   X",
    "X.X X.XXX.XXX.X XXX.X X X.XXX.XXX",
    "X.X X.X   X   X X   X X X.X   X  ",
    "X.X X.X.XXX.XXX X XXX XXX.X XXX.X",
    "X.X X X.X   X   X X   X   X X   X",
    "X.X X XXX.X XXX.X X.XXX.X XXX.X.X",
    "X.X X   X X X   X X.X   X   X X.X",
    "X.XXX.X XXX X.XXX X.X.XXX.XXX X.X",
    "X.X   X X   X.X   X X.X   X   X.X",
    "X.X XXX X.XXX.X XXX X.X XXX.XXX.X",
    "X....X...X.....X.....X.....X.....",
    "XO.............................OX",
    "XXXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXX"
]

maze_levels = [maze_level_1, maze_level_2, maze_level_3]


def calculate_maze_data(maze_level):
    """Obliczanie współrzędnych labiryntu"""
    walls = []
    pellets = []
    power_pellets = []
    # Iteracja po każdym wierszu poziomu labiryntu
    for row in range(MAZE_GRID_ROWS):
        # Iteracja po każdej kolumnie poziomu labiryntu
        for column in range(MAZE_GRID_COLUMNS):
            # Przechowywanie współrzędnych znaku[wiersz][kolumna]
            character = maze_level[row][column]
            # Numeracja wierszy od 0 do 25 (26 nie wliczone)
            # Numeracja kolumn od 0 do 32 (33 nie wliczone)
            # Poniższe wzory x,y uwzględniają pozycję licząc od 0
            character_x = MAZE_LEVEL_START_X + CELL_SIZE * column
            character_y = MAZE_LEVEL_START_Y - CELL_SIZE * row
            # Jeśli znak = "X" – ściana, dodaj współrzędne do listy ścian
            if character == "X":
                walls.append((character_x, character_y))
            # Jeśli znak = "." – kulka, dodaj współrzędne do listy kuleczek
            elif character == ".":
                pellets.append((character_x, character_y))
            elif character == "O":
                power_pellets.append((character_x, character_y))
    # Zwróć listy ze wszystkimi współrzędnymi.
    # Umożliwia to późniejsze pobranie tych danych w innych plikach i zapisanie jako zmienna
    return walls, pellets, power_pellets
