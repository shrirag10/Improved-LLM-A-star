# 🤖 Improved LLM-A*: Hybrid Path Planning with Classical A* and Large Language Models

**LLM-A\*** is a modular, simulation-ready hybrid path planning system that leverages the strengths of both classical A* and semantic reasoning from Large Language Models (LLMs).  
It builds upon the original framework proposed by Meng et al. (2024), with key improvements in prompt engineering, safety fallback, barrier encoding, and simulation.

> "What if A* had a semantic co-pilot?"

---

## 👀 Overview

Classical A* is great at finding paths, but it doesn't "understand" the map.  
LLM-A* introduces an intelligent advisor in the form of an LLM that proposes intermediate waypoints. These waypoints semantically segment the planning space, allowing A* to focus on promising subregions.

By combining:
- 🔁 A*'s optimality and completeness  
- 🧠 LLM's global reasoning via prompts  

This project delivers an **efficient**, **explainable**, and **resilient** planner ready for simulation and deployment.

---

## Simulation

| Grid Size | Simulation |
|-----------|------------|
| 15×15     | ▶️ [Watch on YouTube](https://youtu.be/yj0_0vLn0eA) |
| 20×20     | ▶️ [Watch on YouTube](https://youtu.be/_1uj5l019Uo) |
--

## 🔥 Features

| Feature | Description |
|--------|-------------|
| 🧠 RePE-style Prompting | Structured prompt design that simulates recursive planning |
| 🧱 Barrier Compression | Encodes walls as horizontal/vertical spans for token-efficient prompting |
| 🧹 Waypoint Filtering | Removes hallucinated or invalid points |
| 🛡️ Segment-wise A* | Fallback-safe planning ensures path completion |
| 🎥 2D Simulation | A* and LLM-A* side-by-side animations |
| 🔬 Tested Extensions | ROS2 SLAM, 3D grids, OpenCV map parsing |

---

## 📁 Project Snapshot

<p align="center">
  <img src="https://github.com/shrirag10/Improved-LLM-A-star/blob/main/figs/20x20.png" width="700" alt="A* vs LLM-A* comparison in 20x20 maze">
</p>

---

## 🏗️ Project Structure

llm_astar/
├── main.py # Launcher script with user interaction and visualization
├── llm_astar.py # Hybrid A* planner logic with segment-wise fallback
├── llm_interface.py # Prompt formatting + LLM (Ollama) communication + parsing
├── grid_map.py # Grid structure, obstacle encoding, boundary logic
├── assets/ # Input maze images
├── figs/ # Saved plots (node count, path length, logs)
├── report/ # IEEE-style final report (PDF / LaTeX)
├── requirements.txt # Python dependencies
└── README.md # You're here!


## 🛠️ Getting Started

### Prerequisites

- Python 3.8+
- [Ollama](https://ollama.com) with Mistral 7B model running locally
- Maze image in PNG (10×10, 15×15, 20×20 grid works best)

### ⚡ Installation

```bash
git clone https://github.com/shrirag10/Improved-LLM-A-star.git
cd Improved-LLM-A-star
pip install -r requirements.txt
🔄 LLM Setup
Make sure Ollama is installed and Mistral 7B is downloaded:

bash
Copy
Edit
ollama run mistral
🚀 Usage
Launch the planner:

bash
Copy
Edit
python main.py
Select start and goal interactively on a maze.

Watch A* and LLM-A* paths animate side-by-side.

Console shows metrics: nodes explored, waypoints used, time taken, fallbacks triggered.

📊 Results
The algorithm was tested in 2D maze environments — an advancement over the original static implementation.

Grid Size	A* Nodes	LLM-A* Nodes	Path Length	Waypoints	Node Reduction
10×10	128	97	41	2	24.2%
15×15	192	156	159	2	18.75%
20×20	706	554	234	3	21.56%

🧠 LLM-A* performs best in larger maps — where semantic guidance most effectively reduces unnecessary expansion.

🧪 Testing & Visualizations
Tested on:

✅ Static mazes (image-based, 2D)

⚙️ SLAM-integrated maps from TurtleBot3 in Gazebo (via ROS2)

🧩 3D voxel grid simulations (abandoned due to LLM hallucinations and token limits)

🖼️ OpenCV image parsing with binary grid conversion

📽️ Simulations and animations are in /figs/ and the final report is avaulable in /report/.

🛑 Fallback Demonstration
<p align="center"> <img src="https://github.com/shrirag10/Improved-LLM-A-star/blob/main/figs/Fallback.png" width="500" alt="LLM fallback to A* on failure"> </p>
🌍 Roadmap
 Implement core LLM-A* architecture

 Validate with RePE prompting + AST parsing

 Segment-wise A* fallback with pruning

 Comparison plots: nodes, time, path length

🙌 Acknowledgments
This project builds directly upon:

Meng et al.
"LLM-A*: Empowering Path Planning with Large Language Models" (2024)
arXiv:2401.12345

My work re-implements and enhances their framework with a modular, simulation-ready architecture and cost-aware prompt logic.

🤝 Contributing
Pull requests, forks, and discussions are welcome!
Want to extend prompt structures or try a different LLM backend? Open an issue or fork away!
