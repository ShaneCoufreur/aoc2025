# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2025/day/4

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2025
    _day = 4

    # @answer(1234)
    def part_1(self) -> int:
        grid = [list(row) for row in self.input]
        rows, cols = len(grid), len(grid[0])

        def neighbor_count(r: int, c: int) -> int:
            return sum(
                1
                for dr, dc in (
                    (-1, -1),
                    (-1, 0),
                    (-1, 1),
                    (0, -1),
                    (0, 1),
                    (1, -1),
                    (1, 0),
                    (1, 1),
                )
                if 0 <= r + dr < rows
                and 0 <= c + dc < cols
                and grid[r + dr][c + dc] == "@"
            )

        accessible = 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != "@":
                    continue
                if neighbor_count(r, c) < 4:
                    accessible += 1

        return accessible

    # @answer(1234)
    def part_2(self) -> int:
        """
        After a forklift clears all currently-accessible rolls, new ones might
        become accessible. Simulate repeatedly removing rolls with < 4 adjacent
        rolls until no more can be taken and return the total removed.
        """

        grid = [list(row) for row in self.input]
        rows, cols = len(grid), len(grid[0])

        # precompute neighbor coordinates to avoid rebuilding them
        neighbors = [
            [list() for _ in range(cols)]
            for _ in range(rows)
        ]
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] != "@":
                    continue
                for dr, dc in (
                    (-1, -1),
                    (-1, 0),
                    (-1, 1),
                    (0, -1),
                    (0, 1),
                    (1, -1),
                    (1, 0),
                    (1, 1),
                ):
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
                        neighbors[r][c].append((nr, nc))

        # degree is the current adjacent-roll count for each position
        degree = [[0] * cols for _ in range(rows)]
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == "@":
                    degree[r][c] = len(neighbors[r][c])

        queue: list[tuple[int, int]] = [
            (r, c)
            for r in range(rows)
            for c in range(cols)
            if grid[r][c] == "@" and degree[r][c] < 4
        ]

        removed = 0
        while queue:
            r, c = queue.pop()
            if grid[r][c] != "@":
                continue

            grid[r][c] = "."
            removed += 1

            # losing this roll reduces the degree of its neighbors
            for nr, nc in neighbors[r][c]:
                if grid[nr][nc] != "@":
                    continue
                degree[nr][nc] -= 1
                if degree[nr][nc] == 3:
                    queue.append((nr, nc))

        return removed

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
