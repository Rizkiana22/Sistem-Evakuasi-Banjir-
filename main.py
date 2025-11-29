import pygame
import sys
import config
from models import Environment
import algorithms as algo
import random

# ==========================================
# INISIALISASI
# ==========================================
pygame.init()
screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
pygame.display.set_caption("Simulasi Evakuasi Modular")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 16)

# Setup Environment
env = Environment(config.GRID_SIZE, config.GRID_SIZE)

# State Global
agent_cell = None
goal_cell = None
path = []

status_message = ""

running_sim = False
flood_timer = 0
move_timer = 0


def random_env(env, wall_prob=0.15, water_prob=0.05):
    """Random tembok dan sumber air, tapi tetap bisa di-edit manual."""
    env.flood_q.clear()

    for r in range(env.rows):
        for c in range(env.cols):
            cell = env.get_cell(r, c)

            cell.blocked = False
            cell.is_source = False
            cell.reset_flood()

            # acak tembok
            if random.random() < wall_prob:
                cell.blocked = True
                continue

            # sumber air acak
            if random.random() < water_prob:
                cell.is_source = True
                cell.time_flooded = 0
                cell.status = config.FloodStatus.SHALLOW
                cell.cost = config.COST_MAP[config.FloodStatus.SHALLOW]
                env.flood_q.append(cell)


# ==========================================
# FUNGSI GAMBAR UI
# ==========================================

def draw_ui():
    screen.fill(config.COLOR_BG)

    # 1. Gambar Grid & Status Cell
    for r in range(env.rows):
        for c in range(env.cols):
            cell = env.grid[r][c]
            rect = pygame.Rect(
                c * (config.CELL_SIZE + config.MARGIN),
                r * (config.CELL_SIZE + config.MARGIN),
                config.CELL_SIZE,
                config.CELL_SIZE,
            )

            # Tentukan Warna berdasarkan Status
            color = config.COLOR_DRY
            if cell.blocked:
                color = config.COLOR_WALL
            elif cell.status == config.FloodStatus.SHALLOW:
                color = config.COLOR_SHALLOW
            elif cell.status == config.FloodStatus.MEDIUM:
                color = config.COLOR_MEDIUM
            elif cell.status == config.FloodStatus.DEEP:
                color = config.COLOR_DEEP

            pygame.draw.rect(screen, color, rect)

            # Tanda Sumber Air
            if cell.is_source:
                pygame.draw.circle(screen, config.COLOR_SOURCE, rect.center, 5)

    # 2. Gambar Jalur (Path)
    if path and len(path) > 1:
        points = []
        for p in path:
            px = p.c * (config.CELL_SIZE + config.MARGIN) + \
                config.CELL_SIZE // 2
            py = p.r * (config.CELL_SIZE + config.MARGIN) + \
                config.CELL_SIZE // 2
            points.append((px, py))
        pygame.draw.lines(screen, config.COLOR_PATH, False, points, 3)

    # 3. Gambar Goal (Tujuan)
    if goal_cell:
        rect = pygame.Rect(
            goal_cell.c * (config.CELL_SIZE + config.MARGIN),
            goal_cell.r * (config.CELL_SIZE + config.MARGIN),
            config.CELL_SIZE,
            config.CELL_SIZE,
        )
        pygame.draw.rect(screen, config.COLOR_GOAL, rect, 4)
        txt = font.render("G", True, (0, 0, 0))
        screen.blit(txt, (rect.x + 12, rect.y + 10))

    # 4. Gambar Agent (Orang)
    if agent_cell:
        cx = agent_cell.c * (config.CELL_SIZE +
                             config.MARGIN) + config.CELL_SIZE // 2
        cy = agent_cell.r * (config.CELL_SIZE +
                             config.MARGIN) + config.CELL_SIZE // 2
        pygame.draw.circle(
            screen, config.COLOR_AGENT, (cx, cy), config.CELL_SIZE // 3
        )
        pygame.draw.circle(
            screen, (0, 0, 0), (cx, cy), config.CELL_SIZE // 3, 2
        )
        txt = font.render("S", True, (0, 0, 0))
        screen.blit(txt, (cx - 5, cy - 8))

    # 5. Gambar Sidebar Teks
    info_x = config.GRID_SIZE * (config.CELL_SIZE + config.MARGIN) + 20
    y = 20
    texts = [
        f"Time Step: {env.timestep}",
        "STATUS: " + ("RUNNING" if running_sim else "PAUSED"),
        "",
        "[L-Click]  : Set Start (Agent)",
        "[R-Click]  : Set Goal",
        "[Shift+Click]: Sumber Air ON/OFF",
        "[Ctrl+Click] : Tembok ON/OFF",
        "[SPACE]    : Run/Pause",
        "[R]        : Reset ",
        "[T]        : Random Map",
    ]
    for t in texts:
        col = ((0, 255, 0) if "RUNNING" in t and running_sim else config.COLOR_TEXT)
        label = font.render(t, True, col)
        screen.blit(label, (info_x, y))
        y += 25

    # 6. Status Message (Agent terjebak / Evakuasi berhasil)
    if status_message:
        msg_color = (255, 50, 50)
        label = font.render(status_message, True, msg_color)
        screen.blit(label, (info_x, y + 20))


# ==========================================
# MAIN LOOP
# ==========================================
running = True
while running:
    dt = clock.tick(config.FPS)
    current_time = pygame.time.get_ticks()

    # --- INPUT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            c = mx // (config.CELL_SIZE + config.MARGIN)
            r = my // (config.CELL_SIZE + config.MARGIN)
            cell = env.get_cell(r, c)

            if not cell:
                continue

            mods = pygame.key.get_mods()

            # ctrl + klik untuk set/unset tembok
            if mods & pygame.KMOD_CTRL:
                cell.blocked = not cell.blocked
                if cell.blocked:
                    cell.is_source = False
                    cell.reset_flood()
                else:
                    cell.reset_flood()
                path = algo.run_astar(env, agent_cell, goal_cell)
                continue

            # shift + klik untuk set/unset sumber air
            if mods & pygame.KMOD_SHIFT:
                cell.is_source = not cell.is_source
                if cell.is_source:
                    cell.time_flooded = 0
                    cell.status = config.FloodStatus.SHALLOW
                    cell.cost = config.COST_MAP[config.FloodStatus.SHALLOW]
                    env.flood_q.append(cell)
                else:
                    cell.reset_flood()
                path = algo.run_astar(env, agent_cell, goal_cell)
                continue

            # klik kiri untuk set start
            if event.button == 1:
                agent_cell = cell
                cell.blocked = False
                path = algo.run_astar(env, agent_cell, goal_cell)

            # klik kanan untuk set goal
            elif event.button == 3:
                goal_cell = cell
                cell.blocked = False
                path = algo.run_astar(env, agent_cell, goal_cell)

        # untuk memulai simulasi
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                running_sim = not running_sim

            # untuk merestart map
            elif event.key == pygame.K_r:
                env.reset_simulation()

                # membersihkan tembok, sumer air, path, agent dan goal
                for r in range(env.rows):
                    for c in range(env.cols):
                        cell = env.get_cell(r, c)
                        cell.blocked = False
                        cell.is_source = False
                        cell.reset_flood()
                agent_cell = None
                goal_cell = None
                running_sim = False
                path = []
            # untuk mengacak map
            elif event.key == pygame.K_t:
                random_env(env)

    # --- SIMULATION LOGIC ---
    if running_sim:
        # 1. Update Banjir (BFS)
        if current_time - flood_timer > config.FLOOD_INTERVAL:
            flood_timer = current_time
            algo.run_flood_step(env)
            path = algo.run_astar(env, agent_cell, goal_cell)

        # 2. Gerakan Agen
        if current_time - move_timer > config.MOVE_INTERVAL:
            move_timer = current_time

            if not path:
                status_message = "Agent terjebak!"
                running_sim = False
            elif len(path) > 1:
                next_step = path[1]
                agent_cell = next_step
                path = algo.run_astar(env, agent_cell, goal_cell)
                if agent_cell == goal_cell:
                    status_message = "Evakuasi Berhasil!"
                    running_sim = False

    draw_ui()
    pygame.display.flip()

pygame.quit()
sys.exit()
