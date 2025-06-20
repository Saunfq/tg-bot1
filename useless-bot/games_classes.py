from __future__ import annotations

from dataclasses import dataclass, field
from random import randint


@dataclass
class GuessGame:
    max_tries_to_guess: int = 5
    __status: str = field(init=False, default="не в игре")
    number_of_games: int = field(init=False, default=0)
    number_of_wins: int = field(init=False, default=0)
    cur_tries: int = field(init=False, default=0)

    def start_game(self) -> str:
        if self.__status == "не в игре":
            self.__status = "в игре"
            self.number_to_guess = randint(1, 100)
            self.cur_tries = 0
            return "Игра началась, удачи!"
        else:
            return "Вы уже и так в игре"

    def trie_to_guess(self, number: int) -> str:
        if self.__status == "не в игре":
            return "Вы не в игре"

        if number < 1 or number > 100:
            return "Число находиться в диапазоне от 1 до 100"

        self.cur_tries += 1

        if number == self.number_to_guess:
            self.number_of_games += 1
            self.number_of_wins += 1
            return "Поздравляем! Вы победили!"

        if self.cur_tries == self.max_tries_to_guess:
            self.cancell_game()
            self.number_of_games += 1
            return f"Вы исчерпали количество попыток угадать.\n Вы проиграли :( .\n Было загадано число  - {self.number_to_guess}\n Сыграем еще"

        if number > self.number_to_guess:
            bigger_smaller = "меньше"
        else:
            bigger_smaller = "больше"

        return f"Вы не угадали число, у вас осталось {self.max_tries_to_guess - self.cur_tries} попыток, загаданное число {bigger_smaller} введеного вами"

    def cancell_game(self) -> None:
        self.__status = "не в игре"

    def stats(self) -> str:
        return f"""Количество игр - {self.number_of_games}\nКоличество побед - {self.number_of_wins}"""
