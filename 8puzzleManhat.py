# 8 Puzzle using A* Search
# g(n) = depth
# h(n) = Manhattan distance
# f(n) = g(n) + h(n)

start = (2, 8, 3,
         1, 6, 4,
         7, 0, 5)

goal = (1, 2, 3,
        8, 0, 4,
        7, 6, 5)


# Print puzzle
def print_puzzle(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()


# Generate possible moves
def get_neighbors(state):

    neighbors = []

    # Find blank
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

        # Check valid position
        if 0 <= new_row < 3 and 0 <= new_col < 3:

            new_blank = new_row * 3 + new_col

            # Create new state
            new_state = list(state)

            # Swap blank with tile
            new_state[blank], new_state[new_blank] = \
                new_state[new_blank], new_state[blank]

            neighbors.append(tuple(new_state))

    return neighbors


# Manhattan Distance Heuristic
def manhattan_distance(state):

    distance = 0

    for i in range(9):

        # Don't calculate distance for blank
        if state[i] == 0:
            continue

        # Current position
        current_row = i // 3
        current_col = i % 3

        # Find where this tile belongs in goal
        goal_position = goal.index(state[i])

        goal_row = goal_position // 3
        goal_col = goal_position % 3

        # Manhattan distance
        distance += abs(current_row - goal_row)
        distance += abs(current_col - goal_col)

    return distance


# A* Search
def a_star(start, goal):

    # (f, g, state, path)
    open_list = []

    # Starting node
    g = 0
    h = manhattan_distance(start)
    f = g + h

    open_list.append((f, g, start, [start]))

    visited = set()

    while open_list:

        # Find state with smallest f
        best_index = 0

        for i in range(1, len(open_list)):

            if open_list[i][0] < open_list[best_index][0]:
                best_index = i

        # Remove best state
        f, g, state, path = open_list.pop(best_index)

        # Skip already visited states
        if state in visited:
            continue

        visited.add(state)

        # Goal reached
        if state == goal:
            return path

        # Generate neighbors
        for neighbor in get_neighbors(state):

            if neighbor not in visited:

                # g(n) = depth
                new_g = g + 1

                # h(n) = Manhattan distance
                new_h = manhattan_distance(neighbor)

                # f(n) = g(n) + h(n)
                new_f = new_g + new_h

                open_list.append(
                    (new_f, new_g, neighbor, path + [neighbor])
                )

        print(open_list)

    return None


# Solve puzzle
solution = a_star(start, goal)


# Print solution
if solution:

    print("Solution found!")
    print("Number of moves:", len(solution) - 1)

    for step in solution:
        print_puzzle(step)

else:
    print("No solution found.")
