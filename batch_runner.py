import csv
import time
from grid_map import GridMap
from a_star import a_star_search
from llm_astar import llm_astar

def make_test_maps():
    """Define a few test maps with different barrier setups."""
    maps = []

    # Map 1: Classic L-shaped barrier
    def setup1():
        gmap = GridMap((0, 50), (0, 30))
        gmap.add_horizontal_barrier(10, 0, 25)
        gmap.add_vertical_barrier(25, 10, 22)
        return gmap, (5, 5), (20, 20)

    # Map 2: Diagonal vertical zigzag
    def setup2():
        gmap = GridMap((0, 40), (0, 30))
        for i in range(5, 30, 5):
            gmap.add_vertical_barrier(i, i, i + 5)
        return gmap, (2, 2), (35, 25)

    # Map 3: Narrow corridor
    def setup3():
        gmap = GridMap((0, 50), (0, 20))
        gmap.add_horizontal_barrier(9, 5, 45)
        gmap.add_horizontal_barrier(11, 5, 45)
        return gmap, (2, 10), (48, 10)

    maps.append(setup1)
    maps.append(setup2)
    maps.append(setup3)
    return maps

def run_batch_tests():
    test_maps = make_test_maps()

    with open("results.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "MapID", "Planner", "PathLength", "NodesExplored", "TimeTakenSec", "LLMWaypoints"
        ])

        for i, setup in enumerate(test_maps, 1):
            grid, start, goal = setup()
            print(f"\n=== 🗺️ Map {i}: Start {start}, Goal {goal} ===")

            # --- Run baseline A* ---
            t0 = time.time()
            path, nodes = a_star_search(grid, start, goal)
            t1 = time.time()
            writer.writerow([i, "A*", len(path) if path else 0, nodes, round(t1 - t0, 3), 0])

            # --- Run LLM-A* ---
            t2 = time.time()
            path_llm, waypoints = llm_astar(grid, start, goal, model="mistral")
            t3 = time.time()
            writer.writerow([i, "LLM-A*", len(path_llm) if path_llm else 0, "?", round(t3 - t2, 3), len(waypoints)])

    print("\n✅ Results written to results.csv")
