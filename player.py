from abc import ABC
from itertools import product
from random import choice
from time import sleep
from typing import Dict, Iterator, List, Type

from board import Board
from gametree import GameTree


class Player(ABC):

    SUBCLASSES: Dict[str, Type['Player']]

    _is_first: bool

    @property
    def is_first(self) -> bool:
        return self._is_first

    @is_first.setter
    def is_first(self, value: bool):
        self._is_first = value


class HumanPlayer(Player):

    def __repr__(self) -> str:
        return (
            f"HumanPlayer<is_first: {self._is_first}>"
        )

    def make_move(self, board: Board) -> Board:
        for board_line, grid_line in zip(
            str(board).split("\n"), board.index_grid().split("\n")
        ):
            print(f"{board_line}        {grid_line}")
        token = Board.token(self._is_first)
        while True:
            try:
                index = int(input(f"{token} [0-8]> "))
                return board.place_move(self.is_first, index)
            except ValueError:
                print("Please enter a number between 0 and 8!")
            except KeyError:
                print("This cell is already occupied!")


class ComputerPlayer(Player):

    DIFFICULTIES: List[str] = [
        "Very Easy", "Easy", "Somewhat easy", "Impossible"
    ]

    PLAYER_CHOICE_AMOUNTS: List[List[int]] = [
        [9, 7, 5, 3], [8, 6, 4, 2]
    ]

    WAIT_TIME: float = 0.7

    _gametree: GameTree = GameTree().new()

    _difficulty: int
    _deterministic: bool
    _strategy: 'Strategy'
    _wait: bool

    def __init__(
        self, deterministic: bool = False,
        strategy: 'Strategy' = None, wait: bool = True
    ):
        self._difficulty = None
        self._deterministic = deterministic
        self._strategy = strategy
        self._wait = wait

    def __repr__(self) -> str:
        return (
            f"HumanPlayer<is_first: {self._is_first}, "
            f"search_depth: {self._difficulty}, "
            f"deterministic: {self._deterministic}, "
            f"strategy: {self._strategy}>"
        )

    def set_difficulty(self, value: int):
        self._difficulty = value

    def _take_best_move_criterion(self, board: Board) -> bool:
        return (
            (Board.SIZE - board.free_cell_amount) // 2
            - self._difficulty <= 0
        )

    def make_move(self, board: Board) -> Board:
        if self._wait:
            sleep(self.WAIT_TIME)
        if self._take_best_move_criterion(board):
            index = self._best_move_index(board)
        else:
            index = self._any_move_index(board)
        return board.place_move(self._is_first, index)

    def _any_move_index(self, board: Board) -> Board:
        if self._deterministic:
            return board.free_cell_by_index(
                self._strategy.next_choice(board)
            )
        else:
            return choice(board.free_cell_indices())

    def _best_move_index(self, board: Board) -> Board:
        best_indices = self._gametree.best_moves(board, self._is_first)
        if self._deterministic:
            return best_indices[
                self._strategy.next_choice(board) % len(best_indices)
            ]
        else:
            return choice(best_indices)


class Strategy:

    @classmethod
    def all_player_strategies(cls, is_first: bool) -> Iterator['Strategy']:
        player_index = 0 if is_first else 1
        for choices in product(
            *(
                range(f) for f
                in ComputerPlayer.PLAYER_CHOICE_AMOUNTS[player_index]
            )
        ):
            yield cls([*choices])

    _choices: List[int]

    def __init__(self, choices: List[int]):
        self._choices = choices

    def next_choice(self, board: Board) -> int:
        if board.free_cell_amount == 1:
            return 0
        choice_index = len(self._choices) - board.free_cell_amount // 2
        return self._choices[choice_index]

    def __repr__(self) -> str:
        return f"Strategy<choices: {self._choices}>"

    def __str__(self) -> str:
        return str(self._choices)


Player.SUBCLASSES = {
    'Human': HumanPlayer,
    'Computer': ComputerPlayer
}
