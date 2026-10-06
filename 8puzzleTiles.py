# 8 Puzzle using A* Search
# g(n) = depth
# h(n) = number of misplaced tiles
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

            # Swap blank
            new_state[blank], new_state[new_blank] = \
                new_state[new_blank], new_state[blank]

            neighbors.append(tuple(new_state))

    return neighbors


# Heuristic function
# h(n) = number of misplaced tiles
def misplaced_tiles(state):

    count = 0

    for i in range(9):

        # Don't count the blank
        if state[i] != 0 and state[i] != goal[i]:
            count += 1

    return count


# A* Search
def a_star(start, goal):

    # Each item:
    # (f, g, state, path)
    open_list = []

    # Starting node
    g = 0
    h = misplaced_tiles(start)
    f = g + h

    open_list.append((f, g, start, [start]))

    # Already explored states
    visited = set()

    while open_list:

        # Find node with smallest f
        best_index = 0

        for i in range(1, len(open_list)):
            if open_list[i][0] < open_list[best_index][0]:
                best_index = i

        # Remove best node
        f, g, state, path = open_list.pop(best_index)

        # Skip if already visited
        if state in visited:
            continue

        visited.add(state)

        # Goal found
        if state == goal:
            return path

        # Generate children
        for neighbor in get_neighbors(state):

            if neighbor not in visited:

                # g(n) = depth
                new_g = g + 1

                # h(n) = misplaced tiles
                new_h = misplaced_tiles(neighbor)

                # f(n) = g(n) + h(n)
                new_f = new_g + new_h

                # Add to open list
                open_list.append(
                    (new_f, new_g, neighbor, path + [neighbor])
                )

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
