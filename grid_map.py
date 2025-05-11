import numpy as np
import matplotlib.pyplot as plt
from typing import List, Tuple
import cv2


class GridMap:
    def __init__(self, x_range: Tuple[int, int], y_range: Tuple[int, int]):
        self.x_min, self.x_max = x_range
        self.y_min, self.y_max = y_range
        self.width = self.x_max - self.x_min
        self.height = self.y_max - self.y_min
        self.grid = np.zeros((self.width, self.height), dtype=np.int8)

        self.vertical_barriers = []
        self.horizontal_barriers = []

    def add_vertical_barrier(self, x: int, y_start: int, y_end: int):
        self.vertical_barriers.append([x, y_start, y_end])
        for y in range(y_start, y_end + 1):
            self.set_occupied(x, y)

    def add_horizontal_barrier(self, y: int, x_start: int, x_end: int):
        self.horizontal_barriers.append([y, x_start, x_end])
        for x in range(x_start, x_end + 1):
            self.set_occupied(x, y)

    def in_bounds(self, x: int, y: int) -> bool:
        return self.x_min <= x < self.x_max and self.y_min <= y < self.y_max

    def is_occupied(self, x: int, y: int) -> bool:
        if not self.in_bounds(x, y):
            return True
        return self.grid[x - self.x_min, y - self.y_min] == 1

    def set_occupied(self, x: int, y: int):
        if self.in_bounds(x, y):
            self.grid[x - self.x_min, y - self.y_min] = 1

    def load_from_image(self, image_path: str, threshold: int = 128):
        """
        Load a maze image and convert it into an occupancy grid.
        Black (or dark) pixels are considered walls/obstacles.
        """
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError(f"Failed to load image: {image_path}")
        
        img = cv2.resize(img, (self.width, self.height), interpolation=cv2.INTER_NEAREST)
        self.grid = (img < threshold).astype(np.int8)

        self.vertical_barriers = []
        self.horizontal_barriers = []

    def visualize(self, start: Tuple[int, int], goal: Tuple[int, int],
                  path: List[Tuple[int, int]] = None,
                  waypoints: List[Tuple[int, int]] = None):
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.set_aspect('equal')
        ax.set_xlim(self.x_min, self.x_max)
        ax.set_ylim(self.y_min, self.y_max)

        # Draw obstacles
        for x in range(self.x_min, self.x_max):
            for y in range(self.y_min, self.y_max):
                if self.is_occupied(x, y):
                    ax.add_patch(plt.Rectangle((x, y), 1, 1, color='black'))

        # Draw start/goal
        ax.plot(start[0] + 0.5, start[1] + 0.5, 'go', markersize=10, label='Start')
        ax.plot(goal[0] + 0.5, goal[1] + 0.5, 'ro', markersize=10, label='Goal')

        # Draw path
        if path:
            px, py = zip(*[(x + 0.5, y + 0.5) for x, y in path])
            ax.plot(px, py, color='blue', linewidth=2, label='Path')

        # Draw waypoints
        if waypoints:
            for wp in waypoints:
                ax.plot(wp[0] + 0.5, wp[1] + 0.5, 'y*', markersize=12)
            ax.plot([], [], 'y*', label='LLM Waypoint')

        ax.legend()
        plt.grid(True)
        plt.title("LLM-A* Map Environment")
        plt.show()
