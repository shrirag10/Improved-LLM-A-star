import heapq
from typing import Tuple, List, Dict, Optional
from grid_map import GridMap
import math


def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> float:
    # Euclidean distance
    return math.hypot(b[0] - a[0], b[1] - a[1])


def get_neighbors(pos: Tuple[int, int]) -> List[Tuple[int, int]]:
    x, y = pos
    # 4-connected grid (no diagonals)
    return [(x + dx, y + dy) for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]]


def reconstruct_path(came_from: Dict[Tuple[int, int], Tuple[int, int]],
                     current: Tuple[int, int]) -> List[Tuple[int, int]]:
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]  # reverse the path


def a_star_search(grid: GridMap,
                  start: Tuple[int, int],
                  goal: Tuple[int, int]) -> Tuple[Optional[List[Tuple[int, int]]], int]:
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from: Dict[Tuple[int, int], Tuple[int, int]] = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    visited = set()
    explored_nodes = 0

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current), explored_nodes

        if current in visited:
            continue
        visited.add(current)
        explored_nodes += 1

        for neighbor in get_neighbors(current):
            if not grid.in_bounds(*neighbor) or grid.is_occupied(*neighbor):
                continue

            tentative_g = g_score[current] + 1  # constant cost

            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal)
                if neighbor not in visited:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None, explored_nodes  # No path found
