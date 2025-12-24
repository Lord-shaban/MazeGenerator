<div align="center">

# 🍄 Super Maze Bros

### *A Mario-Themed Maze Generator & Algorithm Visualizer*

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

<img src="https://img.shields.io/badge/🎮_Super_Maze_Bros-Ready_to_Play!-red?style=for-the-badge" alt="Ready to Play">

</div>

---

## 🎯 Overview

**Super Maze Bros** is an interactive maze generator and pathfinding algorithm visualizer with a classic Nintendo Mario theme. Compare up to 4 different algorithms side-by-side and watch them race to find the solution!

<div align="center">

| 🔴 Player 1 | 🟢 Player 2 | 🔵 Player 3 | 🩷 Player 4 |
|:-----------:|:-----------:|:-----------:|:-----------:|
| MARIO | LUIGI | TOAD | PEACH |

</div>

---

## ✨ Features

### 🧩 Maze Generation
- **Recursive Backtracking** (DFS-based) algorithm
- Configurable maze sizes: `15×15`, `21×21`, `25×25`, `31×31`
- Instant generation with beautiful brick-style walls

### 🔍 Solving Algorithms
| Algorithm | Type | Optimal Path? | Description |
|-----------|------|:-------------:|-------------|
| **DFS** | Depth-First Search | ❌ | Explores as deep as possible first |
| **BFS** | Breadth-First Search | ✅ | Guarantees shortest path |
| **A*** | A-Star | ✅ | Heuristic-based optimal pathfinding |
| **Greedy** | Greedy Best-First | ❌ | Fast but not always optimal |

### 🎮 Interactive Features
- 📐 **Adjustable maze size**
- ⚡ **Animation speed control**
- 👥 **1-4 player comparison mode**
- 🏆 **Winner detection** based on path length
- 📊 **Real-time statistics** (path length, cells explored, time)

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/MazeGenerator.git
cd MazeGenerator

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
python main.py
```

---

## 🎨 Mario-Themed Design

| Element | Appearance | Description |
|---------|------------|-------------|
| 🧱 **Walls** | Red Bricks | Classic Mario brick pattern |
| 🟩 **Start** | Green Pipe | Mario's iconic warp pipe |
| ⭐ **Goal** | Golden Star | Collect the star to win! |
| 🌤️ **Path** | Sky Blue | Open path to explore |
| 🟡 **Solution** | Gold Coins | The winning path |

---

## 🕹️ How to Use

1. **Select Maze Size** - Choose from 15×15 to 31×31
2. **Adjust Speed** - Control animation speed with the slider
3. **Choose Players** - Select 1 to 4 algorithms to compare
4. **Pick Algorithms** - Assign an algorithm to each player
5. **Press START!** - Watch the algorithms race!

### Controls

| Button | Action |
|--------|--------|
| `? NEW WORLD` | Generate a new maze |
| `★ START!` | Begin solving animation |
| `✕ RESET` | Clear the solution |

---

## 📊 Algorithm Comparison

```
┌─────────────────────────────────────────────────────────┐
│  Algorithm  │  Speed   │  Optimal  │  Memory  │  Use    │
├─────────────┼──────────┼───────────┼──────────┼─────────┤
│  DFS        │  Fast    │    No     │   Low    │ Simple  │
│  BFS        │  Medium  │    Yes    │   High   │ Shortest│
│  A*         │  Fast    │    Yes    │   Med    │ Best    │
│  Greedy     │  V.Fast  │    No     │   Low    │ Quick   │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
MazeGenerator/
├── main.py          # Main application with GUI
├── requirements.txt # Python dependencies
└── README.md        # This file
```

---

## 🛠️ Technical Details

- **Language:** Python 3.8+
- **GUI Framework:** Tkinter
- **Architecture:** Object-Oriented with MVC pattern
- **Threading:** Background algorithm execution
- **Performance:** Incremental canvas updates for smooth animation

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### 🍄 Let's-a Go! 🍄

*Made with ❤️ and inspired by Super Mario Bros*

**[⬆ Back to Top](#-super-maze-bros)**

</div>
