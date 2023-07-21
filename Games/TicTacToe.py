import random

def print_board(board):
    for row in board:
        print(' | '.join(row))
        print('-' * 9)

def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True

    for col in range(3):
        if all(row[col] == player for row in board):
            return True

    if all(board[i][i] == player for i in range(3)) or all(board[i][2-i] == player for i in range(3)):
        return True

    return False

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

def get_player_move():
    row = int(input('Your turn! Enter row (0-2): '))
    col = int(input('Your turn! Enter column (0-2): '))
    return row, col

def get_computer_move(board):
    empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col] == ' ']
    return random.choice(empty_cells)

def tic_tac_toe():
    board = [[' ' for _ in range(3)] for _ in range(3)]
    players = ['X', 'O']

    while True:
        for player in players:
            print_board(board)

            if player == 'X':
                row, col = get_player_move()
            else:
                row, col = get_computer_move(board)

            if board[row][col] == ' ':
                board[row][col] = player
                if check_win(board, player):
                    print_board(board)
                    if player == 'X':
                        print('Congratulations! You win!')
                    else:
                        print('Computer wins!')
                    return
                elif is_board_full(board):
                    print_board(board)
                    print('It\'s a draw!')
                    return

if __name__ == "__main__":
    tic_tac_toe()