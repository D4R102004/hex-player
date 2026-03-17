from src.Urrutia_Dario_Alfonso.board import HexBoard

# Testing board_initialization


def test_board_initialization_empty():
    """
    Tests a Board is initialized empty
    """
    # Arrange + Act
    board = HexBoard(size=5)

    assert board.size == 5
    assert len(board.board) == 5
    assert all(cell == 0 for row in board.board for cell in row)


# Testing piece placement


def test_board_place_piece_on_empty_cell():
    """
    Tests placing pieces on the board.
    """
    # Arrange
    board = HexBoard(size=5)

    # Act + Assert
    assert board.place_piece(row=0, col=0, player_id=1)  # Place player 1's piece
    assert board.board[0][0] == 1


def test_board_place_piece_on_occupied_cell():
    """
    Tests that placing a piece on an occupied cell fails.
    """

    # Arrange
    board = HexBoard(size=5)

    # Act + Assert
    board.place_piece(row=0, col=0, player_id=1)  # Place player 1's piece

    assert not board.place_piece(
        row=0, col=0, player_id=2
    )  # Attempt to place on occupied cell
    assert board.board[0][0] == 1  # Cell should remain unchanged


# Testing board cloning


def test_board_cloning_is_that_same():
    """
    Tests wether the board correctly clones itself, creating a new instance.
    """

    # Arrange
    board = HexBoard(size=5)
    board.place_piece(row=0, col=0, player_id=1)

    # Act
    new_board = board.clone()

    # Assert
    assert new_board is not board  # Ensure it's a different instance
    assert new_board.size == board.size  # Ensure size is the same
    assert new_board.board == board.board


def test_board_clone_is_independent():
    """
    Test that the cloned board is independent from the original
    """

    # Arrange

    board = HexBoard(size=5)
    board.place_piece(row=0, col=0, player_id=1)

    # Act

    new_board = board.clone()
    new_board.place_piece(row=1, col=1, player_id=2)

    # Assert
    assert board.board[1][1] == 0
    assert new_board.board[0][0] == board.board[0][0]


# Testing check_connection


def test_player_1_wins_left_right():
    """
    Tests that player 1 wins by connecting left to right
    """

    # Arrange
    board = HexBoard(size=3)
    board.place_piece(row=0, col=0, player_id=1)
    board.place_piece(row=0, col=1, player_id=1)
    board.place_piece(row=0, col=2, player_id=1)

    # Act + Assert
    assert board.check_connection(player_id=1)


def test_player_2_wins_top_bottom():
    """
    Tests that player 2 wins by connecting top to bottom
    """

    # Arrange
    board = HexBoard(size=3)
    board.place_piece(row=0, col=0, player_id=2)
    board.place_piece(row=1, col=0, player_id=2)
    board.place_piece(row=2, col=0, player_id=2)

    # Act + Assert
    assert board.check_connection(player_id=2)


def test_empty_board_no_winner():
    """
    Tests that an empty board has no winner
    """

    # Arrange
    board = HexBoard(size=3)

    # Act + Assert
    assert not board.check_connection(player_id=1)
    assert not board.check_connection(player_id=2)


def test_partial_board_has_no_winner():
    """
    Tests that a partially filled board with no winning connections has no winner
    """

    # Arrange
    board = HexBoard(size=3)
    board.place_piece(row=0, col=0, player_id=1)
    board.place_piece(row=1, col=1, player_id=1)
    board.place_piece(row=2, col=2, player_id=1)

    # Act + Assert
    assert not board.check_connection(player_id=1)
    assert not board.check_connection(player_id=2)
