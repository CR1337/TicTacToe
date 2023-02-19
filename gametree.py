import pickle
from dataclasses import dataclass
from typing import Dict, List

from board import Board
from transformation import Transformation


@dataclass
class Transition:

    index: int
    node: 'GameTreeNode'

    def __repr__(self) -> str:
        return (
            "Transition:\n"
            f"index: {self.index}\n"
            f"{repr(self.node)}"
        )


class GameTreeNode:

    _board: Board
    _children: List[Transition]
    _score: int
    _visited: bool

    def __init__(
        self, board: Board
    ):
        self._board = board
        self._children = []
        self._score = None
        self._visited = False

    def __repr__(self) -> str:
        return (
            "GameTreeNode\n"
            f"score: {self._score}\n"
            f"# children: {len(self._children)}\n"
            f"{repr(self._board)}"
        )

    def add_child(
        self, index: int, node: 'GameTreeNode'
    ) -> 'GameTreeNode':
        self._children.append(Transition(index, node))
        return node

    def determine_score(self, maximizing: bool) -> int:
        if self._score is not None:
            return self._score
        if self.is_terminal:
            self._score = self._board.score
        else:
            operator = max if maximizing else min
            self._score = operator(
                c.node.determine_score(not maximizing)
                for c in self._children
            )
        return self._score

    @property
    def children(self) -> List[Transition]:
        return self._children

    @property
    def is_terminal(self) -> bool:
        return self._board.winner() is not None

    @property
    def winner(self) -> str | None:
        return self._board.winner()

    @property
    def board(self) -> Board:
        return self._board

    @property
    def score(self) -> int:
        return self._score

    @property
    def visited(self) -> bool:
        return self._visited

    @visited.setter
    def visited(self, value):
        self._visited = value


class GameTree:

    PICKLE_FILENAME: str = "gametree.pickle"

    _root: GameTreeNode
    _found_nodes: Dict[Board, GameTreeNode]

    @classmethod
    def new(cls) -> 'GameTree':
        try:
            return cls.from_pickle()
        except FileNotFoundError:
            tree = cls()
            tree.construct()
            tree.to_pickle()
            return tree

    @classmethod
    def from_pickle(cls) -> 'GameTree':
        with open(cls.PICKLE_FILENAME, 'rb') as file:
            return pickle.load(file)

    def to_pickle(self):
        with open(self.PICKLE_FILENAME, 'wb') as file:
            pickle.dump(self, file)

    def construct(self):
        self._root = GameTreeNode(Board())
        self._found_nodes = {Board(): self._root}
        self._construct_recursive(self._root, True)
        self._root.determine_score(True)

    def _construct_recursive(self, node: GameTreeNode, maximizing: bool):
        if node.is_terminal or node.visited:
            return
        node.visited = True
        self._add_children(node, maximizing)
        for child in node.children:
            if not child.node.visited:
                self._construct_recursive(child.node, not maximizing)

    def _add_children(self, node: GameTreeNode, maximizing: bool):
        indexed_boards = (
            (idx, Board.from_board(node._board).place_move(maximizing, idx))
            for idx in node.board.free_cell_indices()
        )
        for index, board in indexed_boards:
            if board not in self._found_nodes:
                child = node.add_child(index, GameTreeNode(board))
                self._found_nodes[board] = child
            else:
                node.add_child(index, self._found_nodes[board])

    def _winning_move_criterion(self, maximizing: bool, score: int) -> bool:
        return (
            maximizing and score == Board.SCORES[Board.PLAYER_X]
            or not maximizing and score == Board.SCORES[Board.PLAYER_O]
        )

    def _tie_move_criterion(self, score: int) -> bool:
        return score == Board.SCORES[Board.TIE]

    def best_moves(self, board: Board, maximizing: bool) -> List[int]:
        found_node = self._found_nodes[board]
        best_transitions = [
            t for t in found_node.children
            if self._winning_move_criterion(maximizing, t.node.score)
        ]
        if not best_transitions:
            best_transitions = [
                t for t in found_node.children
                if self._tie_move_criterion(t.node.score)
            ]
        if not best_transitions:
            best_transitions = found_node.children[:]

        transformation = Transformation.between(found_node.board, board)
        return [transformation.apply_to(t.index) for t in best_transitions]
