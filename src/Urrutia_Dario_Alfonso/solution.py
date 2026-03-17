from __future__ import annotations

import math

try:
    from board import HexBoard
except ImportError:
    from src.Urrutia_Dario_Alfonso.board import HexBoard


class MCTSNode:
    """
    A node in the MonteCarlo Tree Search algorithm
    """

    def __init__(
        self,
        board: HexBoard,
        move: tuple[int, int] | None = None,
        parent: MCTSNode | None = None,
    ):
        """
        Initializes a new MCTSNode.

        Args:
            board: The current state of the game board.
            move: The move that led to this node (row, col), or None for the root node.
            parent: The parent node in the search tree, or None for the root node.
        """
        self.board = board
        self.move = move
        self.parent = parent
        self.children: list[MCTSNode] = []
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self, untried_moves: list[tuple[int, int]]) -> bool:
        """
        Checks if the node is fully expanded.

        Args:
            untried_moves: The list of moves that have not been tried yet.

        Returns:
            True if the node is fully expanded, False otherwise.
        """
        return not untried_moves

    def best_child(self, c_param: float = math.sqrt(2)) -> MCTSNode:
        """
        Selects the best child node based on:
          the UCT (Upper Confidence Bound for Trees) formula.

        Args:
            c_param: The exploration parameter that balances
            exploration and exploitation.

        Returns:
            The child node with the highest UCT value.
        """

        return max(
            self.children,
            key=lambda child: (
                child.wins / child.visits
                + c_param * math.sqrt(math.log(self.visits) / child.visits)
            ),
        )
