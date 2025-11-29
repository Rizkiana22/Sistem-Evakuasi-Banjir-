from collections import deque
import config


class Cell:
    def __init__(self, r, c):
        self.r = r
        self.c = c
        self.blocked = False
        self.status = config.FloodStatus.DRY
        self.cost = config.COST_MAP[config.FloodStatus.DRY]
        self.time_flooded = -1
        self.is_source = False

    def reset_flood(self):
        """Mengembalikan status banjir ke awal (kering/sumber)"""
        self.status = config.FloodStatus.DRY
        self.cost = config.COST_MAP[config.FloodStatus.DRY]
        self.time_flooded = -1

        # Jika ini sumber air, set inisialnya
        if self.is_source:
            self.status = config.FloodStatus.SHALLOW
            self.cost = config.COST_MAP[config.FloodStatus.SHALLOW]
            self.time_flooded = 0

    def update_status(self, timestep):
        """Logika kenaikan level air seiring waktu"""
        if self.time_flooded == -1:
            return

        duration = timestep - self.time_flooded

        if duration < 4:
            self.status = config.FloodStatus.SHALLOW
        elif duration < 8:
            self.status = config.FloodStatus.MEDIUM
        else:
            self.status = config.FloodStatus.DEEP

        self.cost = config.COST_MAP[self.status]


class Environment:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # Grid 2D array
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]
        self.flood_q = deque()
        self.timestep = 0

    def get_cell(self, r, c):
        """Helper aman untuk mengambil sel tanpa error index out of bounds"""
        if 0 <= r < self.rows and 0 <= c < self.cols:
            return self.grid[r][c]
        return None

    def reset_simulation(self):
        """Reset total semua variabel simulasi"""
        self.timestep = 0
        self.flood_q.clear()
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                cell.reset_flood()
                if cell.is_source:
                    self.flood_q.append(cell)
