# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2025/day/8

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2025
    _day = 8

    # @answer(1234)
    def part_1(self) -> int:
        points = self._parse_points()
        edge_limit = 10 if self.use_test_data else 1000

        edges = self._sorted_edges(points)
        uf = _UnionFind(len(points))

        for _, i, j in edges[:edge_limit]:
            uf.union(i, j)

        sizes = sorted(uf.component_sizes(), reverse=True)
        product = 1
        for size in sizes[:3]:
            product *= size
        return product

    # @answer(1234)
    def part_2(self) -> int:
        points = self._parse_points()
        edges = self._sorted_edges(points)
        uf = _UnionFind(len(points))

        last_i = last_j = -1
        for _, i, j in edges:
            merged = uf.union(i, j)
            if merged and uf.component_count == 1:
                last_i, last_j = i, j
                break

        if last_i == -1 or last_j == -1:
            raise ValueError("Failed to connect all junction boxes")

        return points[last_i][0] * points[last_j][0]

    def _parse_points(self) -> list[tuple[int, int, int]]:
        points: list[tuple[int, int, int]] = []
        for line in self.input:
            if not line:
                continue
            x, y, z = map(int, line.split(","))
            points.append((x, y, z))
        return points

    @staticmethod
    def _sorted_edges(points: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]:
        edges: list[tuple[int, int, int]] = []  # (dist2, i, j)
        for i in range(len(points)):
            x1, y1, z1 = points[i]
            for j in range(i + 1, len(points)):
                x2, y2, z2 = points[j]
                dx, dy, dz = x1 - x2, y1 - y2, z1 - z2
                dist2 = dx * dx + dy * dy + dz * dz
                edges.append((dist2, i, j))

        edges.sort(key=lambda e: (e[0], e[1], e[2]))
        return edges

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass


class _UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n
        self.component_count = n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        self.component_count -= 1
        return True

    def component_sizes(self) -> list[int]:
        return [self.size[i] for i in range(len(self.parent)) if self.parent[i] == i]
