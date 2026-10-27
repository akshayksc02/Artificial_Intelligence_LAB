import math
import random

def get_heuristic_cost(board):
    """Calculates the number of attacking queen pairs (h)."""
    n = len(board)
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def get_random_neighbor(board):
    """
    Picks a single random column and changes its queen's row to a different position.
    """
    n = len(board)
    neighbor = list(board)
    col = random.randint(0, n - 1)
    
    # Select a row different from current position
    new_row = random.randint(0, n - 1)
    while new_row == board[col]:
        new_row = random.randint(0, n - 1)
        
    neighbor[col] = new_row
    return neighbor

def simulated_annealing_n_queens(n=8, initial_temp=100.0, cooling_rate=0.995, min_temp=0.0001):
    """
    Solves N-Queens using Simulated Annealing.
    """
    # 1. Initialize random state
    current_board = [random.randint(0, n - 1) for _ in range(n)]
    current_cost = get_heuristic_cost(current_board)
    
    temperature = initial_temp
    step = 0

    print(f"Initial State: {current_board} | Initial Conflicts (h): {current_cost}\n")

    while temperature > min_temp and current_cost > 0:
        # Pick a single random neighbor
        neighbor = get_random_neighbor(current_board)
        neighbor_cost = get_heuristic_cost(neighbor)

        # Delta E: change in energy/cost (positive means worsening cost)
        delta_e = neighbor_cost - current_cost

        # If neighbor is better, always accept it.
        # If neighbor is worse, accept with probability P = exp(-delta_e / T)
        if delta_e < 0:
            current_board = neighbor
            current_cost = neighbor_cost
        else:
            acceptance_probability = math.exp(-delta_e / temperature)
            if random.random() < acceptance_probability:
                current_board = neighbor
                current_cost = neighbor_cost

        # Cool down the system
        temperature *= cooling_rate
        step += 1

    # Check outcome
    if current_cost == 0:
        print(f"Success! Global solution found in {step} steps.")
        print(f"Final State: {current_board} | Remaining Conflicts: 0")
        return current_board, True
    else:
        print(f"Failed to find a global optimum before cooling completed after {step} steps.")
        print(f"Final State: {current_board} | Remaining Conflicts (h): {current_cost}")
        return current_board, False

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
    solution_board, is_success = simulated_annealing_n_queens(n=8)
    
    if is_success:
        print("\nVisual Board:")
        print_board(solution_board)