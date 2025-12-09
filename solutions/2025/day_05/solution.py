# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2025/day/5

from bisect import bisect_right

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2025
    _day = 5

    # @answer(1234)
    def part_1(self) -> int:
        ranges, _ingredient_ids = self._parse_input()
        merged = self._merge_ranges(ranges)

        # binary search through the merged ranges for each ingredient id
        starts = [start for start, _ in merged]
        fresh = 0
        for ingredient_id in _ingredient_ids:
            idx = bisect_right(starts, ingredient_id) - 1
            if idx >= 0 and ingredient_id <= merged[idx][1]:
                fresh += 1

        return fresh

    # @answer(1234)
    def part_2(self) -> int:
        ranges, ingredient_ids = self._parse_input()
        merged = self._merge_ranges(ranges)

        # count how many unique ingredient ids are covered by the fresh ranges
        total_fresh_ids = sum(end - start + 1 for start, end in merged)
        return total_fresh_ids

    def _parse_input(self) -> tuple[list[tuple[int, int]], list[int]]:
        # split the input around the blank line separating ranges and ids
        try:
            blank = self.input.index("")
        except ValueError as exc:
            raise ValueError("Expected a blank line between ranges and ingredient ids") from exc

        ranges = [self._parse_range(line) for line in self.input[:blank]]
        ingredient_ids = [int(line) for line in self.input[blank + 1 :]]
        return ranges, ingredient_ids

    @staticmethod
    def _parse_range(line: str) -> tuple[int, int]:
        start, end = line.split("-")
        return int(start), int(end)

    @staticmethod
    def _merge_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
        # combine overlapping/adjacent ranges to speed up lookups
        merged: list[tuple[int, int]] = []
        for start, end in sorted(ranges):
            if not merged or start > merged[-1][1] + 1:
                merged.append((start, end))
            else:
                prev_start, prev_end = merged[-1]
                merged[-1] = (prev_start, max(prev_end, end))
        return merged

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
