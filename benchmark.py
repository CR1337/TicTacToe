from itertools import product
from multiprocessing import Pool, cpu_count
from typing import Iterator, List

from game import Game
from player import ComputerPlayer, Strategy
from ui import DummyUi


class Benchmark:

    CSV_SEP: str = ";"
    UI: DummyUi = DummyUi()

    def _run_game(
        self, first_player_strategy: Strategy,
        second_player_strategy: Strategy,
        first_player_difficulty: int, second_player_difficulty: int
    ) -> str:
        first_player = ComputerPlayer(True, first_player_strategy, False)
        first_player.set_difficulty(first_player_difficulty)
        second_player = ComputerPlayer(True, second_player_strategy, False)
        second_player.set_difficulty(second_player_difficulty)
        game = Game(first_player, second_player, self.UI)
        return game.run()

    def _generate_csv_content(self, results: Iterator[List[int | str]]) -> str:
        return "\n".join(
            f"{self.CSV_SEP}".join(
                str(r) for r in result
            )
            for result in results
        )

    def _result_generator(
        self, first_player_strategy: Strategy
    ) -> Iterator[List[int | str]]:
        for (
            second_player_strategy,
            first_player_difficulty,
            second_player_difficulty
        ) in product(
            Strategy.all_player_strategies(False),
            range(len(ComputerPlayer.DIFFICULTIES)),
            range(len(ComputerPlayer.DIFFICULTIES))
        ):
            yield [
                str(first_player_strategy),
                str(second_player_strategy),
                first_player_difficulty,
                second_player_difficulty,
                self._run_game(
                    first_player_strategy, second_player_strategy,
                    first_player_difficulty, second_player_difficulty
                )
            ]

    def _process_target(self, first_player_strategy: Strategy):
        return self._generate_csv_content(
            self._result_generator(first_player_strategy)
        )

    def run(self):
        with Pool(processes=cpu_count()) as pool:
            results = pool.map(
                self._process_target,
                Strategy.all_player_strategies(True)
            )
        with open("benchmark.csv", 'a') as file:
            for result in results:
                file.write(f"{result}\n")


if __name__ == "__main__":
    benchmark = Benchmark()
    benchmark.run()
