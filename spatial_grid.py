"""Spatial grid for O(1) collision detection instead of O(n)"""

from constants import CELL_SIZE

class SpatialGrid:
    """Grid-based spatial hash for fast wall collision queries"""

    def __init__(self, walls, grid_cell_size=CELL_SIZE):
        """
        Initialize grid with walls.
        grid_cell_size: size of each grid cell (default: CELL_SIZE = 30)
        """
        self.cell_size = grid_cell_size
        self.grid = {}  # {(grid_x, grid_y): [walls in this cell]}

        # Populate grid
        for wall_x, wall_y in walls:
            grid_x = int(wall_x // grid_cell_size)
            grid_y = int(wall_y // grid_cell_size)
            grid_key = (grid_x, grid_y)

            if grid_key not in self.grid:
                self.grid[grid_key] = []
            self.grid[grid_key].append((wall_x, wall_y))

    def get_nearby_walls(self, actor_x, actor_y, radius_cells=2):
        """
        Get walls within radius_cells of actor position.
        Much faster than iterating all walls.

        radius_cells=2 means check 5x5 grid (2 cells in each direction + center)
        """
        grid_x = int(actor_x // self.cell_size)
        grid_y = int(actor_y // self.cell_size)

        nearby_walls = []
        for dx in range(-radius_cells, radius_cells + 1):
            for dy in range(-radius_cells, radius_cells + 1):
                grid_key = (grid_x + dx, grid_y + dy)
                if grid_key in self.grid:
                    nearby_walls.extend(self.grid[grid_key])

        return nearby_walls
