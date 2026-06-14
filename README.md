# Pac-Man w Pythonie

Gra Pac-Man zaimplementowana w Pythonie z wykorzystaniem biblioteki `turtle` do renderowania grafiki.

## Uruchomienie

```bash
python main.py
```

## Sterowanie

| Klawisz | Akcja         |
|---------|---------------|
| Strzałka prawa  | Ruch w prawo  |
| Strzałka lewa   | Ruch w lewo   |
| Strzałka górna  | Ruch w górę   |
| Strzałka dolna  | Ruch w dół    |

## Opis plików

### `main.py`
Główny plik uruchamiający grę. Zawiera:
- `init_screen()` – konfiguruje okno gry (rozmiar, kolor tła, tytuł)
- `bind_controls()` – przypisuje klawisze strzałek do sterowania graczem
- `game_loop()` – pętla gry wykonywana co ~16ms (60 FPS), aktualizuje pozycję gracza i odświeża ekran
- `main()` – inicjalizuje wszystkie elementy gry i uruchamia pętlę główną

### `actors.py`
Definiuje klasy postaci gry (aktorów):
- `Actor` – klasa bazowa dla wszystkich postaci, dziedziczy po `turtle.Turtle`; ukrywa kursor i ustawia szybkość rysowania na maksymalną
- `Player` – klasa gracza (Pac-Man); żółte kółko poruszające się po ekranie z teleportacją przez krawędzie, posiada życia (3) i punkty (0)

### `constants.py`
Plik ze stałymi konfiguracyjnymi całej gry:
- Rozmiar komórki siatki (`CELL_SIZE = 30`)
- Wymiary ekranu (`SCREEN_WIDTH = 1000`, `SCREEN_HEIGHT = 850`)
- Parametry siatki labiryntu (`GRID_ROWS`, `GRID_COLUMNS`)
- Pozycja startowa labiryntu na ekranie (`MAZE_LEVEL_START_X/Y`)
- Prędkość gracza (`PLAYER_MOVE_SPEED = 5`)

### `mazes.py`
Przechowuje dane labiryntu i logikę ich przetwarzania:
- `maze_level_1` – tekstowa mapa labiryntu, gdzie `X` = ściana, `.` = kulka, `O` = kulka mocy, spacja = pusty korytarz
- `calculate_maze_data()` – przetwarza tekstową mapę na listy współrzędnych ekranowych ścian, kulek i kulek mocy

### `renderer.py`
Odpowiada za renderowanie (rysowanie) elementów labiryntu na ekranie:
- `Pen` – klasa bazowa dla elementów rysujących; wczytuje dane labiryntu przy inicjalizacji
- `Wall` – rysuje niebieskie kwadratowe ściany labiryntu
- `Pellet` – rysuje małe złote kulki do zbierania przez Pac-Mana
- `PowerPellet` – rysuje większe zielone kulki mocy dające specjalne zdolności
