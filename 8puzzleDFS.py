# 8 Puzzle using DFS

start = (2, 8, 3,
         1, 6, 4,
         7, 0, 5)

goal = (1, 2, 3,
        8, 0, 4,
        7, 6, 5)


def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()


def get_neighbors(state):
    neighbors = []

    # Position of blank (0)
    blank = state.index(0)

    row = blank // 3
    col = blank % 3

    # Possible moves: up, down, left, right
    moves = [
        (-1, 0),  # up
        (1, 0),   # down
        (0, -1),  # left
        (0, 1)    # right
    ]

    for dr, dc in moves:

        new_row = row + dr
        new_col = col + dc

        # Check if new position is inside board
        if 0 <= new_row < 3 and 0 <= new_col < 3:

            new_blank = new_row * 3 + new_col

            # Convert tuple to list so we can swap
            new_state = list(state)

            new_state[blank], new_state[new_blank] = \
                new_state[new_blank], new_state[blank]

            neighbors.append(tuple(new_state))

    return neighbors


def dfs(start, goal):

    # Stack for DFS
    stack = [(start, [])]

    # Remember visited states
    visited = set()

    while stack:

        state, path = stack.pop()

        # Already visited?
        if state in visited:
            continue

        visited.add(state)

        # Goal reached
        if state == goal:
            return path + [state]

        # Explore neighbors
        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                stack.append((neighbor, path + [state]))

    return None


# Solve puzzle
solution = dfs(start, goal)


if solution:
    print("Solution found!")
    print("Number of moves:", len(solution) - 1)

    for step in solution:
        print_puzzle(step)

else:
    print("No solution found.")
