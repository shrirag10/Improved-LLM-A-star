from typing import List, Tuple, Optional
from grid_map import GridMap
from a_star import a_star_search
from llm_interface import get_llm_waypoints

def manhattan(p1: Tuple[int, int], p2: Tuple[int, int]) -> int:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def filter_dense_waypoints(waypoints: List[Tuple[int, int]], min_dist: int = 3) -> List[Tuple[int, int]]:
    if not waypoints:
        return []

    filtered = [waypoints[0]]
    for wp in waypoints[1:]:
        if manhattan(filtered[-1], wp) >= min_dist:
            filtered.append(wp)

    return filtered

def prune_redundant_waypoints(grid: GridMap,
                               waypoints: List[Tuple[int, int]],
                               start: Tuple[int, int],
                               goal: Tuple[int, int]) -> List[Tuple[int, int]]:
    targets = [start] + waypoints + [goal]
    pruned = []
    i = 0

    while i < len(targets) - 2:
        if a_star_search(grid, targets[i], targets[i + 2])[0] is not None:
            i += 1  # Middle point is redundant
        else:
            pruned.append(targets[i + 1])
            i += 1

    if len(targets) >= 3 and targets[-2] not in pruned:
        pruned.append(targets[-2])

    return pruned

def llm_astar(grid: GridMap,
              start: Tuple[int, int],
              goal: Tuple[int, int],
              model: str = "mistral") -> Tuple[Optional[List[Tuple[int, int]]], List[Tuple[int, int]]]:
    """
    LLM-A* path planner with:
    - LLM-generated waypoints
    - Filtering and pruning
    - Segment-wise A* fallback
    """

    print("📤 Querying LLM for waypoints...")
    waypoints = get_llm_waypoints(
        start=start,
        goal=goal,
        horizontal_barriers=grid.horizontal_barriers,
        vertical_barriers=grid.vertical_barriers,
        grid=grid,
        model=model
    )

    print(f"📌 Raw LLM Waypoints: {waypoints}")

    if not waypoints:
        print("⚠️ No valid LLM waypoints — defaulting to baseline A*")
        fallback_path, _ = a_star_search(grid, start, goal)
        return fallback_path, []

    # Step 1: Filter waypoints inside walls / redundant
    waypoints = [wp for wp in waypoints if grid.in_bounds(*wp) and not grid.is_occupied(*wp)]
    waypoints = filter_dense_waypoints(waypoints, min_dist=3)
    waypoints = prune_redundant_waypoints(grid, waypoints, start, goal)

    print(f"✅ Filtered & Pruned Waypoints: {waypoints}")

    # Step 2: Segment-wise planning
    targets = [start] + waypoints + [goal]
    full_path = []
    total_nodes = 0

    for i in range(len(targets) - 1):
        s = targets[i]
        g = targets[i + 1]
        print(f"🔄 Planning from {s} → {g}...")

        path, explored = a_star_search(grid, s, g)

        if path is None:
            print(f"❌ Segment failed: {s} → {g}. Fallback to full A*.")
            fallback_path, _ = a_star_search(grid, start, goal)
            return fallback_path, []

        # Avoid duplicating nodes
        if i == 0:
            full_path.extend(path)
        else:
            full_path.extend(path[1:])

        total_nodes += explored

    print(f"✅ Final LLM-A* Path Length: {len(full_path)}")
    return full_path, waypoints
