from src.Urrutia_Dario_Alfonso.board import HexBoard
from src.Urrutia_Dario_Alfonso.solution import MCTSNode, SmartPlayer

# Testing _current_player


def test_current_player_returns_player1_on_empty_board():
    """
    Testing that on an empty board, we get player 1
    """

    # Arrange

    board = HexBoard(size=3)
    player = SmartPlayer(player_id=1)

    # Act + Assert

    assert player._current_player(board) == 1


def test_current_player_returns_player2_after_one_move():
    """
    Test that after one move,
    The player to move is player 2
    """

    # Arrange
    board = HexBoard(size=3)
    board.place_piece(row=0, col=0, player_id=1)
    player = SmartPlayer(player_id=1)

    # Act + Assert
    assert player._current_player(board) == 2


# Testing _get_untried_moves


def test_empty_board_returns_all_cells():
    """
    Tests wether an empty board
    returns all cells for a new move
    """

    board = HexBoard(size=3)
    player = SmartPlayer(player_id=1)

    moves = player._get_untried_moves(board)
    assert len(moves) == 9  # 3x3 grid returns 9 moves


def test_non_empty_board_returns_cells():
    """
    Tests wether a non empty board returns the correct untried moves
    """

    board = HexBoard(size=3)
    board.place_piece(row=0, col=0, player_id=1)
    board.place_piece(row=1, col=1, player_id=2)

    player = SmartPlayer(player_id=1)

    moves = player._get_untried_moves(board)
    assert len(moves) == 7  # 2 cells occupied, so 7 moves left
    assert (0, 0) not in moves  # Occupied cell should not be in moves
    assert (1, 1) not in moves


# Testing _backpropagate


def test_backpropagate_updates_visits_and_wins():
    """
    Tests that _backpropagate correctly
    updates the visits and wins of the nodes in the path.
    """

    # Arrange

    board = HexBoard(size=5)
    root = MCTSNode(board=board)
    child1 = MCTSNode(board=board, parent=root)
    child2 = MCTSNode(board=board, parent=child1)

    # Act
    player = SmartPlayer(player_id=1)
    player._backpropagate(child2, result=1)

    # Assert
    assert root.visits == 1
    assert root.wins == 1
    assert child1.visits == 1
    assert child1.wins == 1
    assert child2.visits == 1
    assert child2.wins == 1


# Testing Simulate


def test_simulate_returns_valid_result():
    """
    Tests that simulate returns either 0 or 1,
    and that it does not modify the original board.
    """

    board = HexBoard(size=3)
    player = SmartPlayer(player_id=2)

    board.place_piece(row=1, col=1, player_id=1)
    result = player._simulate(board)

    assert result in [0, 1]  # Result should be either 0 or 1
    assert board.board[1][1] == 1  # Original board unchanged
