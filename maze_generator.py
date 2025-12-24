import random

# ==========================================
# 1. THE MODEL
# Responsibility: Handles data and logic (The Algorithm)
# ==========================================
class MazeModel:
    def __init__(self, width, height):
        # Ensure odd dimensions for the grid
        self.width = width if width % 2 != 0 else width + 1
        self.height = height if height % 2 != 0 else height + 1
        self.grid = self._initialize_grid()

    def _initialize_grid(self):
        # Create a grid filled with walls
        return [["#" for _ in range(self.width)] for _ in range(self.height)]

    def generate_maze(self):
        """
        The Core Logic: Recursive Backtracker (DFS)
        """
        start_x, start_y = 1, 1
        self.grid[start_y][start_x] = " "
        
        stack = [(start_x, start_y)]

        while stack:
            current_x, current_y = stack[-1] # -1 just gets the top of the stack (stack here is actually a normal list that works as a stack by enforcing stack rules)
            neighbors = self._get_unvisited_neighbors(current_x, current_y)

            if neighbors:
                next_x, next_y = random.choice(neighbors)
                
                # Remove wall between current and next
                wall_x = (current_x + next_x) // 2
                wall_y = (current_y + next_y) // 2
                self.grid[wall_y][wall_x] = " "
                
                # Mark next cell as path
                self.grid[next_y][next_x] = " "
                stack.append((next_x, next_y))
            else:
                stack.pop()

    def _get_unvisited_neighbors(self, x, y):
        # Helper logic to find valid moves
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        neighbors = []
        
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < self.width and 0 < ny < self.height:
                if self.grid[ny][nx] == "#":
                    neighbors.append((nx, ny))
        return neighbors

    def get_data(self):
        # Return the raw data (grid) for the View to consume
        return self.grid
    