from functools import reduce
from operator import add, xor
from typing import Dict, List


class Board:

    LINE_INDICES: List[List[int]] = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]

    WIDTH: int = 3
    SIZE: int = WIDTH ** 2
    PLAYER_X: str = 'X'
    PLAYER_O: str = 'O'
    EMPTY: str = ' '
    TIE: str = 'T'

    SCORES: Dict[str, int] = {
        TIE: 0,
        PLAYER_X: 1,
        PLAYER_O: -1,
    }

    _cells: List[str]

    @classmethod
    def from_board(cls, board: 'Board') -> 'Board':
        new_board = cls()
        new_board._cells = board._cells[:]
        return new_board

    @classmethod
    def token(cls, is_first: bool) -> str:
        return cls.PLAYER_X if is_first else cls.PLAYER_O

    def __init__(self):
        self._cells = [self.EMPTY] * self.SIZE

    def place_move(self, is_first: bool, index: str) -> 'Board':
        if self._cells[index] != self.EMPTY:
            raise KeyError(f"Cell {index} is occupied!")
        new_board = self.from_board(self)
        new_board._cells[index] = self.token(is_first)
        return new_board

    def winner(self) -> str | None:
        for indices in self.LINE_INDICES:
            line = (self._cells[indices[i]] for i in range(self.WIDTH))
            if len(set(line)) == 1 and self._cells[indices[0]] != self.EMPTY:
                return self._cells[indices[0]]
        return None if self.EMPTY in self._cells else self.TIE

    def free_cell_indices(self) -> List[int]:
        return [i for i, c in enumerate(self._cells) if c == self.EMPTY]

    @staticmethod
    def _fill_grid(cells: List[str]) -> str:
        return (
            "╔═══╦═══╦═══╗\n"
            f"║ {cells[0]} ║ {cells[1]} ║ {cells[2]} ║\n"
            "╠═══╬═══╬═══╣\n"
            f"║ {cells[3]} ║ {cells[4]} ║ {cells[5]} ║\n"
            "╠═══╬═══╬═══╣\n"
            f"║ {cells[6]} ║ {cells[7]} ║ {cells[8]} ║\n"
            "╚═══╩═══╩═══╝"
        )

    def __str__(self) -> str:
        return self._fill_grid(self._cells)

    def __repr__(self) -> str:
        return f"Board with id: {hex(id(self))}\n{str(self)}"

    @classmethod
    def index_grid(cls) -> str:
        return cls._fill_grid(list(range(cls.SIZE)))

    def __setitem__(self, index, value):
        self._cells[index] = value

    def __getitem__(self, index) -> str:
        return self._cells[index]

    def simple_hash(self) -> int:
        return hash(reduce(add, self._cells, ""))

    def __hash__(self) -> int:
        from transformation import Transformation
        boards = (t.apply_to(self) for t in Transformation.ALL)
        hashes = (b.simple_hash() for b in boards)
        return reduce(xor, hashes, 0)

    def simple_equal(self, other: 'Board') -> bool:
        return all(c1 == c2 for c1, c2 in zip(self._cells, other._cells))

    def __eq__(self, other: 'Board') -> bool:
        from transformation import Transformation
        boards = (t.apply_to(self) for t in Transformation.ALL)
        return any(b.simple_equal(other) for b in boards)

    @property
    def score(self) -> int:
        return self.SCORES[self.winner()]

    def free_cell_by_index(self, index: int) -> int:
        return self.free_cell_indices()[index]

    @property
    def free_cell_amount(self) -> int:
        return len(self.free_cell_indices())
