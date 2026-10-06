board = [' ' for _ in range(9)]

def print_board():
    for i in range(0, 9, 3):
        print('| ' + ' | '.join(board[i:i+3]) + ' |')


def check_winner(player):
    win_states = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for state in win_states:
        if all(board[i] == player for i in state):
            return True

    return False


def find_ai_move():
    # 1. Can AI win?
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'

            if check_winner('O'):
                board[i] = ' '
                return i

            board[i] = ' '

    # 2. Can player win? Block them.
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'

            if check_winner('X'):
                board[i] = ' '
                return i

            board[i] = ' '

    # 3. Take center
    if board[4] == ' ':
        return 4

    # 4. Take a corner
    for i in [0, 2, 6, 8]:
        if board[i] == ' ':
            return i

    # 5. Take any remaining space
    for i in range(9):
        if board[i] == ' ':
            return i


print("Tic-Tac-Toe")
print("Positions are 0-8")

while ' ' in board:

    print_board()

    # Human
    try:
        move = int(input("Your move: "))

        if move < 0 or move > 8:
            print("Choose 0-8.")
            continue

        if board[move] != ' ':
            print("That cell is already taken.")
            continue

    except ValueError:
        print("Enter a number.")
        continue

    board[move] = 'X'

    if check_winner('X'):
        print_board()
        print("You win!")
        break

    if ' ' not in board:
        print_board()
        print("Draw!")
        break

    # AI
    ai_move = find_ai_move()
    board[ai_move] = 'O'

    print("AI chose:", ai_move)

    if check_winner('O'):
        print_board()
        print("AI wins!")
        break
