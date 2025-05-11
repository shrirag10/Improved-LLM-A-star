import requests
import json
import ast
import re
from typing import Tuple, List
from grid_map import GridMap

COST_RULES = """
Map Cost Rules:
- Open grid cell: cost = 1.0
- Diagonal movement: cost = 1.4
- Barriers/obstacles: impassable
- The goal is to minimize total cost, not just number of steps.
- Prefer straight, low-cost paths that avoid unnecessary turns.
"""

def format_repe_prompt(start: Tuple[int, int], goal: Tuple[int, int],
                       horizontal_barriers: List[List[int]],
                       vertical_barriers: List[List[int]]) -> str:
    return f"""
{COST_RULES}

You are an expert path planner. Identify a cost-minimizing path from START to GOAL while avoiding obstacles.
Your output must follow one of these two formats:

Format A (JSON-style):
Generated Path: [[x1, y1], [x2, y2], ..., [xn, yn]]

Format B (Bullet-style):
Generated Path:
- [x1, y1]
- [x2, y2]
...
- [xn, yn]

Start Point: {list(start)}
Goal Point: {list(goal)}
Horizontal Barriers: {horizontal_barriers}
Vertical Barriers: {vertical_barriers}

Remember:
- Max 10 waypoints.
- Do not include the start or goal points.
- Avoid collisions.
"""

def ask_ollama(prompt: str, model: str = "mistral", timeout: int = 30) -> str:
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(url, json=payload, timeout=timeout)
        lines = response.text.strip().split("\n")
        full_response = ""
        for line in lines:
            data = json.loads(line)
            full_response += data.get("response", "")
        return full_response
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return ""

def extract_waypoints_from_response(response: str) -> List[Tuple[int, int]]:
    """
    Try to extract a path using multiple strategies:
    1. JSON-style list [[x, y], ...]
    2. Bulleted list: - [x, y]
    """
    # Primary: JSON-style list extraction
    match = re.search(r"Generated Path[:：]?\s*(\[\[.*?\]\])", response, re.DOTALL)
    if match:
        try:
            path_str = match.group(1).strip()
            path = ast.literal_eval(path_str)
            result = []
            for p in path:
                if isinstance(p, list) and len(p) == 2:
                    try:
                        x = int(p[0])
                        y = int(p[1])
                        result.append((x, y))
                    except Exception as e:
                        print(f"❌ Conversion error: {e} for {p}")
            if result:
                return result
        except Exception as e:
            print(f"❌ Error parsing structured list: {e}")

    # Fallback: Bulleted format extraction
    bullets = re.findall(r"-\s*\[?(\d+),\s*(\d+)\]?", response)
    if bullets:
        return [(int(x), int(y)) for x, y in bullets]

    # Final fallback: Loose extraction of all pairs
    loose = re.findall(r"\[(\d+),\s*(\d+)\]", response)
    if loose:
        return [(int(x), int(y)) for x, y in loose]

    print("❌ No valid waypoints extracted.")
    return []

def filter_waypoints(waypoints: List[Tuple[int, int]],
                     start: Tuple[int, int],
                     goal: Tuple[int, int],
                     grid: GridMap) -> List[Tuple[int, int]]:
    seen = set()
    valid = []
    for wp in waypoints:
        if wp in (start, goal) or wp in seen:
            continue
        x, y = wp
        if not grid.in_bounds(x, y):
            continue
        if grid.is_occupied(x, y):
            continue
        seen.add(wp)
        valid.append(wp)
    return valid

def get_llm_waypoints(start: Tuple[int, int], goal: Tuple[int, int],
                      horizontal_barriers: List[List[int]],
                      vertical_barriers: List[List[int]],
                      grid: GridMap,
                      model: str = "mistral") -> List[Tuple[int, int]]:
    prompt = format_repe_prompt(start, goal, horizontal_barriers, vertical_barriers)
    print("📤 Sending prompt to LLM...")
    response = ask_ollama(prompt, model=model)
    print("🧠 Mistral Response:\n", response)
    raw_waypoints = extract_waypoints_from_response(response)
    valid_waypoints = filter_waypoints(raw_waypoints, start, goal, grid)
    if not valid_waypoints:
        print("⚠️ No usable waypoints — defaulting to A*")
    else:
        print(f"✅ Parsed {len(valid_waypoints)} LLM waypoints")
    return valid_waypoints

# Optional test stub
if __name__ == "__main__":
    from grid_map import GridMap
    start = (5, 5)
    goal = (20, 20)
    hbar = [[10, 0, 25], [15, 30, 50]]
    vbar = [[25, 10, 22]]
    grid = GridMap((0, 60), (0, 60))
    # Set barriers on the grid for testing purposes
    for y, x0, x1 in hbar:
        for x in range(x0, x1 + 1):
            grid.set_occupied(x, y)
    for x, y0, y1 in vbar:
        for y in range(y0, y1 + 1):
            grid.set_occupied(x, y)
    waypoints = get_llm_waypoints(start, goal, hbar, vbar, grid)
    print("🧭 Final waypoints:", waypoints)
