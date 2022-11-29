"""The main logic of a choice algorythm."""
from typing import Tuple

from choice_queue import Queue


class Asker:
    """Class that provides ask and answer methods
    depends on your choices list."""

    def __init__(self, choices):
        self.q = Queue(choices)
        self.rating = []

    def is_ended(self):
        return self.q.size == 1

    def ask(self) -> tuple:
        """Gives you two variants to choose."""
        if not self.is_ended():
            first_variant = self.q.queue[self.q.tail - 1]
            second_variant = self.q.queue[self.q.tail - 2]
            return first_variant, second_variant
        if len(self.rating) < self.q.max_n:
            self.rating.append(self.q.queue[self.q.head])
            return self.rating
        # raise IndexError('Nothing to choose')

    def answer(self, choice: str) -> None:
        """Here you can make another choice."""
        if self.is_ended():
            raise IndexError('Nothing to choose')
        first_variant, second_variant = self.ask()
        if choice not in (first_variant, second_variant):
            raise ValueError('Answer is incorrect')
        self.q.pop()
        self.q.pop()
        winner = first_variant if choice == first_variant else second_variant
        loser = first_variant if choice != first_variant else second_variant
        self.q.push(winner)
        self.rating.append(loser)

    def get_progress(self) -> Tuple[int, int]:
        """Returns current progress and maximum number of choices."""
        return abs(self.q.size - self.q.max_n) + 1, self.q.max_n - 1

    def __str__(self):
        return self.q.__str__()


if __name__ == '__main__':
    """Quick example."""
    sample = ('1 + 1, Джентльмены, Волк с Уолл-стрит, Гнев человеческий, '
              'Брат, Аватар, Начало, Побег из Шоушенка')
    sample = '1, 2, 3'
    sample = sample.split(',')
    sample = list(map(str.strip, sample))  # Remove leading whitespaces
    sample = list(set(sample))  # Remove repeats and shuffle choices

    a = Asker(sample)
    print(a)

    while True:
        if not a.is_ended():
            aa, b = a.ask()
            print(aa, b)
            progress, maximum = a.get_progress()
            print(f'Progress is {progress}/{maximum}')
            user_choice = input()
            try:
                a.answer(user_choice)
            except Exception as e:
                print(e)
        # except IndexError as e:
        else:
            print()
            print('Result:')
            print(a.ask()[::-1])
            break
