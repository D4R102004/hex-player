from __future__ import annotations

from abc import ABC, abstractmethod


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
