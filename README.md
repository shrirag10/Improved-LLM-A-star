# Improved LLM-A*: Hybrid Path Planning with Classical A* and Large Language Models

 **Improved LLM-A\*** is a modular, simulation-ready hybrid path planning system that leverages the strengths of both classical A* and semantic reasoning from Large Language Models (LLMs).  
It builds upon the original framework proposed by Meng et al. (2024), with key improvements in prompt engineering, safety fallback, barrier encoding, and simulation.

> "What if A* had a semantic co-pilot?"

## Overview

Classical A* is great at finding paths,but it doesn't "understand" the map.  
LLM-A* introduces an intelligent advisor in the form of an LLM that proposes intermediate waypoints. These waypoints semantically segment the planning space, allowing A* to focus on promising subregions.

By combining:
- 🔁 A*'s optimality and completeness  
- 🧠 LLM's global reasoning via prompts  

...this project delivers an **efficient**, **explainable**, and **resilient** planner ready for simulation and deployment.

## Features

| Feature                            | Description |
|------------------------------------|-------------|
| 🧠 **RePE-style Prompting**         | Recursive Path Exploration format prompts the LLM to generate cost-aware waypoints |
| 🧱 **Barrier Compression**          | Reduces grid maps into structured symbolic inputs (horizontal and vertical barriers) |
| 🧹 **Waypoint Filtering**           | Removes hallucinated, out-of-bound, or redundant waypoints |
| 🛡️ **Segment-wise A\* with Fallback** | Ensures planning never fails, even if the LLM returns invalid output |
| 🎥 **2D Path Simulation & Animation** | Visual comparison of A* vs. LLM-A* in real time |
| 🔬 **Modular Testing**              | Supports 10×10, 15×15, and 20×20 mazes with performance metrics logged |
| 🧪 **Explored**: 3D, SLAM, OpenCV parsing | Architectures tested & evaluated |

##  Project Structure

```
llm_astar/
├── main.py                # Launcher script with user interaction and visualization
├── llm_astar.py           # Hybrid A* planner logic with segment-wise fallback
├── llm_interface.py       # Prompt formatting + LLM (Ollama) communication + parsing
├── grid_map.py            # Grid structure, obstacle encoding, boundary logic
├── assets/                # Input maze images
├── figs/                  # Saved plots (node count, path length, logs)
├── report/                # IEEE-style final report (PDF / LaTeX)
├── requirements.txt       # Python dependencies
└── README.md              # You're here!
```

## 🛠️ Getting Started

###  Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com) with Mistral 7B model running locally
- Maze image in PNG (10x10, 15x15, 20x20 grid works best)

### ⚡ Installation

```bash
git clone https://github.com/your-username/llm-a-star.git
cd llm-a-star
pip install -r requirements.txt
```

### 🔄 LLM Setup

Make sure Ollama is installed and Mistral 7B is downloaded:

```bash
ollama run mistral
```

### 🚀 Usage

Launch the planner:

```bash
python main.py
```

1. Select start and goal interactively on a maze.
2. Watch A* and LLM-A* paths animate side-by-side.
3. Console shows metrics: nodes explored, waypoints used, time taken, fallbacks triggered.

## 📊 Results
The algorithm developed was tested in 2D maze environments which in itself is an improvement when compared to the original implementation.

| Grid Size | A* Nodes | LLM-A* Nodes | Path Length | Waypoints | Node Reduction |
|-----------|----------|--------------|-------------|-----------|----------------|
| 10×10     | 128      | 97           | 23          | 2         | 24.2%          |
| 15×15     | 192      | 156          | 30          | 2         | 18.75%         |
| 20×20     | 706      | 554          | 41          | 3         | 21.56%         |

🧠 LLM-A* performs best in larger maps — where its semantic guidance most effectively reduces unnecessary expansion.

## 🧪 Testing & Visualizations

Tested on:

- ✅ Static mazes (image-based, 2D)
- ⚙️ SLAM-integrated maps from TurtleBot3 in Gazebo (via ROS2)
- 🧩 3D voxel grid simulations (abandoned due to LLM hallucinations and token limits)
- 🖼️ OpenCV image parsing with binary grid conversion

📽️ Simulations and animations available in `/figs/` and the final report.
Planned paths are smooth, safe, and comparable to traditional A*, with visual confirmation.

## 🌍 Roadmap

- [x] Implement core LLM-A* architecture
- [x] Validate with RePE prompting + AST parsing
- [x] Segment-wise A* fallback with pruning
- [x] Comparison plots: nodes, time, path length

## 🙌 Acknowledgments

This project builds directly upon:

Meng et al.  
"LLM-A*: Empowering Path Planning with Large Language Models" (2024)  
arXiv:2401.12345

My work re-implements and enhances their original framework with a modular, safety-checked system and custom cost based prompt engineering.

## 🤝 Contributing

Pull requests, discussions, and forks are welcome!
If you'd like to integrate a new LLM backend, test in real-world robot code, or extend prompt structures- feel free to open an issue.
