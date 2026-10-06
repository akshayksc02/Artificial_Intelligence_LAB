import math

# Initialize the 3x3 board
board = [' ' for _ in range(9)]

def print_board():
    for row in [board[i*3:(i+1)*3] for i in range(3)]:
        print('| ' + ' | '.join(row) + ' |')

def check_winner(b, player):
    win_states = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Horizontal
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Vertical
        [0, 4, 8], [2, 4, 6]             # Diagonal
    ]
    return any(all(b[cell] == player for cell in state) for state in win_states)

def moves_left(b):
    return ' ' in b

# The Minimax Function
def minimax(b, depth, is_max):
    if check_winner(b, 'O'): return 10 - depth  # AI wins (prefer faster wins)
    if check_winner(b, 'X'): return depth - 10  # Human wins (prefer delayed losses)
    if not moves_left(b): return 0              # Draw

    if is_max:
        best = -math.inf
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'O'
                best = max(best, minimax(b, depth + 1, False))
                b[i] = ' '
        return best
    else:
        best = math.inf
        for i in range(9):
            if b[i] == ' ':
                b[i] = 'X'
                best = min(best, minimax(b, depth + 1, True))
                b[i] = ' '
        return best

# Find the best move for the AI ('O')
def find_best_move(b):
    best_val = -math.inf
    best_move = -1
    for i in range(9):
        if b[i] == ' ':
            b[i] = 'O'
            move_val = minimax(b, 0, False)
            b[i] = ' '
            if move_val > best_val:
                best_val = move_val
                best_move = i
    return best_move

# Main Game Loop
print("Welcome to Tic-Tac-Toe AI! Enter a position from 0-8.")
print_board()

while moves_left(board) and not check_winner(board, 'X') and not check_winner(board, 'O'):
    # Human Turn
    try:
        human_move = int(input("\nYour move (0-8): "))
        if board[human_move] != ' ':
            print("Cell already taken! Try again.")
            continue
    except (ValueError, IndexError):
        print("Invalid input. Choose a number between 0 and 8.")
        continue
        
    board[human_move] = 'X'
    print_board()
    
    if check_winner(board, 'X') or not moves_left(board):
        break
        
    # AI Turn
    print("\nAI is thinking...")
    ai_move = find_best_move(board)
    board[ai_move] = 'O'
    print_board()

# Game Result
if check_winner(board, 'O'):
    print("\nThe AI wins! Better luck next time.")
elif check_winner(board, 'X'):
    print("\nAmazing! You beat the AI (This shouldn't happen!).")
else:
    print("\nIt's a draw!")