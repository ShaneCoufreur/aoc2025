# Generated using @xavdid's AoC Python Template: https://github.com/xavdid/advent-of-code-python-template

# puzzle prompt: https://adventofcode.com/2025/day/9

from ...base import StrSplitSolution, answer


class Solution(StrSplitSolution):
    _year = 2025
    _day = 9

    # @answer(1234)
    def part_1(self) -> int:
        points = self._parse_points()
        max_area = 0

        for i in range(len(points)):
            x1, y1 = points[i]
            for j in range(i + 1, len(points)):
                x2, y2 = points[j]
                area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)
                if area > max_area:
                    max_area = area

        return max_area

    # @answer(1234)
    def part_2(self) -> int:
        points = self._parse_points()
        bands = self._build_scanline_bands(points)

        max_area = 0
        for i in range(len(points)):
            x1, y1 = points[i]
            for j in range(i + 1, len(points)):
                x2, y2 = points[j]
                x_lo, x_hi = sorted((x1, x2))
                y_lo, y_hi = sorted((y1, y2))
                potential = (x_hi - x_lo + 1) * (y_hi - y_lo + 1)
                if potential <= max_area:
                    continue

                if self._rectangle_inside(bands, x_lo, x_hi, y_lo, y_hi):
                    max_area = potential

        return max_area

    def _parse_points(self) -> list[tuple[int, int]]:
        points: list[tuple[int, int]] = []
        for line in self.input:
            if not line:
                continue
            x_str, y_str = line.split(",")
            points.append((int(x_str), int(y_str)))
        return points

    def _build_scanline_bands(
        self, points: list[tuple[int, int]]
    ) -> list[tuple[int, int, list[tuple[int, int]]]]:
        """
        Precompute inside intervals for each horizontal band of rows between unique y-values.
        A band is represented by (y_start, y_end, intervals), where intervals are inclusive
        x ranges that are inside the polygon on any row in that band.
        """
        # construct vertical edges from the closed loop of points
        vertical_edges: list[tuple[int, int, int]] = []  # (x, y_min, y_max)
        horizontal_edges: list[tuple[int, int, int]] = []  # (x_min, x_max, y)
        for i in range(len(points)):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % len(points)]
            if x1 == x2:  # vertical edge
                if y1 < y2:
                    vertical_edges.append((x1, y1, y2))
                else:
                    vertical_edges.append((x1, y2, y1))
            else:
                if x1 < x2:
                    horizontal_edges.append((x1, x2, y1))
                else:
                    horizontal_edges.append((x2, x1, y1))

        ys = sorted({y for _, y in points})
        if not ys:
            return []

        bands: list[tuple[int, int, list[tuple[int, int]]]] = []
        for idx in range(len(ys)):
            y_val = ys[idx]
            intervals_at_y = self._row_intervals(vertical_edges, horizontal_edges, y_val)
            bands.append((y_val, y_val, intervals_at_y))

            if idx + 1 < len(ys):
                next_y = ys[idx + 1]
                if next_y > y_val + 1:
                    inner_start = y_val + 1
                    inner_end = next_y - 1
                    intervals_inner = self._row_intervals(vertical_edges, horizontal_edges, inner_start)
                    bands.append((inner_start, inner_end, intervals_inner))

        return bands

    def _row_intervals(
        self,
        vertical_edges: list[tuple[int, int, int]],
        horizontal_edges: list[tuple[int, int, int]],
        row: int,
    ) -> list[tuple[int, int]]:
        """
        Compute inclusive x-intervals that are inside the polygon on a specific row
        using the even-odd rule with vertical edges.
        """
        counts: dict[int, int] = {}
        for x, y_min, y_max in vertical_edges:
            if y_min <= row < y_max:
                counts[x] = counts.get(x, 0) + 1
        crossings = sorted(x for x, cnt in counts.items() if cnt % 2 == 1)
        if len(crossings) % 2 != 0:
            return []

        intervals: list[tuple[int, int]] = []
        for i in range(0, len(crossings), 2):
            left = crossings[i]
            right = crossings[i + 1]
            intervals.append((left, right))

        for x_min, x_max, y in horizontal_edges:
            if y == row:
                intervals.append((x_min, x_max))

        if not intervals:
            return []

        intervals.sort()
        merged: list[tuple[int, int]] = []
        cur_start, cur_end = intervals[0]
        for start, end in intervals[1:]:
            if start <= cur_end:
                cur_end = max(cur_end, end)
            else:
                merged.append((cur_start, cur_end))
                cur_start, cur_end = start, end
        merged.append((cur_start, cur_end))
        return merged

    @staticmethod
    def _rectangle_inside(
        bands: list[tuple[int, int, list[tuple[int, int]]]],
        x_lo: int,
        x_hi: int,
        y_lo: int,
        y_hi: int,
    ) -> bool:
        """
        Check whether the inclusive rectangle [x_lo, x_hi] x [y_lo, y_hi] lies entirely
        within the precomputed inside intervals.
        """
        for y_start, y_end, intervals in bands:
            if y_end < y_lo or y_start > y_hi:
                continue
            # rectangle overlaps this band
            if not intervals:
                return False
            covered = False
            for left, right in intervals:
                if left <= x_lo and x_hi <= right:
                    covered = True
                    break
            if not covered:
                return False
        return True

    # @answer((1234, 4567))
    # def solve(self) -> tuple[int, int]:
    #     pass
