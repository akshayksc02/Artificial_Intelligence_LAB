import random

def get_heuristic_cost(board):
    """
    Calculates the number of attacking queen pairs.
    board[i] represents the row index of the queen in column i.
    """
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            # Same row
            if board[i] == board[j]:
                conflicts += 1
            # Same diagonal: |row_i - row_j| == |col_i - col_j|
            elif abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_best_neighbor(board):
    """
    Finds the neighbor state with the minimum conflict count
    by moving one queen at a time within its column.
    """
    n = len(board)
    current_cost = get_heuristic_cost(board)
    best_board = list(board)
    best_cost = current_cost

    for col in range(n):
        original_row = board[col]
        for row in range(n):
            if row != original_row:
                temp_board = list(board)
                temp_board[col] = row
                cost = get_heuristic_cost(temp_board)
                
                if cost < best_cost:
                    best_cost = cost
                    best_board = temp_board

        board[col] = original_row

    return best_board, best_cost

def hill_climbing_n_queens(n):
    """
    Standard Steepest-Ascent Hill Climbing without Restarts.
    Stops and fails if trapped in a local minimum/plateau.
    """
    # 1. Generate an initial random state (one queen per column)
    current_board = [random.randint(0, n - 1) for _ in range(n)]
    current_cost = get_heuristic_cost(current_board)
    step = 0

    print(f"Initial State: {current_board} | Initial Conflicts (h): {current_cost}\n")

    while True:
        # Goal state reached
        if current_cost == 0:
            print(f"Success! Global solution found in {step} steps.")
            return current_board, True

        # Find the best neighboring state
        neighbor_board, neighbor_cost = get_best_neighbor(current_board)

        # Local Minimum or Plateau reached: no neighbor strictly improves the cost
        if neighbor_cost >= current_cost:
            print(f"Stuck at Local Minimum/Plateau after {step} steps.")
            print(f"Final State: {current_board} | Remaining Conflicts (h): {current_cost}")
            return current_board, False

        # Move to the better neighbor
        current_board = neighbor_board
        current_cost = neighbor_cost
        step += 1

def print_board(board):
    """Utility function to display the board visually."""
    n = len(board)
    for row in range(n):
        line = ""
        for col in range(n):
            if board[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)

# --- Execution Example ---
if __name__ == "__main__":
    N = 8
    final_board, is_solution = hill_climbing_n_queens(N)
    
    if is_solution:
        print("\nVisual Representation of Solution:")
        print_board(final_board)
    else:
        print("\nNo solution found (trapped in local minimum). Run again to try a different initial random state.")