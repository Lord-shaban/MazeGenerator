def bfs_maze_solver(maze, start, end, wall_char='#'):

    '''
    Finds the shortest path between a start and end point in a grid using (Breadth-First Search (BFS)).
        #===========
        #Parameters:
        #===========
        # Inputs:
        #--------
        # maze : list[list] [A 2D grid representing the maze. Each element can be a character or integer.]
        # start : tuple (row, col) [The starting coordinates, e.g., (0, 0).]
        # end : tuple (row, col) [The target coordinates to reach, e.g., (5, 5).]
        # wall_char : anything actually it's optional but (default='#') [The value inside the maze grid that represents a wall/obstacle.]
        # The algorithm will not traverse cells containing this value.

        #Returns:
        #--------
        # list[tuple] or None
        # - List[tuple]: Returns a list of coordinates [(r, c), (r, c), ...] representing the path from start to end (inclusive).
        # - None: Returns None if the end is unreachable (blocked by walls).
    '''

    rows, cols = len(maze), len(maze[0])
    queue = [(start, [start])]
    visited = {start}
    explored = [] # <--- 1. Added list
    
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        (curr_r, curr_c), path = queue.pop(0)
        explored.append((curr_r, curr_c)) # <--- 2. Track explored

        if (curr_r, curr_c) == end:
            return path, explored # <--- 3. Return tuple

        for dr, dc in moves:
            nr, nc = curr_r + dr, curr_c + dc
            if (0 <= nr < rows and 0 <= nc < cols and
                    maze[nr][nc] != wall_char and (nr, nc) not in visited):
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))

    return None, explored # <--- 4. Return tuple

#============================================================================================================
# ==================== 2. The Test Suite =========================
def tests():
    print("Running Maze Solver Tests...\n")

    # TEST CASE 1: Standard Maze (Path exists)
    maze_1 = [
        ['S', '#', ' ', 'E'],
        [' ', '#', ' ', ' '],
        [' ', ' ', ' ', ' ']
    ]
    # We expect it to go down, around the wall, and up to E
    result_1 = bfs_maze_solver(maze_1, (0, 0), (0, 3))
    assert result_1 is not None, "Test 1 Failed: Path should exist"
    assert result_1[-1] == (0, 3), "Test 1 Failed: Did not reach end"
    print("Test 1 Passed: Standard path found.")

    # TEST CASE 2: Blocked Maze (No path)
    maze_2 = [
        ['S', '#', 'E'],
        [' ', '#', ' '],
        ['#', '#', '#']
    ]
    result_2 = bfs_maze_solver(maze_2, (0, 0), (0, 2))
    assert result_2 is None, "Test 2 Failed: Should return None for blocked path"
    print("Test 2 Passed: Correctly identified blocked path.")

    # TEST CASE 3: Direct Neighbor
    maze_3 = [
        ['S', 'E'],
        [' ', ' ']
    ]
    result_3 = bfs_maze_solver(maze_3, (0, 0), (0, 1))
    expected_len = 2  # [(0,0), (0,1)]
    assert len(result_3) == expected_len, "Test 3 Failed: Path should be direct"
    print("Test 3 Passed: Found immediate neighbor.")

    print("\nAll tests passed successfully!")

# --- 3. Run It ---
if __name__ == "__main__":
    tests()