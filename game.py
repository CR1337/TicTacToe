from typing import List, Protocol

from board import Board
from player import Player


class UiProtocol(Protocol):

    def print_board(self, board: Board):
        pass


class Game:

    _players: List[Player]
    _current_player: Player
    _board: Board
    _ui = UiProtocol

    def __init__(
        self, first_player: Player, second_player: Player, ui: UiProtocol
    ):
        self._players = [first_player, second_player]
        self._players[0].is_first = True
        self._players[1].is_first = False
        self._current_player = self._players[0]
        self._board = Board()
        self._ui = ui

    def __repr__(self) -> str:
        return (
            "Game\n"
            f"players[0]: {repr(self._players[0])}\n"
            f"player[1]: {repr(self._players[1])}\n"
            f"current_player: {repr(self._current_player)}\n"
            f"{repr(self._board)}"
        )

    def _switch_current_player(self):
        self._current_player = self._players[
            1 - self._players.index(self._current_player)
        ]

    def run(self) -> str:
        return self._mainloop()

    def _mainloop(self) -> str:
        winner = None
        while not winner:
            self._ui.print_term(self._current_player.is_first)
            self._board = self._current_player.make_move(self._board)
            self._ui.print_board(self._board)
            self._ui.print_empty_line()
            self._switch_current_player()
            winner = self._board.winner()
        return winner
