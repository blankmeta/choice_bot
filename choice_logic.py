"""The main logic of a choice algorythm."""
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
        self.rating.append(self.q.queue[self.q.head])
        raise IndexError('Nothing to choose')

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

    def __str__(self):
        return self.q.__str__()


if __name__ == '__main__':
    """Quick example."""
    sample = ('1 + 1, Джентльмены, Волк с Уолл-стрит, Гнев человеческий, '
              'Брат, Аватар, Начало, Побег из Шоушенка')
    sample = sample.split(',')
    sample = list(map(str.strip, sample))  # Remove leading whitespaces
    sample = list(set(sample))  # Remove repeats and shuffle choices

    a = Asker(sample)
    print(a)

    while True:
        try:
            print(a.ask())
            user_choice = input()
            try:
                a.answer(user_choice)
            except Exception as e:
                print(e)
        except IndexError as e:
            print()
            print('Result:')
            print(a.rating[::-1])
            break
