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
