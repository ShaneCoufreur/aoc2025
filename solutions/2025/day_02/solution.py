# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2025/day/2

import re

from ...base import TextSolution


class Solution(TextSolution):
    _year = 2025
    _day = 2

    # @answer(1234)
    def part_1(self) -> int:
        ranges = self.input.split(",")
        invalid_ids = 0
        invalid_id_sum = 0
        for r in ranges:
            low, high = map(int, r.split("-"))
            # print(low,high)
            for i in range(low, high + 1):
                s = str(i)
                firstpart, secondpart = s[: len(s) // 2], s[len(s) // 2 :]
                if firstpart == secondpart:
                    invalid_ids += 1
                    invalid_id_sum += i
        return invalid_id_sum

    # @answer(1234)
    def part_2(self) -> int:
        ranges = self.input.split(",")
        invalid_ids = 0
        invalid_id_sum = 0
        for r in ranges:
            low, high = map(int, r.split("-"))
            # print(low,high)
            for i in range(low, high + 1):
                s = str(i)
                if self.is_invalid_id_regex(s):
                    invalid_ids += 1
                    invalid_id_sum += i
        return invalid_id_sum

    def is_invalid_id_regex(self, s):
        return bool(re.fullmatch(r"(\d+)\1+", s))

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
