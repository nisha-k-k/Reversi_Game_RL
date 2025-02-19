import numpy as np
import tkinter as tk
from tkinter import messagebox
import random

class Reversi:
    """Handles the game logic for Reversi (Othello)."""

    def __init__(self):
        self.board = np.zeros((8, 8), dtype=int) # creates 8 x 8 board
        self.board[3][3], self.board[4][4] = -1, -1  # Sets initial white pieces
        self.board[3][4], self.board[4][3] = 1, 1    # Sets initial black pieces
        self.current_player = 1 
        self.game_over = False  # Track if game has ended

    def get_valid_moves(self, player):
        """Returns a list of valid moves for the given player.
        D = Down
        U = Up
        L = Left
        R = Right

        Playable directions: (D1, L1), (D1), (D1, R1), (L1), (R1), (U1, L1), (U1), (U1, R1) 
        """
        
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)] 
        valid_moves = []
        
        for x in range(8):
            for y in range(8):
                if self.board[x, y] != 0:
                    continue
                for dx, dy in directions: #for each direction possibility
                    nx, ny = x + dx, y + dy 
                    captured = []
                    while 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx, ny] == -player:
                        captured.append((nx, ny))
                        nx += dx
                        ny += dy
                    if captured and 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx, ny] == player:
                        valid_moves.append((x, y))
                        break
        return valid_moves

    def make_move(self, x, y, player):
        """Places a piece and flips opponent's pieces if the move is valid."""
        if (x, y) not in self.get_valid_moves(player) or self.game_over:
            return False
        
        self.board[x, y] = player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            captured = []
            while 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx, ny] == -player:
                captured.append((nx, ny))
                nx += dx
                ny += dy
            if captured and 0 <= nx < 8 and 0 <= ny < 8 and self.board[nx, ny] == player:
                for cx, cy in captured:
                    self.board[cx, cy] = player

        self.current_player = -player
        return True

    def is_game_over(self):
        """Checks if the game is over (no valid moves for both players)."""
        if not self.get_valid_moves(1) and not self.get_valid_moves(-1):
            self.game_over = True  # Mark game as over
            return True
        return False

    def get_winner(self):
        """Determines the winner: 1 for Black, -1 for White, 0 for a tie."""
        score = np.sum(self.board)
        return 1 if score > 0 else -1 if score < 0 else 0

class ReversiGUI:
    """Handles the graphical interface using Tkinter."""

    def __init__(self, master):
        self.master = master
        self.master.title("Reversi (Othello)")
        self.game = Reversi()
        self.mode = None

        self.canvas = tk.Canvas(self.master, width=400, height=400, bg="green") #creates the look of the base board
        self.canvas.grid(row=0, column=0, columnspan=3)
        self.canvas.bind("<Button-1>", self.on_click)

        self.status_label = tk.Label(self.master, text="Select Game Mode", font=("Arial", 12))
        self.status_label.grid(row=1, column=0, columnspan=3)

        # Add Buttons for user to choose if they want User vs Ai or User vs User
        tk.Button(self.master, text="User vs AI", command=lambda: self.set_mode("AI")).grid(row=2, column=0)
        tk.Button(self.master, text="User vs User", command=lambda: self.set_mode("User")).grid(row=2, column=1)

        self.draw_board()

    def set_mode(self, mode):
        """Set game mode and restart game."""
        self.mode = mode
        self.game = Reversi()
        self.status_label.config(text="Black's Turn (X)")
        self.draw_board()

    def draw_board(self):
        """Draw the game board and pieces."""
        self.canvas.delete("all")
        for i in range(9):
            self.canvas.create_line(i * 50, 0, i * 50, 400, fill="black")
            self.canvas.create_line(0, i * 50, 400, i * 50, fill="black")

        for x in range(8):
            for y in range(8):
                piece = self.game.board[x, y]
                if piece == 1:
                    self.canvas.create_oval(y * 50 + 5, x * 50 + 5, y * 50 + 45, x * 50 + 45, fill="black")
                elif piece == -1:
                    self.canvas.create_oval(y * 50 + 5, x * 50 + 5, y * 50 + 45, x * 50 + 45, fill="white")

    def on_click(self, event):
        """Handles user clicks and makes a move."""
        if self.mode is None or self.game.game_over:
            return  # Prevent clicking after game over

        x, y = event.y // 50, event.x // 50
        if self.game.make_move(x, y, self.game.current_player):
            self.draw_board()
            if self.game.is_game_over():
                self.show_winner()
                return  # Stop further moves

            if self.mode == "AI" and self.game.current_player == -1:
                self.ai_move()

    def ai_move(self):
        """AI makes a move."""
        move = random.choice(self.game.get_valid_moves(-1)) if self.mode == "AI" else None
        if move:
            self.game.make_move(*move, -1)
            self.draw_board()
            if self.game.is_game_over():
                self.show_winner()

    def show_winner(self):
        """Displays the winner or game status in a pop-up message."""
        black_count = np.sum(self.game.board == 1)
        white_count = np.sum(self.game.board == -1)

        if not self.game.get_valid_moves(1) and not self.game.get_valid_moves(-1):
            messagebox.showinfo("Game Over", f"No more valid moves!\nBlack: {black_count}  White: {white_count}")

        winner = self.game.get_winner()
        if self.mode == "AI":
            if winner == 1:
                messagebox.showinfo("Game Over", f"You win! 🎉\nBlack: {black_count}  White: {white_count}")
            elif winner == -1:
                messagebox.showinfo("Game Over", f"You lose! 😢\nBlack: {black_count}  White: {white_count}")
            else:
                messagebox.showinfo("Game Over", f"It's a tie! 🤝\nBlack: {black_count}  White: {white_count}")
        else:  # User vs User
            if winner == 1:
                messagebox.showinfo("Game Over", f"Black wins! 🏆\nBlack: {black_count}  White: {white_count}")
            elif winner == -1:
                messagebox.showinfo("Game Over", f"White wins! 🏆\nBlack: {black_count}  White: {white_count}")
            else:
                messagebox.showinfo("Game Over", f"It's a tie! 🤝\nBlack: {black_count}  White: {white_count}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ReversiGUI(root)
    root.mainloop()
