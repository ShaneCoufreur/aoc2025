# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2025/day/1

from ...base import StrSplitSolution


class Solution(StrSplitSolution):
    _year = 2025
    _day = 1

    # @answer(1234)
    def part_1(self) -> int:
        position = 50
        zeros = 0

        for instruction in self.input:
            direction = instruction[0]
            steps = int(instruction[1:])

            position, _ = self._rotate(position, direction, steps)
            if position == 0:
                zeros += 1

        return zeros

    # @answer(1234)
    def part_2(self) -> int:
        position = 50
        zeros = 0

        for instruction in self.input:
            direction = instruction[0]
            steps = int(instruction[1:])

            position, hits = self._rotate(position, direction, steps)
            zeros += hits

        return zeros

    def _rotate(self, start: int, direction: str, steps: int) -> tuple[int, int]:
        """
        Returns the new position and how many times 0 is seen during the rotation.
        """
        if direction == "L":
            zero_hits = self._count_zero_hits(start, steps, go_left=True)
            return (start - steps) % 100, zero_hits

        zero_hits = self._count_zero_hits(start, steps, go_left=False)
        return (start + steps) % 100, zero_hits

    @staticmethod
    def _count_zero_hits(start: int, steps: int, go_left: bool) -> int:
        """
        Count the number of times a step lands on 0 while rotating `steps` clicks.
        """
        remainder = start if go_left else (100 - start) % 100

        if remainder == 0:
            return steps // 100

        if steps < remainder:
            return 0

        return 1 + (steps - remainder) // 100

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
