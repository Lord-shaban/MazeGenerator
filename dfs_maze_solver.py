# DFS maze.py

class DFSMazeSolver:
    def __init__(self, maze):
        """
        maze: Maze object from main.py
        Expected attributes:
            - maze.grid  -> 2D list of characters
            - maze.rows  -> number of rows
            - maze.cols  -> number of columns
        """
        self.maze = maze
        self.grid = maze.grid
        self.rows = maze.rows
        self.cols = maze.cols


    def solve(self):
        """
        Solves the maze using DFS.
        Returns:
            path -> list of (row, col) from start 'S' to end 'E'
        """

        start, goal = self._find_start_and_goal()

        stack = [start]                 
        visited = set([start])          
        parent = {start: None}
        explored = [] # <--- 1. Added list

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while stack:
            r, c = stack.pop()
            explored.append((r, c)) # <--- 2. Track explored

            if (r, c) == goal:
                break

            for dr, dc in directions:
                nr, nc = r + dr, c + dc

                if self._is_valid_move(nr, nc, visited):
                    visited.add((nr, nc))
                    parent[(nr, nc)] = (r, c)
                    stack.append((nr, nc))

        # <--- 3. Return tuple
        return self._reconstruct_path(parent, goal), explored

    # -------------------------------------------------
    # Helper functions
    # -------------------------------------------------

    def _find_start_and_goal(self):
        start = goal = None

        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 'S':
                    start = (r, c)
                elif self.grid[r][c] == 'E':
                    goal = (r, c)

        if start is None or goal is None:
            raise ValueError("Maze must contain 'S' (start) and 'E' (end)")

        return start, goal

    def _is_valid_move(self, r, c, visited):
        return (
            0 <= r < self.rows and
            0 <= c < self.cols and
            self.grid[r][c] != '#' and
            (r, c) not in visited
        )

    def _reconstruct_path(self, parent, goal):
        path = []
        cell = goal

        while cell is not None:
            path.append(cell)
            cell = parent.get(cell)

        path.reverse()
        return path
