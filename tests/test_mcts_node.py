from src.Urrutia_Dario_Alfonso.board import HexBoard
from src.Urrutia_Dario_Alfonso.solution import MCTSNode

# Test initialization


def test_mcts_node_initialization():
    """
    Tests that an MCTSNode is initialized correctly.
    """

    # Arrange

    board = HexBoard(size=5)
    root = MCTSNode(board=board)

    # Act + Assert
    assert root.board == board
    assert root.move is None
    assert root.parent is None
    assert root.children == []
    assert root.visits == 0
    assert root.wins == 0


# Test is_fully_expanded


def test_is_fully_expanded_when_no_moves_left():
    """
    Tests that is_fully_expanded returns True when there are no untried moves left.
    """

    # Arrange
    board = HexBoard(size=5)
    node = MCTSNode(board=board)
    untried_moves = []

    # Act + Assert
    assert node.is_fully_expanded(untried_moves)


def test_is_fully_expanded_when_moves_left():
    """
    Tests that is_fully_expanded returns False when there are untried moves left.
    """

    # Arrange
    board = HexBoard(size=5)
    node = MCTSNode(board=board)
    untried_moves = [(0, 0), (0, 1)]

    # Act + Assert
    assert not node.is_fully_expanded(untried_moves)


# Test best_child
def test_best_child_returns_child_with_highest_uct():
    """
    Tests that best_child returns the child with the highest UCT value.
    """

    # Arrange
    board = HexBoard(size=5)
    parent_node = MCTSNode(board=board)
    child1 = MCTSNode(board=board, parent=parent_node)
    child1.visits = 10
    child1.wins = 5
    child2 = MCTSNode(board=board, parent=parent_node)
    child2.visits = 20
    child2.wins = 15
    parent_node.children = [child1, child2]
    parent_node.visits = 30

    # Act
    best_child = parent_node.best_child(c_param=1.0)

    # Assert
    assert best_child == child2
