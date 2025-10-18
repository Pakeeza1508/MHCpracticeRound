import sys
import collections

def solve():
    """
    Solves a single test case for the Guardian Boundary problem.
    """
    try:
        R, C, S = map(int, sys.stdin.readline().split())
        grid = [sys.stdin.readline().strip() for _ in range(R)]
    except (IOError, ValueError):
        return 0

    # Phase 1: Calculate shortest distance from each cell to the nearest '#' object
    # using a multi-source Breadth-First Search (BFS).
    dist = [[float('inf')] * C for _ in range(R)]
    q = collections.deque()

    for r in range(R):
        for c in range(C):
            if grid[r][c] == '#':
                dist[r][c] = 0
                q.append((r, c))

    # Standard BFS traversal
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    while q:
        r, c = q.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and dist[nr][nc] == float('inf'):
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))

    # Phase 2: Identify all safe cells and find the largest connected component.
    # A cell is safe if its distance to the nearest '#' AND nearest wall is >= S + 1.
    
    visited = [[False] * C for _ in range(R)]
    max_area = 0

    for r_start in range(R):
        for c_start in range(C):
            # Check if this cell is safe and part of a component we haven't counted yet.
            dist_to_wall = min(r_start + 1, R - r_start, c_start + 1, C - c_start)
            is_safe = dist[r_start][c_start] >= S + 1 and dist_to_wall >= S + 1

            if is_safe and not visited[r_start][c_start]:
                # Found a new safe area. Let's find its size.
                current_area = 0
                comp_q = collections.deque([(r_start, c_start)])
                visited[r_start][c_start] = True
                
                while comp_q:
                    r, c = comp_q.popleft()
                    current_area += 1
                    
                    for dr, dc in directions:
                        nr, nc = r + dr, c + dc
                        
                        if 0 <= nr < R and 0 <= nc < C and not visited[nr][nc]:
                            # Check if the neighbor cell is also safe.
                            # We must re-check conditions, as we didn't pre-build an is_safe grid.
                            neighbor_dist_to_wall = min(nr + 1, R - nr, nc + 1, C - nc)
                            is_neighbor_safe = dist[nr][nc] >= S + 1 and neighbor_dist_to_wall >= S + 1

                            if is_neighbor_safe:
                                visited[nr][nc] = True
                                comp_q.append((nr, nc))
                
                max_area = max(max_area, current_area)

    return max_area

def main():
    """
    Main function to read input and handle multiple test cases.
    """
    try:
        num_test_cases = int(sys.stdin.readline())
    except (IOError, ValueError):
        return

    for i in range(1, num_test_cases + 1):
        result = solve()
        print(f"Case #{i}: {result}")

if __name__ == "__main__":
    main()

# to run this file
    # Get-Content zone_in_input.txt | python problem2.py 
    # Get-Content zone_in_input.txt | python problem2.py > zone_in_output.txt