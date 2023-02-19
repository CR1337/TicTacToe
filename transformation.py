from typing import List

from board import Board


class Transformation:

    SYMMETRIES: List[List[int]] = [
        [
            0, 1, 2,
            3, 4, 5,
            6, 7, 8
        ],  # e
        [
            2, 5, 8,
            1, 4, 7,
            0, 3, 6
        ],  # r¹
        [
            8, 7, 6,
            5, 4, 3,
            2, 1, 0
        ],  # r²
        [
            6, 3, 0,
            7, 4, 1,
            8, 5, 2
        ],  # r³
        [
            2, 1, 0,
            5, 4, 3,
            8, 7, 6
        ],  # f
        [
            8, 5, 2,
            7, 4, 1,
            6, 3, 0
        ],  # rf
        [
            6, 7, 8,
            3, 4, 5,
            0, 1, 2
        ],  # r²f
        [
            0, 3, 6,
            1, 4, 7,
            2, 5, 8
        ],  # r³f
    ]

    @classmethod
    def all(cls) -> List['Transformation']:
        return [cls(idx) for idx in range(len(cls.SYMMETRIES))]

    ALL: List['Transformation']

    @classmethod
    def between(cls, source: Board, destination: Board) -> 'Transformation':
        for transformation in cls.ALL:
            if source.simple_equal(transformation.apply_to(destination)):
                return transformation
        return None

    _symmetry: List[int]

    def __init__(self, index: str):
        self._symmetry = self.SYMMETRIES[index]

    def apply_to(self, x: Board | int) -> Board | int:
        if isinstance(x, int):
            return self._apply_to_index(x)
        else:
            return self._apply_to_board(x)

    def _apply_to_index(self, x: int) -> int:
        return self._symmetry[x]

    def _apply_to_board(self, x: Board) -> Board:
        new_board = Board()
        for idx in range(Board.SIZE):
            new_board[idx] = x[self._symmetry[idx]]
        return new_board


Transformation.ALL = Transformation.all()
