# MazeGenerator

A Python library for generating and solving mazes using various algorithms.

## Features

- **Maze Generation Algorithms:**
  - Depth-First Search (Recursive Backtracker)
  - Prim's Algorithm

- **Maze Solving Algorithms:**
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)

- **Visualization:** ASCII art display of mazes with optional solution path

## Installation

```bash
git clone https://github.com/YOUR_USERNAME/MazeGenerator.git
cd MazeGenerator
pip install -r requirements.txt
```

## Usage

```python
from main import Maze

# Create a maze
maze = Maze(21, 21)

# Generate using DFS algorithm
maze.generate("dfs")

# Display the maze
print(maze.display())

# Solve using BFS
path = maze.solve("bfs")

# Display with solution
print(maze.display(path))
```

## Running the Demo

```bash
python main.py
```

## Example Output

```
██████████████████████
██S     ██      ██  ██
████  ████  ██  ██  ██
██      ██  ██      ██
██  ██████  ██████  ██
██          ██      ██
██████████  ██  ██████
██      ██      ██  ██
██  ██  ████████    ██
██  ██          ██  ██
██  ██████████  ██  ██
██              ██  ██
██████████████████  ██
██                  ██
██  ████████████████E██
██████████████████████
```

## License

MIT License
