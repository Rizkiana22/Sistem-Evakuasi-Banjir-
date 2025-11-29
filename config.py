from enum import Enum

# ==========================================
# KONFIGURASI UMUM
# ==========================================
GRID_SIZE = 15
CELL_SIZE = 40
MARGIN = 1
WINDOW_WIDTH = GRID_SIZE * (CELL_SIZE + MARGIN) + 350
WINDOW_HEIGHT = max(GRID_SIZE * (CELL_SIZE + MARGIN), 400)
FPS = 60

# Kecepatan Simulasi (milidetik)
FLOOD_INTERVAL = 600  # Air menyebar
MOVE_INTERVAL = 400   # Agen bergerak

# ==========================================
# DEFINISI WARNA (RGB)
# ==========================================
COLOR_BG = (30, 30, 30)
COLOR_WALL = (80, 80, 80)
COLOR_DRY = (245, 245, 245)
COLOR_SHALLOW = (135, 206, 250)
COLOR_MEDIUM = (30, 144, 255)
COLOR_DEEP = (0, 0, 139)
COLOR_GOAL = (220, 20, 60)
COLOR_PATH = (255, 215, 0)
COLOR_SOURCE = (0, 255, 255)
COLOR_AGENT = (255, 255, 255)
COLOR_TEXT = (255, 255, 255)

# ==========================================
# STATUS & COST MAP
# ==========================================


class FloodStatus(Enum):
    DRY = 0
    SHALLOW = 1
    MEDIUM = 2
    DEEP = 3


COST_MAP = {
    FloodStatus.DRY: 1.0,
    FloodStatus.SHALLOW: 5.0,
    FloodStatus.MEDIUM: 20.0,
    FloodStatus.DEEP: float('inf')
}
