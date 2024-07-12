import tkinter as tk
from tkinter import messagebox
import math

# Function to check if there is a winner
def check_win(board, player):
    for row in board:
        if all([spot == player for spot in row]):
            return True
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    if all([board[i][i] == player for i in range(3)]) or all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

# Function to check if the game is a draw
def check_draw(board):
    for row in board:
        if any([spot == " " for spot in row]):
            return False
    return True

# Minimax algorithm with alpha-beta pruning
def minimax(board, depth, is_maximizing):
    if check_win(board, "O"):
        return 1
    if check_win(board, "X"):
        return -1
    if check_draw(board):
        return 0

    if is_maximizing:
        best_score = -math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = math.inf
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = " "
                    best_score = min(score, best_score)
        return best_score

# Function to determine the best move for the computer
def best_move(board):
    best_score = -math.inf
    move = None
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                board[row][col] = "O"
                score = minimax(board, 0, False)
                board[row][col] = " "
                if score > best_score:
                    best_score = score
                    move = (row, col)
    return move

class TicTacToeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe Game")
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.player = "X"
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.create_board()

    def create_board(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(self.root, text=" ", font='normal 20 bold', height=3, width=6, command=lambda row=row, col=col: self.click(row, col))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def click(self, row, col):
        if self.board[row][col] == " ":
            self.board[row][col] = self.player
            self.buttons[row][col].config(text=self.player)
            if check_win(self.board, self.player):
                self.end_game(f"{self.player} wins!")
            elif check_draw(self.board):
                self.end_game("Draw!")
            else:
                self.player = "O" if self.player == "X" else "X"
                if self.player == "O":
                    move = best_move(self.board)
                    if move:
                        self.click(move[0], move[1])

    def end_game(self, result):
        messagebox.showinfo("Game Over", result)
        self.reset_board()

    def reset_board(self):
        self.board = [[" " for _ in range(3)] for _ in range(3)]
        self.player = "X"
        for row in range(3):
            for col in range(3):
                self.buttons[row][col].config(text=" ")

def main():
    root = tk.Tk()
    game = TicTacToeGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
