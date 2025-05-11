import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List
from grid_map import GridMap
from a_star import a_star_search
from llm_astar import llm_astar
from matplotlib.animation import FuncAnimation
from matplotlib.backend_bases import MouseEvent
from pathlib import Path

# -------------------------
# Maze image loader
# -------------------------
def load_maze_from_image(image_path: str, threshold: int = 127) -> GridMap:
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"❌ Could not load image: {image_path}")
    if img.shape[0] > 100 or img.shape[1] > 100:
        img = cv2.resize(img, (40, 40), interpolation=cv2.INTER_NEAREST)
    _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    binary = (binary == 0).astype(np.uint8)
    h, w = binary.shape
    gmap = GridMap((0, w), (0, h))
    for y in range(h):
        for x in range(w):
            if binary[y, x] == 1:
                gmap.set_occupied(x, h - y - 1)
    return gmap

# -------------------------
# Interactive selector
# -------------------------
def select_points_interactively(grid: GridMap) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    selected: List[Tuple[int, int]] = []

    def onclick(event: MouseEvent):
        if event.xdata is None or event.ydata is None:
            return
        x, y = int(event.xdata), int(event.ydata)
        if grid.in_bounds(x, y) and not grid.is_occupied(x, y):
            selected.append((x, y))
            print(f"✅ Selected: ({x}, {y})")
            ax.plot(x + 0.5, y + 0.5, 'go' if len(selected) == 1 else 'ro', markersize=10)
            plt.draw()
        if len(selected) == 2:
            plt.close()

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(grid.x_min, grid.x_max)
    ax.set_ylim(grid.y_min, grid.y_max)
    ax.set_aspect('equal')
    ax.set_title("🖱️ Click Start (Green) and Goal (Red)")
    ax.grid(True)

    for x in range(grid.x_min, grid.x_max):
        for y in range(grid.y_min, grid.y_max):
            if grid.is_occupied(x, y):
                ax.add_patch(plt.Rectangle((x, y), 1, 1, color='black'))

    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    fig.canvas.mpl_disconnect(cid)

    if len(selected) != 2:
        raise RuntimeError("Start and goal not selected!")

    return selected[0], selected[1]

# -------------------------
# Dual Animation
# -------------------------
def animate_dual_paths(grid: GridMap,
                       astar_path: List[Tuple[int, int]],
                       llm_path: List[Tuple[int, int]],
                       start: Tuple[int, int],
                       goal: Tuple[int, int]):

    fig, axs = plt.subplots(1, 2, figsize=(14, 7))
    fig.suptitle("Simultaneous A* vs LLM-A* Path Simulation")

    for ax in axs:
        ax.set_xlim(grid.x_min, grid.x_max)
        ax.set_ylim(grid.y_min, grid.y_max)
        ax.set_aspect('equal')
        ax.grid(True)
        ax.plot(start[0] + 0.5, start[1] + 0.5, 'go', label="Start", markersize=8)
        ax.plot(goal[0] + 0.5, goal[1] + 0.5, 'ro', label="Goal", markersize=8)
        for x in range(grid.x_min, grid.x_max):
            for y in range(grid.y_min, grid.y_max):
                if grid.is_occupied(x, y):
                    ax.add_patch(plt.Rectangle((x, y), 1, 1, color='black'))
        ax.legend(loc="upper left")

    # Show full paths
    if astar_path:
        px, py = zip(*[(x + 0.5, y + 0.5) for x, y in astar_path])
        axs[0].plot(px, py, 'm--', alpha=0.5, label="A* Path")
        axs[0].set_title("A*")

    if llm_path:
        px, py = zip(*[(x + 0.5, y + 0.5) for x, y in llm_path])
        axs[1].plot(px, py, 'cyan', alpha=0.5, label="LLM-A* Path")
        axs[1].set_title("LLM-A*")

    # Animated robots
    robot0, = axs[0].plot([], [], 'mo', markersize=8)
    trail0, = axs[0].plot([], [], 'm-', linewidth=2)
    robot1, = axs[1].plot([], [], 'bo', markersize=8)
    trail1, = axs[1].plot([], [], 'b-', linewidth=2)

    t0x, t0y = [], []
    t1x, t1y = [], []

    def update(frame):
        if frame < len(astar_path):
            x0, y0 = astar_path[frame]
            t0x.append(x0 + 0.5)
            t0y.append(y0 + 0.5)
            robot0.set_data(x0 + 0.5, y0 + 0.5)
            trail0.set_data(t0x, t0y)
        if frame < len(llm_path):
            x1, y1 = llm_path[frame]
            t1x.append(x1 + 0.5)
            t1y.append(y1 + 0.5)
            robot1.set_data(x1 + 0.5, y1 + 0.5)
            trail1.set_data(t1x, t1y)
        return robot0, robot1, trail0, trail1

    total_frames = max(len(astar_path), len(llm_path))
    ani = FuncAnimation(fig, update, frames=total_frames, interval=300, repeat=False)
    plt.show()

# -------------------------
# Compare + Animate
# -------------------------
def compare_astar_vs_llmastar(grid: GridMap,
                               start: Tuple[int, int],
                               goal: Tuple[int, int],
                               model: str = "mistral"):

    print("\n🔵 Running baseline A*...")
    t0 = time.time()
    pure_path, pure_nodes = a_star_search(grid, start, goal)
    t1 = time.time()

    print("\n🟡 Running LLM-A*...")
    t2 = time.time()
    llm_path, waypoints = llm_astar(grid, start, goal, model=model)
    t3 = time.time()

    print("\n📊 Comparison Summary:")
    if pure_path:
        print(f"✅ A* Path Length:     {len(pure_path)}")
        print(f"🔹 A* Nodes Explored:  {pure_nodes}")
        print(f"⏱️  A* Time Taken:      {t1 - t0:.3f}s")
    else:
        print("❌ A* failed to find a path.")

    if llm_path:
        print(f"\n✅ LLM-A* Path Length: {len(llm_path)}")
        print(f"⭐ LLM Waypoints Used:  {len(waypoints)}")
        print(f"⏱️  LLM-A* Time Taken:  {t3 - t2:.3f}s")
    else:
        print("❌ LLM-A* failed to find a path.")

    if pure_path or llm_path:
        animate_dual_paths(grid, pure_path, llm_path, start, goal)

# -------------------------
# 🟢 MAIN
# -------------------------
if __name__ == "__main__":
    image_path = "/home/shrirag10/llm_astar_sim/20_ by_ 20_orthogonalmaze.png"  # Replace if needed
    if not Path(image_path).exists():
        print(f"❌ Maze image not found at {image_path}")
        exit(1)

    gmap = load_maze_from_image(image_path)
    start, goal = select_points_interactively(gmap)
    compare_astar_vs_llmastar(gmap, start, goal)
