from __future__ import annotations

import math
import random
import time

try:
    from board import HexBoard
    from player import Player
except ImportError:
    from src.Urrutia_Dario_Alfonso.board import HexBoard
    from src.Urrutia_Dario_Alfonso.player import Player


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


class SmartPlayer(Player):
    """
    A Player that will play using MCTS
    """

    def play(self, board: HexBoard) -> tuple[int, int]:
        """
        Decides the best move using MCTS.

        Args:
            board: The current game board state.

        Returns:
            A tuple (row, col) representing the chosen move.
        """

        root = MCTSNode(board=board.clone())
        start_time = time.time()
        while time.time() - start_time < 4.5:
            node = self._select(root)

            untried_moves = self._get_untried_moves(node.board)
            if untried_moves:
                node = self._expand(node)

            result = self._simulate(node.board)
            self._backpropagate(node, result)

        if not root.children:
            return self._get_untried_moves(board)[0]

        return max(root.children, key=lambda child: child.visits).move

    def _select(self, node: MCTSNode) -> MCTSNode:
        """
        Selects a node to expand, by walking down the tree
        until it finds a node that is not fully expanded.

        Args:
            node: The current node in the search tree.

        Returns:
            The selected node for expansion.
        """
        untried_moves = self._get_untried_moves(node.board)

        while node.children and node.is_fully_expanded(untried_moves):
            node = node.best_child()
            untried_moves = self._get_untried_moves(node.board)
        return node

    def _expand(self, node: MCTSNode) -> MCTSNode:
        """
        Expands a node by adding a new child node for an untried move.
        Pick one untried move, create a new child node with that move,
          add it to the parent's children list, return the new child.

        Args:
            node: The node to expand.

        Returns:
            the new child node created from the expansion.
        """

        untried_moves = self._get_untried_moves(node.board)

        if not untried_moves:
            raise ValueError("No moves left to expand")

        move = random.choice(untried_moves)  # Just pick a random untried move
        new_board = node.board.clone()
        new_board.place_piece(
            row=move[0], col=move[1], player_id=self._current_player(new_board)
        )

        child_node = MCTSNode(board=new_board, move=move, parent=node)
        node.children.append(child_node)
        return child_node

    def _get_untried_moves(self, board: HexBoard) -> list[tuple[int, int]]:
        """
        Returns a list of untried moves for the given board state.

        Args:
            board: The current game board state.

        Returns:
            A list of tuples (row, col) representing the untried moves.
        """
        return [
            (row, col)
            for row in range(board.size)
            for col in range(board.size)
            if board.board[row][col] == 0
        ]

    def _current_player(self, board: HexBoard) -> int:
        """
        Determines whose turn is it given the board\

        Assumes that player 1 starts first and players alternate turns.

        Args:
            board: The current game board state.

        Returns:
            The player ID (1 or 2) of the current player.
        """
        occupied_cells = sum(cell != 0 for row in board.board for cell in row)

        # Player 1 starts first, so odd count means player 1's turn,
        # even means player 2's turn

        return occupied_cells % 2 + 1

    def _simulate(self, board: HexBoard) -> int:
        """
        From a given board state, play random moves alternating
        between players until someone wins.
        Return 1 if our player won, 0 if we lost.

        Args:
            board: The current game board state.

        Returns:
            1 if the player won, 0 if the player lost.
        """
        sim_board = board.clone()

        current_player = self._current_player(sim_board)

        empty = self._get_untried_moves(sim_board)
        random.shuffle(empty)

        for move in empty:
            sim_board.place_piece(row=move[0], col=move[1], player_id=current_player)
            current_player = 3 - current_player  # Switch player (1 <-> 2)

        return 1 if sim_board.check_connection(self.player_id) else 0

    def _backpropagate(self, node: MCTSNode, result: int) -> None:
        """
        Backpropagates the result of a simulation up the tree, updating
        the visit and win counts for each node along the path.

        Args:
            node: The node from which to start backpropagation.
            result: The result of the simulation (1 for win, 0 for loss).
        """
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent
