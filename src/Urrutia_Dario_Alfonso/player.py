from __future__ import annotations

from abc import ABC, abstractmethod

try:
    from board import HexBoard
except ImportError:
    from src.Urrutia_Dario_Alfonso.board import HexBoard


class Player(ABC):
    """
    Abstract base class for a player in the Hex game
    """

    def __init__(self, player_id: int):
        """
        Initializes a player with a given ID

        Args:
            player_id (int): The ID of the player (1 or 2)
        """
        self.player_id = player_id

    @abstractmethod
    def play(self, board: HexBoard) -> tuple[int, int]:
        """
        Abstract method to make a move on the board.

        Args:
            board: The current game board state.

        Returns:
            A tuple (row, col) representing the chosen move.
        """
        raise NotImplementedError("Subclasses must implement play()")
