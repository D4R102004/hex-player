from __future__ import annotations

import math
import tkinter as tk

from src.Urrutia_Dario_Alfonso.board import HexBoard
from src.Urrutia_Dario_Alfonso.solution import SmartPlayer


class HexGame:
    """
    Model layer of the HEX game.

    Tracks the board state, players, turn order,
    and win condition. Independent of any GUI framework.
    """

    def __init__(self, size: int = 11, human_id: int = 1) -> None:
        """
        Initializes a new HEX game session.

        Args:
            size: The dimension of the NxN board (default is 11).
            human_id: The player ID for the human player (1 or 2, default is 1).
        """

        # Board
        self.size = size
        self.board = HexBoard(size=size)

        # Players
        self.human_id = human_id
        self.ai_id = 3 - human_id
        self.ai = SmartPlayer(player_id=self.ai_id)

        # Game state
        self.current_player = 1
        self.game_over = False
        self.winner: int | None = None

    def make_move(self, row: int, col: int) -> bool:
        """
        Processes a move for the current player.

        Args:
            row: The row index for the move.
            col: The column index for the move.

        Returns:
            True if the move was successful, False if the move was invalid
            (e.g., cell already occupied or game already over).
        """

        if not self.game_over:
            if self.board.place_piece(row, col, player_id=self.current_player):
                if self.board.check_connection(self.current_player):
                    self.game_over = True
                    self.winner = self.current_player
                else:
                    self.current_player = 3 - self.current_player  # Switch player

                return True

        return False

    def is_human_turn(self) -> bool:
        """
        Defines wether it is the human player's turn

        Returns:
          True if it's the human player's turn
        """

        return self.current_player == self.human_id

    def get_ai_move(self) -> tuple[int, int] | None:
        """
        Gets the AI's move if it's the AI's turn.

        Returns:
            A tuple (row, col) for the AI's move, or None if it's not the AI's turn.
        """

        if not self.game_over and self.current_player == self.ai_id:
            return self.ai.play(self.board)

        return None


class HexView:
    """
    View layer of the HEX game.
    Responsible for rendering the board, pieces, and game status
    using tkinter. Does not modify game state.
    """

    def __init__(self, game: HexGame, cell_size: int = 50) -> None:
        """
        Initialize the game display.

        Args:
            game: The HexGame instance to visualize.
            cell_size: The pixel size of each cell in the grid (default is 50).
        """

        self.root = tk.Tk()
        self.game = game
        self.cell_size = cell_size
        self.padding = cell_size
        self.root.title("HEX — SmartPlayer")

        width = int(game.size * cell_size * 2.5) + self.padding * 2
        height = int(game.size * cell_size * 1.5) + self.padding * 2

        self.canvas = tk.Canvas(self.root, width=width, height=height, bg="#f0f0f0")
        self.canvas.pack()

    def _cell_center(self, row: int, col: int) -> tuple[float, float]:
        """
        Translates from Board's row and columns to pixel coordinates for drawing.

        Args:
            row: The row index of the cell.
            col: The column index of the cell.


        Returns:
            A tuple (x, y) representing the pixel coordinates of the cell's center.
        """
        x = self.padding + col * self.cell_size * 1.5
        y = self.padding + row * self.cell_size * math.sqrt(3) / 2
        if row % 2 == 0:
            x += self.cell_size * 0.75
        return x, y

    def _hex_corners(self, row: int, col: int) -> list[tuple[float, float]]:
        """
        Calculates the pixel coordinates of the corners of a hexagon for a given cell.

        Args:
            row: The row index of the cell.
            col: The column index of the cell.

        Returns:
            A list of 6 (x, y) tuples representing the hexagon corners.
        """

        cx, cy = self._cell_center(row, col)
        corners = []

        for i in range(6):
            angle = math.radians(30 + i * 60)
            x = cx + self.cell_size * 0.5 * math.cos(angle)
            y = cy + self.cell_size * 0.5 * math.sin(angle)
            corners.append((x, y))

        return corners

    def draw_board(self) -> None:
        """
        Render the hexagonal grid and pieces on the canvas
        based on the current game state.
        """

        self.canvas.delete("all")

        for row in range(self.game.size):
            for col in range(self.game.size):
                cell = self.game.board.board[row][col]

                # Determine color
                if cell == 1:
                    color = "#ff4444"  # red for player 1

                elif cell == 2:
                    color = "#4444ff"  # blue for player 2

                else:
                    color = "#cccccc"  # grey for empty

                # Draw hexagon
                corners = self._hex_corners(row, col)
                self.canvas.create_polygon(
                    corners,
                    fill=color,
                    outline="#333333",
                    width=2,
                )

    def draw_status(self) -> None:
        """
        Displays the current game status (turn, winner) on the canvas.
        """

        status_text = ""
        if self.game.game_over:
            if self.game.winner == self.game.human_id:
                status_text = "You win! 🎉"
            else:
                status_text = "AI wins! 🤖"
        else:
            if self.game.is_human_turn():
                status_text = "Your turn (Red)"
            else:
                status_text = "AI's turn (Blue)"

        self.canvas.create_text(
            self.game.size * self.cell_size * 1.5 + self.padding,
            self.padding // 2,
            text=status_text,
            font=("Arial", 16, "bold"),
            fill="#333333",
        )
