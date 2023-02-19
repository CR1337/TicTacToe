from abc import ABC, abstractmethod
from typing import List, Type

from board import Board
from game import Game
from player import ComputerPlayer, Player


class Ui(ABC):

    @abstractmethod
    def print_board(self, board: Board):
        raise NotImplementedError()

    @abstractmethod
    def print_term(self, first_players_term: bool):
        raise NotImplementedError()

    @abstractmethod
    def print_empty_line(self):
        raise NotImplementedError()

    def _print_winner(self, winner: str):
        message = "Tie!" if winner == Board.TIE else f"{winner} wins!"
        print(message)

    def _ask_int(self, prompt: str, minimum: int, maximum: int) -> int:
        while True:
            try:
                number = int(input(prompt))
                if number < minimum or number > maximum:
                    raise ValueError()
                return number
            except ValueError:
                print(
                    f"Please enter a number between {minimum} and {maximum}!"
                )

    def _difficulty_menu(self) -> int:
        print("Please select a difficulty for this computer player:")
        print()
        for idx, string in enumerate(ComputerPlayer.DIFFICULTIES):
            print(f"[{idx}] {string}")
        print()
        maximum = len(ComputerPlayer.DIFFICULTIES) - 1
        difficulty = self._ask_int(f"[0-{maximum}]> ", 0, maximum)
        print()
        return difficulty

    def _player_type_menu(self, is_first: bool) -> Type[Player]:
        number_word = "first" if is_first else "second"
        token = Board.token(is_first)
        print(f"What kind of player is the {number_word} player ({token})?")
        print()
        for idx, string in enumerate(Player.SUBCLASSES):
            print(f"[{idx}] {string}")
        print()
        selection = self._ask_int("[0-1]> ", 0, 1)
        player_type = list(Player.SUBCLASSES.values())[selection]
        print()
        return player_type

    def _players_menu(self) -> List[Player]:
        players = []
        for is_first in [True, False]:
            player_type = self._player_type_menu(is_first)
            player = player_type()
            if player_type == ComputerPlayer:
                difficulty = self._difficulty_menu()
                player.set_difficulty(difficulty)
            players.append(player)
        return players

    def _play_again_menu(self) -> int:
        print("What do you want to do now?")
        print()
        print("[0] Play again with the same players")
        print("[1] Play again with other players")
        print("[2] Exit the game")
        print()
        next_action = self._ask_int("[0-2]> ", 0, 2)
        print()
        return next_action

    def _mainloop(self):
        players = self._players_menu()
        while True:
            game = Game(*players, self)
            winner = game.run()
            self._print_winner(winner)
            print()
            next_action = self._play_again_menu()
            if next_action == 0:
                continue
            elif next_action == 1:
                players = self._players_menu()
            elif next_action == 2:
                break

    def _greeting(self):
        print("Welcome to Tic-Tac-Toe!")
        print()

    def _goodbye(self):
        print("Bye.")
        print()

    def run(self):
        self._greeting()
        self._mainloop()
        self._goodbye()


class TerminalUi(Ui):

    def print_board(self, board: Board):
        print(board)

    def print_term(self, first_players_term: bool):
        token = Board.token(first_players_term)
        print(f"It's {token}s term:")

    def print_empty_line(self):
        print()


class DummyUi(Ui):

    def print_board(self, _: Board):
        pass

    def print_term(self, _: bool):
        pass

    def print_empty_line(self):
        pass
