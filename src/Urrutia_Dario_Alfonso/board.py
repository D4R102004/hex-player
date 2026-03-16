from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque


class AbstractBoard(ABC):
    """Defines the interface that any game board must implement."""

    @abstractmethod
    def clone(self) -> AbstractBoard:
        """
        Creates and returns a deep copy of the board.

        Returns:
            A new AbstractBoard instance with identical state to this one.
        """

    @abstractmethod
    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        """
        Places a piece for the specified player at the given location.

        Args:
            row: The row index where the piece is to be placed.
            col: The column index where the piece is to be placed.
            player_id: The identifier for the player (1 or 2).

        Returns:
            True if the piece was placed successfully, False if the cell
            was already occupied.
        """

    @abstractmethod
    def check_connection(self, player_id: int) -> bool:
        """
        Checks if the specified player has formed a winning connection.

        Args:
            player_id: The identifier for the player (1 or 2).

        Returns:
            True if the player has connected their two sides, False otherwise.
        """


class HexBoard(AbstractBoard):
    """
    Represents the NxN game board for a HEX match.

    The board is modeled as a 2D matrix where:
        - 0 = empty cell
        - 1 = Player 1 piece
        - 2 = Player 2 piece

    Attributes:
        size: The dimension N of the NxN board.
        board: The NxN matrix representing current game state.
    """

    def __init__(self, size: int) -> None:
        """
        Initializes an empty NxN HexBoard.

        Args:
            size: The dimension N of the board (creates an NxN grid).
        """
        self.size = size
        self.board = [[0 for _ in range(size)] for _ in range(size)]

    def clone(self) -> HexBoard:
        """
        Creates and returns a deep copy of this board.

        Returns:
            A new HexBoard instance with identical state to this one.
        """
        new_board = HexBoard(self.size)
        new_board.board = [row[:] for row in self.board]
        return new_board

    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        """
        Places a piece for the specified player at the given location if it's empty.

          Args:
              row: The row index where the piece is to be placed.
              col: The column index where the piece is to be placed.
              player_id: The identifier for the player (1 or 2).

          Returns:
              True if the piece was placed successfully, False if the cell
              was already occupied.
        """
        if self.board[row][col] == 0:
            self.board[row][col] = player_id
            return True
        return False

    def _get_neighbors(self, row: int, col: int) -> list[tuple[int, int]]:
        """
        Returns the list of valid neighboring cell coordinates for a given cell.

        Args:
            row: The row index of the cell.
            col: The column index of the cell.

        Returns:
            A list of tuples, where each tuple contains the row and column indices
            of a neighboring cell.
        """
        neighbors = []

        if row % 2 == 0:
            directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 0), (0, -1)]
        else:
            directions = [(0, -1), (-1, 0), (0, 1), (1, 1), (1, 0), (1, -1)]

        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < self.size and 0 <= new_col < self.size:
                neighbors.append((new_row, new_col))

        return neighbors

    def check_connection(self, player_id: int) -> bool:
        """
        Checks if the specified player has formed a winning connection.

        Args:
            player_id: The identifier for the player (1 or 2).

        Returns:
            True if the player has connected their two sides, False otherwise.
        """

        initial_cells = (
            [(row, 0) for row in range(self.size) if self.board[row][0] == player_id]
            if player_id == 1
            else [
                (0, col) for col in range(self.size) if self.board[0][col] == player_id
            ]
        )

        queue = deque(initial_cells)
        visited = set(initial_cells)

        while queue:
            row, col = queue.popleft()

            if (player_id == 1 and col == self.size - 1) or (
                player_id == 2 and row == self.size - 1
            ):
                return True

            for neighbor in self._get_neighbors(row, col):
                neighbor_row, neighbor_col = neighbor
                if (
                    neighbor not in visited
                    and self.board[neighbor_row][neighbor_col] == player_id
                ):
                    visited.add(neighbor)
                    queue.append(neighbor)

        return False
