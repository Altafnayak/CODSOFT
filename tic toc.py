#Altaf
#tic toc
import tkinter as tk
import math

PLAYER_X = "X"
PLAYER_O = "O"
EMPTY = " "
WINNING_COMBINATIONS = [
    [(0, 0), (0, 1), (0, 2)],  
    [(1, 0), (1, 1), (1, 2)],   
    [(2, 0), (2, 1), (2, 2)],   
    [(0, 0), (1, 0), (2, 0)], 
    [(0, 1), (1, 1), (2, 1)],  
    [(0, 2), (1, 2), (2, 2)],  
    [(0, 0), (1, 1), (2, 2)],  
    [(0, 2), (1, 1), (2, 0)],  
]

def initialize_board():
    return [[EMPTY for _ in range(3)] for _ in range(3)]


def is_game_over(board):
    for combination in WINNING_COMBINATIONS:
        first = board[combination[0][0]][combination[0][1]]
        if first != EMPTY and all(board[row][col] == first for row, col in combination):
            return first
    if all(cell != EMPTY for row in board for cell in row):
        return "Tie"
    return None

def minimax(board, depth, alpha, beta, is_maximizing):
    result = is_game_over(board)
    if result:
        if result == PLAYER_X:
            return -1
        elif result == PLAYER_O:
            return 1
        else:  
            return 0
    
    if is_maximizing:
        best_score = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_O
                    score = minimax(board, depth + 1, alpha, beta, False)
                    board[i][j] = EMPTY
                    best_score = max(score, best_score)
                    alpha = max(alpha, best_score)
                    if beta <= alpha:
                        break  
        return best_score
    else:
        best_score = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_X
                    score = minimax(board, depth + 1, alpha, beta, True)
                    board[i][j] = EMPTY
                    best_score = min(score, best_score)
                    beta = min(beta, best_score)
                    if beta <= alpha:
                        break  
        return best_score


def find_best_move(board):
    best_score = -math.inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = PLAYER_O
                score = minimax(board, 0, -math.inf, math.inf, False)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

def on_click(row, col):
    global board, turn
    if board[row][col] == EMPTY and not game_over and turn == PLAYER_X:
        board[row][col] = PLAYER_X
        buttons[row][col].config(text=PLAYER_X, state=tk.DISABLED)
        if not is_game_over(board):
            turn = PLAYER_O
            update_turn_indicator()
            ai_move()

def ai_move():
    global turn
    if game_over:
        return
    move = find_best_move(board)
    if move != (-1, -1):
        row, col = move
        board[row][col] = PLAYER_O
        buttons[row][col].config(text=PLAYER_O, state=tk.DISABLED)
    if is_game_over(board):
        display_result()
    else:
        turn = PLAYER_X
        update_turn_indicator()

def highlight_winner(combination):
    for row, col in combination:
        buttons[row][col].config(bg="green", fg="white", font=("Arial", 16, "bold"))

def update_turn_indicator():
    if turn == PLAYER_X:
        turn_indicator.config(text="Player X's Turn", fg="blue")
    else:
        turn_indicator.config(text="Player O's Turn (AI)", fg="red")

def display_result():
    global game_over
    result = is_game_over(board)
    game_over = True
    if result == PLAYER_X:
        result_label.config(text="Player X Wins!", fg="white", bg="blue", font=("Arial", 20, "bold"))
    elif result == PLAYER_O:
        result_label.config(text="Player O Wins!", fg="white", bg="red", font=("Arial", 20, "bold"))
    elif result == "Tie":
        result_label.config(text="It's a Tie!", fg="white", bg="gray", font=("Arial", 20, "bold"))
    
    if result in [PLAYER_X, PLAYER_O]:
        for combination in WINNING_COMBINATIONS:
            first = board[combination[0][0]][combination[0][1]]
            if first != EMPTY and all(board[row][col] == first for row, col in combination):
                highlight_winner(combination)
                break

    for i in range(3):
        for j in range(3):
            buttons[i][j].config(state=tk.DISABLED)

def reset_game():
    global board, turn, game_over
    board = initialize_board()
    turn = PLAYER_X
    game_over = False
    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text=EMPTY, state=tk.NORMAL, bg="SystemButtonFace")
    update_turn_indicator()

root = tk.Tk()
root.title("Tic-Tac-Toe")

board = initialize_board()
turn = PLAYER_X  
game_over = False

buttons = [[None for _ in range(3)] for _ in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j] = tk.Button(root, text=EMPTY, width=10, height=3,
                                  command=lambda i=i, j=j: on_click(i, j))
        buttons[i][j].grid(row=i, column=j)

result_label = tk.Label(root, text="", font=("Arial", 16), width=20, height=2)
result_label.grid(row=3, column=0, columnspan=3)

turn_indicator = tk.Label(root, text="Player X's Turn", font=("Arial", 14), fg="blue")
turn_indicator.grid(row=4, column=0, columnspan=3)

reset_button = tk.Button(root, text="Restart", command=reset_game)
reset_button.grid(row=5, column=0, columnspan=3)

update_turn_indicator()
root.mainloop()
