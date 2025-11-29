import math
import heapq
import config

# =====================================================================
# KONSTANTA — 8 ARAH (North, South, East, West + Diagonal)
# =====================================================================

NEIGHBORS_8 = [
    (-1, 0), (1, 0),  # Atas, Bawah
    (0, -1), (0, 1),  # Kiri, Kanan
    (-1, -1), (-1, 1), (1, -1), (1, 1)  # Diagonal
]

# =====================================================================
# BFS — Flood Spreading
# =====================================================================


def run_flood_step(env):
    """Satu langkah penyebaran air berbasis BFS (level-order)."""

    env.timestep += 1

    # --------------------------------------------------
    # 1. Update kedalaman air yang sudah ada
    # --------------------------------------------------
    for r in range(env.rows):
        for c in range(env.cols):
            cell = env.grid[r][c]
            if cell.status != config.FloodStatus.DRY:
                cell.update_status(env.timestep)

    # --------------------------------------------------
    # 2. Penyebaran air (BFS queue)
    # --------------------------------------------------
    current_q_len = len(env.flood_q)

    for _ in range(current_q_len):
        current_cell = env.flood_q.popleft()

        for dr, dc in NEIGHBORS_8:
            nr, nc = current_cell.r + dr, current_cell.c + dc
            neighbor = env.get_cell(nr, nc)

            # Syarat menyebar
            if (neighbor
                and not neighbor.blocked
                    and neighbor.time_flooded == -1):

                neighbor.status = config.FloodStatus.SHALLOW
                neighbor.cost = config.COST_MAP[config.FloodStatus.SHALLOW]
                neighbor.time_flooded = env.timestep

                env.flood_q.append(neighbor)

# =====================================================================
# A* — Pathfinding (Safety + Speed)
# =====================================================================


def heuristic(a, b):
    """Euclidean distance untuk smooth path."""
    return math.hypot(a.r - b.r, a.c - b.c)


def run_astar(env, start, goal):
    """A* mencari jalur paling aman & efisien."""

    # --------------------------------------------------
    # Validasi dasar
    # --------------------------------------------------
    if not start or not goal:
        return []
    if start.blocked or goal.blocked:
        return []
    if start.status == config.FloodStatus.DEEP:
        return []  # Agen tewas / trapped

    # --------------------------------------------------
    # Struktur A*
    # --------------------------------------------------
    open_set = []
    heapq.heappush(open_set, (0, start.r, start.c))
    open_set_hash = {start}

    came_from = {}

    g_score = {node: float("inf") for row in env.grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in env.grid for node in row}
    f_score[start] = heuristic(start, goal)

    # --------------------------------------------------
    # Loop utama A*
    # --------------------------------------------------
    while open_set:
        _, cr, cc = heapq.heappop(open_set)
        current = env.grid[cr][cc]

        if current in open_set_hash:
            open_set_hash.remove(current)

        # --------------------------------------------------
        # Cek apakah mencapai tujuan
        # --------------------------------------------------
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        # --------------------------------------------------
        # Cek semua tetangga (8 arah)
        # --------------------------------------------------
        for dr, dc in NEIGHBORS_8:
            neighbor = env.get_cell(current.r + dr, current.c + dc)
            if not neighbor:
                continue
            if neighbor.blocked:
                continue
            if neighbor.status == config.FloodStatus.DEEP:
                continue  # Terlalu berbahaya dilewati

            # Biaya masuk ke sel tetangga dipengaruhi kedalaman air
            is_diagonal = (dr != 0 and dc != 0)
            base_cost = neighbor.cost
            move_cost = math.sqrt(2) if is_diagonal else base_cost
            tentative_g = g_score[current] + move_cost

            if tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g

                f = tentative_g + heuristic(neighbor, goal)
                f_score[neighbor] = f

                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f, neighbor.r, neighbor.c))
                    open_set_hash.add(neighbor)

    return []  # Tidak ada jalur
