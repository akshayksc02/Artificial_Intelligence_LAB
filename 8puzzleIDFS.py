# 8 Puzzle using IDDFS
# 0 represents the blank space

start = (2, 8, 3,
         1, 6, 4,
         7, 0, 5)

goal = (1, 2, 3,
        8, 0, 4,
        7, 6, 5)


# Print the puzzle
def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()


# Generate all possible moves
def get_neighbors(state):

    neighbors = []

    # Find blank position
    blank = state.index(0)

    row = blank // 3
    col = blank % 3

    # Up, Down, Left, Right
    moves = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    for dr, dc in moves:

        new_row = row + dr
        new_col = col + dc

        # Check whether move is valid
        if 0 <= new_row < 3 and 0 <= new_col < 3:

            new_blank = new_row * 3 + new_col

            # Make a new puzzle
            new_state = list(state)

            # Swap blank with tile
            new_state[blank], new_state[new_blank] = \
                new_state[new_blank], new_state[blank]

            neighbors.append(tuple(new_state))

    return neighbors


# Depth Limited DFS
def depth_limited_search(state, goal, depth, path):

    # Goal found
    if state == goal:
        return path

    # Depth limit reached
    if depth == 0:
        return None

    # Explore neighbors
    for neighbor in get_neighbors(state):

        # Don't go back to a state already in current path
        if neighbor not in path:

            result = depth_limited_search(
                neighbor,
                goal,
                depth - 1,
                path + [neighbor]
            )

            if result is not None:
                return result

    return None


# IDDFS
def iddfs(start, goal):

    depth = 0

    while True:

        print("Searching at depth:", depth)

        path = depth_limited_search(
            start,
            goal,
            depth,
            [start]
        )

        if path is not None:
            return path

        depth += 1


# Solve the puzzle
solution = iddfs(start, goal)


# Print solution
print("\nSolution found!")
print("Number of moves:", len(solution) - 1)

for step in solution:
    print_puzzle(step)
