# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2025/day/7

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2025
    _day = 7

    # @answer(1234)
    def part_1(self) -> int:
        grid, width, start_col, start_row = self._prepare_grid()
        splits = 0

        active: set[int] = {start_col}
        for row in range(start_row + 1, len(grid)):
            queue = list(active)
            processed: set[int] = set()
            carry_down: set[int] = set()

            while queue:
                col = queue.pop()
                if col in processed or not 0 <= col < width:
                    continue
                processed.add(col)

                if grid[row][col] == "^":
                    splits += 1
                    for next_col in (col - 1, col + 1):
                        if 0 <= next_col < width:
                            queue.append(next_col)
                else:
                    carry_down.add(col)

            active = carry_down
            if not active:
                break

        return splits

    # @answer(1234)
    def part_2(self) -> int:
        grid, width, start_col, start_row = self._prepare_grid()
        active: dict[int, int] = {start_col: 1}
        timelines = 0

        for row in range(start_row + 1, len(grid)):
            next_active: dict[int, int] = {}
            for col, count in active.items():
                if not 0 <= col < width:
                    timelines += count
                    continue

                if grid[row][col] == "^":
                    for next_col in (col - 1, col + 1):
                        if 0 <= next_col < width:
                            next_active[next_col] = next_active.get(next_col, 0) + count
                        else:
                            timelines += count
                else:
                    next_active[col] = next_active.get(col, 0) + count

            active = next_active
            if not active:
                break

        timelines += sum(active.values())  # whatever exits the bottom
        return timelines

    def _prepare_grid(self) -> tuple[list[str], int, int, int]:
        width = max(len(line) for line in self.input)
        padded = [line.ljust(width, ".") for line in self.input]

        start_row = next(i for i, line in enumerate(padded) if "S" in line)
        start_col = padded[start_row].index("S")

        return padded, width, start_col, start_row

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
