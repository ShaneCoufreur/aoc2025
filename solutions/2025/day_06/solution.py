# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2025/day/6

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2025
    _day = 6

    # @answer(1234)
    def part_1(self) -> int:
        return sum(self._apply_operator(nums, op) for nums, op in self._parse_segments())

    # @answer(1234)
    def part_2(self) -> int:
        return sum(
            self._apply_operator(nums, op) for nums, op in self._parse_segments_vertical()
        )

    def _parse_segments(self) -> list[tuple[list[int], str]]:
        """
        Break the input into contiguous column ranges (one per problem) and extract the
        numbers and operator for each range.
        """
        number_rows, op_row, spans = self._prep_grid()

        parsed: list[tuple[list[int], str]] = []
        for start, end in spans:
            numbers = []
            for row in number_rows:
                chunk = row[start:end].strip()
                if chunk:
                    numbers.append(int(chunk))

            op = self._extract_operator(op_row, start, end)
            parsed.append((numbers, op))

        return parsed

    def _parse_segments_vertical(self) -> list[tuple[list[int], str]]:
        """
        Parse problems by reading each column as a number, ordered right-to-left.
        """
        number_rows, op_row, spans = self._prep_grid()

        parsed: list[tuple[list[int], str]] = []
        for start, end in spans:
            numbers: list[int] = []
            for col in range(end - 1, start - 1, -1):
                digits = [row[col] for row in number_rows if row[col].isdigit()]
                if digits:
                    numbers.append(int("".join(digits)))

            op = self._extract_operator(op_row, start, end)
            parsed.append((numbers, op))

        return parsed

    def _prep_grid(self) -> tuple[list[str], str, list[tuple[int, int]]]:
        """Pad lines to equal width and identify contiguous column spans for problems."""
        width = max(len(line) for line in self.input)
        padded = [line.ljust(width) for line in self.input]
        number_rows = padded[:-1]
        op_row = padded[-1]

        sep_cols = [all(row[col] == " " for row in padded) for col in range(width)]
        spans: list[tuple[int, int]] = []
        in_segment = False
        start = 0

        for col in range(width + 1):  # +1 flushes the final segment
            is_separator = True if col == width else sep_cols[col]

            if not is_separator and not in_segment:
                start = col
                in_segment = True
                continue

            if is_separator and in_segment:
                spans.append((start, col))
                in_segment = False

        return number_rows, op_row, spans

    @staticmethod
    def _extract_operator(op_row: str, start: int, end: int) -> str:
        ops = [char for char in op_row[start:end] if char in {"+", "*"}]
        if len(ops) != 1:
            raise ValueError(f"Expected exactly one operator in columns [{start}, {end}), found {ops}")
        return ops[0]

    @staticmethod
    def _apply_operator(numbers: list[int], op: str) -> int:
        if op == "+":
            return sum(numbers)

        product = 1
        for num in numbers:
            product *= num
        return product

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
