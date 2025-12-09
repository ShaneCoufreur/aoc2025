# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2025/day/3

from ...base import StrSplitSolution


class Solution(StrSplitSolution):
    _year = 2025
    _day = 3

    # @answer(1234)
    def part_1(self) -> int:
        total = 0
        for line in self.input:
            digits = [int(c) for c in line]
            n = len(digits)
            suffix_max = [0] * (n+1)
            suffix_max[n] = -1

            for i in range(n - 1, -1, -1):
                suffix_max[i] = max(digits[i], suffix_max[i + 1])
            best = -1
            for i in range(n - 1):
                ones = suffix_max[i + 1] 
                if ones == -1:
                    continue
                best = max(best, digits[i] * 10 + ones)
            total += best
        return total

    # @answer(1234)
    def part_2(self) -> int:
        total = 0
        for line in self.input:
            digits = [int(c) for c in line]
            n = len(digits)
            k = 12
            if n < k:
                return 0
            remove = n - k
            stack = []

            for d in digits:
                while remove > 0 and stack and stack[-1] < d:
                    stack.pop()
                    remove -= 1
                stack.append(d)
            if remove > 0:
                stack = stack[:-remove]

            total += int(''.join(map(str, stack)))
        
        return total

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
