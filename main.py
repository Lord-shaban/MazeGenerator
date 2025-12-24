"""
🍄 SUPER MAZE BROS 🍄
Classic Mario-Style Maze Generator & Solver
"""

import tkinter as tk
from tkinter import ttk
import random
from collections import deque
import heapq
import time
import threading


# ══════════════════════════════════════════════════════════════════════════════
# MAZE ALGORITHMS
# ══════════════════════════════════════════════════════════════════════════════

class MazeGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def generate(self):
        maze = [[1] * self.width for _ in range(self.height)]
        stack = [(1, 1)]
        maze[1][1] = 0
        
        while stack:
            x, y = stack[-1]
            neighbors = []
            for dx, dy in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
                nx, ny = x + dx, y + dy
                if 0 < nx < self.width - 1 and 0 < ny < self.height - 1 and maze[ny][nx] == 1:
                    neighbors.append((nx, ny, dx // 2, dy // 2))
            if neighbors:
                nx, ny, wx, wy = random.choice(neighbors)
                maze[y + wy][x + wx] = 0
                maze[ny][nx] = 0
                stack.append((nx, ny))
            else:
                stack.pop()
        
        maze[1][1] = 0
        maze[self.height - 2][self.width - 2] = 0
        return maze


class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.height = len(maze)
        self.width = len(maze[0])
        self.start = (1, 1)
        self.end = (self.width - 2, self.height - 2)
    
    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height and self.maze[ny][nx] == 0:
                neighbors.append((nx, ny))
        return neighbors
    
    def solve_dfs(self):
        stack = [(self.start, [self.start])]
        visited = {self.start}
        explored = []
        while stack:
            (x, y), path = stack.pop()
            explored.append((x, y))
            if (x, y) == self.end:
                return path, explored
            for n in self.get_neighbors(x, y):
                if n not in visited:
                    visited.add(n)
                    stack.append((n, path + [n]))
        return None, explored
    
    def solve_bfs(self):
        queue = deque([(self.start, [self.start])])
        visited = {self.start}
        explored = []
        while queue:
            (x, y), path = queue.popleft()
            explored.append((x, y))
            if (x, y) == self.end:
                return path, explored
            for n in self.get_neighbors(x, y):
                if n not in visited:
                    visited.add(n)
                    queue.append((n, path + [n]))
        return None, explored
    
    def solve_astar(self):
        def h(a): return abs(a[0] - self.end[0]) + abs(a[1] - self.end[1])
        open_set = [(h(self.start), 0, self.start)]
        came_from = {}
        g = {self.start: 0}
        visited = set()
        explored = []
        while open_set:
            _, _, current = heapq.heappop(open_set)
            if current in visited:
                continue
            visited.add(current)
            explored.append(current)
            if current == self.end:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1], explored
            for n in self.get_neighbors(current[0], current[1]):
                ng = g[current] + 1
                if n not in g or ng < g[n]:
                    came_from[n] = current
                    g[n] = ng
                    heapq.heappush(open_set, (ng + h(n), ng, n))
        return None, explored
    
    def solve_greedy(self):
        def h(a): return abs(a[0] - self.end[0]) + abs(a[1] - self.end[1])
        open_set = [(h(self.start), self.start)]
        came_from = {}
        visited = set()
        explored = []
        while open_set:
            _, current = heapq.heappop(open_set)
            if current in visited:
                continue
            visited.add(current)
            explored.append(current)
            if current == self.end:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return path[::-1], explored
            for n in self.get_neighbors(current[0], current[1]):
                if n not in visited:
                    came_from[n] = current
                    heapq.heappush(open_set, (h(n), n))
        return None, explored


# ══════════════════════════════════════════════════════════════════════════════
# SUPER MARIO THEME GUI
# ══════════════════════════════════════════════════════════════════════════════

class SuperMazeBros:
    # Authentic NES Mario Colors - Comfortable for eyes
    C = {
        'sky': '#5c94fc',
        'sky_light': '#88b4fc',
        'brick': '#c84c0c',
        'brick_dark': '#a43000',
        'block': '#e4a048',
        'block_dark': '#c88420',
        'ground': '#e09050',
        'ground_dark': '#a06030',
        'pipe': '#38b838',
        'pipe_dark': '#207820',
        'coin': '#f8d830',
        'coin_dark': '#c8a800',
        'white': '#fcfcfc',
        'black': '#000000',
        'mario_red': '#d82800',
        'luigi_green': '#00a800',
        'toad_blue': '#0058f8',
        'peach_pink': '#f8a0c0',
    }
    
    # Player themes
    PLAYERS = [
        {'name': 'MARIO', 'icon': '🔴', 'explored': '#ff6060', 'solution': '#f8d830', 'border': '#d82800'},
        {'name': 'LUIGI', 'icon': '🟢', 'explored': '#60d060', 'solution': '#f8d830', 'border': '#00a800'},
        {'name': 'TOAD',  'icon': '🔵', 'explored': '#60a0ff', 'solution': '#f8b800', 'border': '#0058f8'},
        {'name': 'PEACH', 'icon': '🩷', 'explored': '#ffa0c0', 'solution': '#f8b800', 'border': '#f878a8'},
    ]
    
    ALGORITHMS = {'DFS': 'solve_dfs', 'BFS': 'solve_bfs', 'A*': 'solve_astar', 'Greedy': 'solve_greedy'}
    
    def __init__(self, root):
        self.root = root
        self.root.title("🍄 Super Maze Bros")
        self.root.configure(bg=self.C['sky'])
        
        self.maze_size = 21
        self.cell_size = 14
        self.maze = None
        self.solving = False
        self.speed = 8
        self.num_players = 4
        
        self.canvases = []
        self.stats = []
        self.algo_vars = []
        self.player_frames = []
        self.cell_ids = []  # Cache for cell canvas IDs
        self.drawn_states = []  # Track drawn state per canvas
        
        self._build_ui()
        self._generate()
    
    def _build_ui(self):
        # Main container with sky gradient effect
        self.main = tk.Frame(self.root, bg=self.C['sky'])
        self.main.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # ═══ TOP SECTION: Title & Clouds ═══
        self._build_header()
        
        # ═══ CONTROL PANEL: Question Block Style ═══
        self._build_controls()
        
        # ═══ GAME AREA: Mazes ═══
        self._build_game_area()
        
        # ═══ BOTTOM: Ground & Status ═══
        self._build_footer()
    
    def _build_header(self):
        header = tk.Frame(self.main, bg=self.C['sky'], height=70)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Top row with SIZE - TITLE - PLAYERS
        top_row = tk.Frame(header, bg=self.C['sky'])
        top_row.pack(fill=tk.X, pady=10)
        
        # LEFT: Size control
        left_frame = tk.Frame(top_row, bg=self.C['sky'])
        left_frame.pack(side=tk.LEFT, padx=20)
        
        size_outer = tk.Frame(left_frame, bg=self.C['black'], padx=2, pady=2)
        size_outer.pack(side=tk.LEFT, padx=(0, 10))
        size_inner = tk.Frame(size_outer, bg=self.C['block'], padx=8, pady=4)
        size_inner.pack()
        tk.Label(size_inner, text="📐 SIZE", font=('Consolas', 9, 'bold'),
                fg=self.C['brick_dark'], bg=self.C['block']).pack(side=tk.LEFT, padx=(0, 5))
        self.size_var = tk.StringVar(value="21×21")
        size_cb = ttk.Combobox(size_inner, textvariable=self.size_var,
                              values=["15×15", "21×21", "25×25", "31×31"], width=6, state='readonly')
        size_cb.pack(side=tk.LEFT)
        size_cb.bind('<<ComboboxSelected>>', self._on_size_change)
        
        # Speed control next to size
        speed_outer = tk.Frame(left_frame, bg=self.C['black'], padx=2, pady=2)
        speed_outer.pack(side=tk.LEFT)
        speed_inner = tk.Frame(speed_outer, bg=self.C['block'], padx=8, pady=4)
        speed_inner.pack()
        tk.Label(speed_inner, text="⚡ SPEED", font=('Consolas', 9, 'bold'),
                fg=self.C['brick_dark'], bg=self.C['block']).pack(side=tk.LEFT, padx=(0, 5))
        self.speed_var = tk.IntVar(value=75)
        speed_scale = tk.Scale(speed_inner, from_=1, to=100, orient=tk.HORIZONTAL,
                              variable=self.speed_var, length=60, showvalue=False,
                              bg=self.C['block'], highlightthickness=0, troughcolor=self.C['block_dark'],
                              activebackground=self.C['coin'],
                              command=lambda v: setattr(self, 'speed', max(1, 101 - int(v))))
        speed_scale.pack(side=tk.LEFT)
        
        # CENTER: Title
        title_container = tk.Frame(top_row, bg=self.C['sky'])
        title_container.pack(side=tk.LEFT, expand=True)
        
        # Shadow
        shadow = tk.Label(title_container, text="🍄 SUPER MAZE BROS 🍄",
                font=('Consolas', 20, 'bold'), fg=self.C['black'],
                bg=self.C['sky'])
        shadow.place(x=2, y=2)
        
        # Main title
        tk.Label(title_container, text="🍄 SUPER MAZE BROS 🍄",
                font=('Consolas', 20, 'bold'), fg=self.C['coin'],
                bg=self.C['sky']).pack()
        
        # RIGHT: Players control
        right_frame = tk.Frame(top_row, bg=self.C['sky'])
        right_frame.pack(side=tk.RIGHT, padx=20)
        
        players_outer = tk.Frame(right_frame, bg=self.C['black'], padx=2, pady=2)
        players_outer.pack()
        players_inner = tk.Frame(players_outer, bg=self.C['block'], padx=8, pady=4)
        players_inner.pack()
        tk.Label(players_inner, text="👥 PLAYERS", font=('Consolas', 9, 'bold'),
                fg=self.C['brick_dark'], bg=self.C['block']).pack(side=tk.LEFT, padx=(0, 5))
        self.num_var = tk.StringVar(value="4")
        players_cb = ttk.Combobox(players_inner, textvariable=self.num_var,
                                  values=["1", "2", "3", "4"], width=3, state='readonly')
        players_cb.pack(side=tk.LEFT)
        players_cb.bind('<<ComboboxSelected>>', self._on_players_change)
    
    def _build_controls(self):
        # Question block outer frame
        ctrl_outer = tk.Frame(self.main, bg=self.C['black'], padx=3, pady=3)
        ctrl_outer.pack(fill=tk.X, padx=20, pady=(5, 10))
        
        # Question block inner
        ctrl_block = tk.Frame(ctrl_outer, bg=self.C['block'], padx=15, pady=10)
        ctrl_block.pack(fill=tk.X)
        
        # Add rivet/corner decorations
        for corner in [(0, 0), (1, 0), (0, 1), (1, 1)]:
            dot = tk.Frame(ctrl_block, bg=self.C['block_dark'], width=6, height=6)
            dot.place(relx=corner[0], rely=corner[1], anchor='center' if corner == (0.5, 0.5) else 
                     ('nw' if corner == (0,0) else 'ne' if corner == (1,0) else 'sw' if corner == (0,1) else 'se'),
                     x=8 if corner[0]==0 else -8, y=8 if corner[1]==0 else -8)
        
        # Controls row
        row = tk.Frame(ctrl_block, bg=self.C['block'])
        row.pack()
        
        # Algorithm selectors
        defaults = ['DFS', 'BFS', 'A*', 'Greedy']
        for i in range(4):
            p = self.PLAYERS[i]
            var = tk.StringVar(value=defaults[i])
            self.algo_vars.append(var)
            
            frame = tk.Frame(row, bg=self.C['block'])
            frame.pack(side=tk.LEFT, padx=6)
            
            # Player label with color
            lbl = tk.Label(frame, text=f"{p['icon']}P{i+1}", font=('Consolas', 9, 'bold'),
                          fg=p['border'], bg=self.C['block'])
            lbl.pack(side=tk.LEFT, padx=(0, 4))
            
            cb = ttk.Combobox(frame, textvariable=var, values=list(self.ALGORITHMS.keys()),
                             width=6, state='readonly')
            cb.pack(side=tk.LEFT)
    
    def _ctrl_group(self, parent, label, widget):
        frame = tk.Frame(parent, bg=self.C['block'])
        frame.pack(side=tk.LEFT, padx=8)
        
        tk.Label(frame, text=label, font=('Consolas', 9, 'bold'),
                fg=self.C['brick_dark'], bg=self.C['block']).pack(side=tk.LEFT, padx=(0, 5))
        widget.pack(side=tk.LEFT)
    
    def _separator(self, parent):
        tk.Label(parent, text="┃", font=('Consolas', 12),
                fg=self.C['block_dark'], bg=self.C['block']).pack(side=tk.LEFT, padx=8)
    
    def _build_game_area(self):
        # Buttons row - Pipe style
        btn_frame = tk.Frame(self.main, bg=self.C['sky'])
        btn_frame.pack(pady=8)
        
        self.btn_gen = self._pipe_button(btn_frame, "? NEW WORLD", self._generate, self.C['block'], self.C['block_dark'])
        self.btn_solve = self._pipe_button(btn_frame, "★ START!", self._start_solve, self.C['pipe'], self.C['pipe_dark'])
        self.btn_clear = self._pipe_button(btn_frame, "✕ RESET", self._clear, self.C['mario_red'], self.C['brick_dark'])
        
        # Mazes container
        self.game_frame = tk.Frame(self.main, bg=self.C['sky'])
        self.game_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self._create_player_panels()
    
    def _pipe_button(self, parent, text, command, color, dark):
        outer = tk.Frame(parent, bg=self.C['black'], padx=2, pady=2)
        outer.pack(side=tk.LEFT, padx=6)
        
        inner = tk.Frame(outer, bg=dark, padx=2, pady=2)
        inner.pack()
        
        btn = tk.Button(inner, text=text, font=('Consolas', 10, 'bold'),
                       bg=color, fg=self.C['white'], activebackground=color,
                       width=12, relief=tk.FLAT, cursor='hand2', command=command)
        btn.pack()
        return btn
    
    def _create_player_panels(self):
        # Clear existing
        for w in self.game_frame.winfo_children():
            w.destroy()
        
        self.canvases = []
        self.stats = []
        self.player_frames = []
        self.cell_ids = []
        self.drawn_states = []
        
        n = self.num_players
        
        # Adjust cell size based on number of players
        if n == 1:
            self.cell_size = 16
        elif n == 2:
            self.cell_size = 14
        elif n == 3:
            self.cell_size = 11
        else:
            self.cell_size = 9
        
        # Container for all player panels
        container = tk.Frame(self.game_frame, bg=self.C['sky'])
        container.pack()
        
        for i in range(n):
            panel = self._create_single_panel(container, i)
            panel.pack(side=tk.LEFT, padx=8, pady=5)
            self.player_frames.append(panel)
    
    def _create_single_panel(self, parent, idx):
        p = self.PLAYERS[idx]
        
        frame = tk.Frame(parent, bg=self.C['sky'])
        
        # ─── Header: Player name ───
        header = tk.Frame(frame, bg=self.C['sky'])
        header.pack(fill=tk.X, pady=(0, 4))
        
        tk.Label(header, text=p['icon'], font=('Segoe UI', 14),
                bg=self.C['sky']).pack(side=tk.LEFT)
        
        name_lbl = tk.Label(header, text=f"P{idx+1} - {self.algo_vars[idx].get()}",
                           font=('Consolas', 11, 'bold'), fg=p['border'], bg=self.C['sky'])
        name_lbl.pack(side=tk.LEFT, padx=5)
        
        # ─── Maze Canvas: Pipe-style border ───
        # Outer black border
        outer = tk.Frame(frame, bg=self.C['black'], padx=3, pady=3)
        outer.pack()
        
        # Colored border
        border = tk.Frame(outer, bg=p['border'], padx=2, pady=2)
        border.pack()
        
        # Dark inner
        inner = tk.Frame(border, bg=self.C['pipe_dark'], padx=2, pady=2)
        inner.pack()
        
        canvas = tk.Canvas(inner, width=self.maze_size * self.cell_size,
                          height=self.maze_size * self.cell_size,
                          bg=self.C['sky_light'], highlightthickness=0)
        canvas.pack()
        self.canvases.append(canvas)
        
        # ─── Stats: Coin block style ───
        stats_outer = tk.Frame(frame, bg=self.C['black'], padx=2, pady=2)
        stats_outer.pack(fill=tk.X, pady=(6, 0))
        
        stats_block = tk.Frame(stats_outer, bg=self.C['coin'], padx=8, pady=5)
        stats_block.pack(fill=tk.X)
        
        stats = {}
        
        # Path (with star icon)
        path_frame = tk.Frame(stats_block, bg=self.C['coin'])
        path_frame.pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(path_frame, text="★", font=('Segoe UI', 10), fg=self.C['mario_red'], 
                bg=self.C['coin']).pack(side=tk.LEFT)
        stats['path'] = tk.Label(path_frame, text="-", font=('Consolas', 9, 'bold'),
                                fg=self.C['black'], bg=self.C['coin'])
        stats['path'].pack(side=tk.LEFT, padx=2)
        
        # Explored (with coin icon)
        exp_frame = tk.Frame(stats_block, bg=self.C['coin'])
        exp_frame.pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(exp_frame, text="🪙", font=('Segoe UI', 9), bg=self.C['coin']).pack(side=tk.LEFT)
        stats['explored'] = tk.Label(exp_frame, text="-", font=('Consolas', 9, 'bold'),
                                    fg=self.C['black'], bg=self.C['coin'])
        stats['explored'].pack(side=tk.LEFT, padx=2)
        
        # Time
        time_frame = tk.Frame(stats_block, bg=self.C['coin'])
        time_frame.pack(side=tk.LEFT)
        tk.Label(time_frame, text="⏱", font=('Segoe UI', 9), bg=self.C['coin']).pack(side=tk.LEFT)
        stats['time'] = tk.Label(time_frame, text="-", font=('Consolas', 9, 'bold'),
                                fg=self.C['black'], bg=self.C['coin'])
        stats['time'].pack(side=tk.LEFT, padx=2)
        
        self.stats.append(stats)
        
        return frame
    
    def _build_footer(self):
        # Ground section
        ground_frame = tk.Frame(self.main, bg=self.C['ground'], height=50)
        ground_frame.pack(fill=tk.X, side=tk.BOTTOM)
        ground_frame.pack_propagate(False)
        
        # Ground pattern (brick-like)
        ground_inner = tk.Frame(ground_frame, bg=self.C['ground'])
        ground_inner.pack(fill=tk.BOTH, expand=True)
        
        # Top border line
        tk.Frame(ground_inner, bg=self.C['ground_dark'], height=3).pack(fill=tk.X)
        
        # Status label
        status_container = tk.Frame(ground_inner, bg=self.C['ground'])
        status_container.pack(fill=tk.BOTH, expand=True)
        
        self.status_lbl = tk.Label(status_container, 
                                   text="🎮 PRESS START TO PLAY!",
                                   font=('Consolas', 12, 'bold'),
                                   fg=self.C['white'], bg=self.C['ground'])
        self.status_lbl.place(relx=0.5, rely=0.5, anchor='center')
    
    def _on_size_change(self, e=None):
        size = int(self.size_var.get().split('×')[0])
        self.maze_size = size
        self._create_player_panels()
        self._generate()
    
    def _on_players_change(self, e=None):
        self.num_players = int(self.num_var.get())
        self._create_player_panels()
        if self.maze:
            for i in range(self.num_players):
                self._draw_maze(i)
    
    def _generate(self):
        if self.solving:
            return
        
        self.status_lbl.config(text="🔨 BUILDING WORLD...")
        self.root.update()
        
        gen = MazeGenerator(self.maze_size, self.maze_size)
        self.maze = gen.generate()
        
        # Clear cache for redraw
        self.cell_ids = []
        self.drawn_states = []
        
        for i in range(self.num_players):
            self._draw_maze(i)
            self.stats[i]['path'].config(text="-")
            self.stats[i]['explored'].config(text="-")
            self.stats[i]['time'].config(text="-")
        
        self.status_lbl.config(text="🎮 PRESS START TO PLAY!")
    
    def _draw_maze(self, idx, explored=None, solution=None):
        if idx >= len(self.canvases):
            return
        
        canvas = self.canvases[idx]
        canvas.delete('all')
        
        p = self.PLAYERS[idx]
        explored_set = set(explored) if explored else set()
        solution_set = set(solution) if solution else set()
        
        start = (1, 1)
        end = (self.maze_size - 2, self.maze_size - 2)
        
        cs = self.cell_size
        
        for y in range(self.maze_size):
            for x in range(self.maze_size):
                x1, y1 = x * cs, y * cs
                x2, y2 = x1 + cs, y1 + cs
                pos = (x, y)
                
                if self.maze[y][x] == 1:
                    # BRICK
                    canvas.create_rectangle(x1, y1, x2, y2, fill=self.C['brick'], outline=self.C['brick_dark'], width=1)
                    # Brick pattern
                    if cs >= 10:
                        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                        canvas.create_line(x1, mid_y, x2, mid_y, fill=self.C['brick_dark'])
                        if y % 2 == 0:
                            canvas.create_line(mid_x, y1, mid_x, mid_y, fill=self.C['brick_dark'])
                        else:
                            canvas.create_line(mid_x, mid_y, mid_x, y2, fill=self.C['brick_dark'])
                
                elif pos == start:
                    # PIPE (Start)
                    canvas.create_rectangle(x1, y1, x2, y2, fill=self.C['pipe'], outline=self.C['pipe_dark'], width=2)
                    if cs >= 12:
                        canvas.create_text((x1+x2)//2, (y1+y2)//2, text="▶",
                                          font=('Consolas', max(8, cs-5), 'bold'), fill=self.C['white'])
                
                elif pos == end:
                    # FLAG/STAR (End)
                    canvas.create_rectangle(x1, y1, x2, y2, fill=self.C['coin'], outline=self.C['coin_dark'], width=2)
                    if cs >= 12:
                        canvas.create_text((x1+x2)//2, (y1+y2)//2, text="★",
                                          font=('Consolas', max(8, cs-4), 'bold'), fill=self.C['mario_red'])
                
                elif pos in solution_set:
                    # SOLUTION PATH (Coins)
                    canvas.create_rectangle(x1, y1, x2, y2, fill=p['solution'], outline=self.C['coin_dark'], width=1)
                
                elif pos in explored_set:
                    # EXPLORED
                    canvas.create_rectangle(x1, y1, x2, y2, fill=p['explored'], outline='', width=0)
                
                else:
                    # SKY/PATH
                    canvas.create_rectangle(x1, y1, x2, y2, fill=self.C['sky_light'], outline='', width=0)
    
    def _start_solve(self):
        if self.solving or not self.maze:
            return
        
        self.solving = True
        self.btn_solve.config(state=tk.DISABLED)
        self.btn_gen.config(state=tk.DISABLED)
        
        threading.Thread(target=self._solve, daemon=True).start()
    
    def _solve(self):
        solver = MazeSolver(self.maze)
        
        results = []
        for i in range(self.num_players):
            algo = self.algo_vars[i].get()
            t0 = time.time()
            method = getattr(solver, self.ALGORITHMS[algo])
            sol, exp = method()
            t = (time.time() - t0) * 1000
            results.append({'idx': i, 'algo': algo, 'solution': sol, 'explored': exp, 'time': t})
        
        self.root.after(0, lambda: self.status_lbl.config(text="🏃 GO GO GO!"))
        
        # Animate exploration - batch updates
        max_exp = max(len(r['explored']) for r in results)
        step = max(1, max_exp // 40)  # Fewer frames for speed
        
        def update_exploration(frame):
            if not self.solving or frame > max_exp:
                # Start solution animation
                self.root.after(50, lambda: animate_solution(0))
                return
            for r in results:
                exp = r['explored'][:min(frame, len(r['explored']))]
                self._draw_maze(r['idx'], exp, None)
            self.root.after(max(5, self.speed // 4), lambda: update_exploration(frame + step))
        
        def animate_solution(frame):
            max_sol = max((len(r['solution']) for r in results if r['solution']), default=0)
            if not self.solving or frame > max_sol:
                finish_solve()
                return
            for r in results:
                if r['solution']:
                    sol = r['solution'][:min(frame, len(r['solution']))]
                    self._draw_maze(r['idx'], r['explored'], sol)
            self.root.after(max(5, self.speed // 8), lambda: animate_solution(frame + 1))
        
        def finish_solve():
            for r in results:
                self._draw_maze(r['idx'], r['explored'], r['solution'])
                if r['solution']:
                    st = self.stats[r['idx']]
                    st['path'].config(text=str(len(r['solution'])))
                    st['explored'].config(text=str(len(r['explored'])))
                    st['time'].config(text=f"{r['time']:.0f}ms")
            
            valid = [r for r in results if r['solution']]
            if valid:
                best = min(valid, key=lambda x: (len(x['solution']), len(x['explored'])))
                self.status_lbl.config(text=f"🏆 PLAYER {best['idx']+1} ({best['algo']}) WINS! ★ {len(best['solution'])} steps")
            
            self.solving = False
            self.btn_solve.config(state=tk.NORMAL)
            self.btn_gen.config(state=tk.NORMAL)
        
        self.root.after(10, lambda: update_exploration(0))
    
    def _clear(self):
        if self.solving:
            self.solving = False
        
        if self.maze:
            # Clear cache for clean redraw
            self.cell_ids = []
            self.drawn_states = []
            
            for i in range(self.num_players):
                self._draw_maze(i)
                self.stats[i]['path'].config(text="-")
                self.stats[i]['explored'].config(text="-")
                self.stats[i]['time'].config(text="-")
            self.status_lbl.config(text="🎮 READY FOR NEW GAME!")
        
        self.btn_solve.config(state=tk.NORMAL)
        self.btn_gen.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    root.resizable(True, True)
    
    w, h = 1000, 620
    x = (root.winfo_screenwidth() - w) // 2
    y = (root.winfo_screenheight() - h) // 2 - 30
    root.geometry(f'{w}x{h}+{x}+{y}')
    root.minsize(750, 550)
    
    SuperMazeBros(root)
    root.mainloop()


if __name__ == "__main__":
    main()
