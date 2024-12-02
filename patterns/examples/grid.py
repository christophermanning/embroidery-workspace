import streamlit as st
import random
from collections import deque
from shapely.geometry import Point

from patterns import Pattern

import numpy as np


class Grid(Pattern):
    def options():
        return {
            "label": "Grid",
            "inputs": {
                "width": {
                    "function": st.slider,
                    "args": {
                        "label": "Width",
                        "min_value": 50,
                        "max_value": 1000,
                        "step": 10,
                        "value": 1000,
                    },
                },
                "height": {
                    "function": st.slider,
                    "args": {
                        "label": "Height",
                        "min_value": 50,
                        "max_value": 1000,
                        "step": 10,
                        "value": 1000,
                    },
                },
                "dimension": {
                    "function": st.slider,
                    "args": {
                        "label": "Dimension",
                        "min_value": 2,
                        "max_value": 50,
                        "step": 1,
                        "value": 10,
                    },
                },
                "path": {
                    "function": st.selectbox,
                    "args": {
                        "label": "Path",
                        "options": [
                            "Random",
                            "Horizontal",
                            "Spiral",
                            "Diagonal",
                            "DFS",
                            "BFS",
                        ],
                    },
                },
                "random_seed": {
                    "function": st.number_input,
                    "args": {
                        "label": "Random Seed",
                        "value": lambda: random.randint(0, 999_999_999),
                        "step": 1,
                    },
                },
                "debug": {
                    "function": st.checkbox,
                    "args": {"label": "Debug", "value": False},
                },
            },
        }

    def pattern(self, width, height, dimension, path, random_seed, debug):
        nx, ny = (dimension, dimension)
        np.random.seed(random_seed)
        random.seed(random_seed)

        x0 = self.canvas.margin
        x1 = self.canvas.margin + width - self.canvas.margin
        x, step = np.linspace(x0, x1, nx, True, True)
        self.log.append(f"_Stitch Distance_ `{round(step,2)}`")

        y0 = self.canvas.margin
        y1 = self.canvas.margin + height - self.canvas.margin
        y = np.linspace(y0, y1, ny)
        xv, yv = np.meshgrid(x, y)

        coords = np.vstack(list(zip(xv.ravel(), yv.ravel())))

        if path == "Random":
            np.random.shuffle(coords)
        elif path == "Horizontal":
            for i in range(1, dimension):
                if i % 2 != 0:
                    start = dimension * i
                    end = start + dimension
                    coords[start:end] = coords[start:end][::-1]
        elif path == "Spiral":
            tcoords = []

            xi = -1
            yi = 0
            direction = 1
            rows = dimension
            cols = dimension - 1
            for _ in range(dimension * dimension):
                for _ in range(0, rows):
                    xi += direction
                    tcoords.append(coords[yi * dimension + xi])
                rows -= 1

                for _ in range(0, cols):
                    yi += direction
                    tcoords.append(coords[yi * dimension + xi])
                cols -= 1

                direction *= -1

            coords = tcoords
        elif path == "Diagonal":
            tcoords = []

            for k in range(0, dimension * 2):
                tmp = []

                for j in range(0, k):
                    i = k - j
                    if i < dimension and j < dimension:
                        tmp.append(coords[i * dimension + j])

                if k % 2 == 0:
                    tcoords.extend(tmp[::-1])
                else:
                    tcoords.extend(tmp)

            coords = tcoords
        elif path == "DFS" or path == "BFS":
            # [x, y, weight]
            matrix = [
                [
                    (xv[m][n], yv[m][n], random.uniform(0, 1))
                    for n in range(0, len(yv), 1)
                ]
                for m in range(0, len(xv), 1)
            ]

            class Search:
                # matrix of size m x n
                def __init__(self, matrix: list[list[tuple[float, float, float]]]):
                    self.matrix = matrix
                    self.visited = set()

                def valid(self, mn: tuple[int, int]):
                    in_bounds = 0 <= mn[0] < len(self.matrix[0]) and 0 <= mn[1] < len(
                        self.matrix
                    )
                    return in_bounds and mn not in self.visited

                # breadth first search
                def bfs(self, start: tuple[int, int], end: tuple[int, int]):
                    # double ended queue containing tuples: (node, path)
                    queue = deque([(start, [start])])
                    self.visited.add(start)

                    while queue:
                        current, path = queue.popleft()

                        if current == end:
                            return path

                        for d in [(1, 1), (1, 0), (-1, -1), (-1, 0)]:
                            adjacent_cell = tuple(map(sum, zip(current, d)))
                            if self.valid(adjacent_cell):
                                (m, n) = adjacent_cell[0:2]
                                queue.append((adjacent_cell, path + [adjacent_cell]))
                                self.visited.add(adjacent_cell)

                    return []

                # depth first search
                # find the path with the maximum cost
                def dfs(self, start: tuple[int, int], end: tuple[int, int]):
                    # recursive function
                    def _dfs(
                        mn: tuple[int, int], cost=0
                    ) -> tuple[float, list[tuple[int, int]]]:
                        if mn == end:
                            return (cost, [mn])

                        self.visited.add(mn)

                        # if there's no valid adjacent_cell, the -inf default for max_cost will
                        # discard this branch because it will cost less than all other branches
                        max_cost = float("-inf")
                        max_path = []

                        # find the direction that will maximize the cost
                        # up, right, down, left
                        for d in [(1, 1), (1, 0), (-1, -1), (-1, 0)]:
                            adjacent_cell = tuple(map(sum, zip(mn, d)))

                            if self.valid(adjacent_cell):
                                inner_cost, path = _dfs(
                                    adjacent_cell,
                                    matrix[mn[0]][mn[1]][2] + cost,
                                )

                                if inner_cost > max_cost:
                                    max_cost = inner_cost
                                    max_path = path

                        return (cost + max_cost, [mn] + max_path)

                    return _dfs(start)

            start = (0, 0)
            end = (
                random.randint(0, len(matrix) - 1),
                random.randint(0, len(matrix) - 1),
            )

            search = Search(matrix)
            solution = []

            if path == "DFS":
                solution = search.dfs(start, end)[1]
            elif path == "BFS":
                solution = search.bfs(start, end)
            else:
                raise ValueError(f"unknown search path {path}")

            coords = []
            for v in solution:
                (m, n) = v
                coords.append(matrix[m][n][0:2])

        else:
            raise ValueError("Unknown Path Type")

        for i, v in enumerate(coords):
            c = (v[0], v[1])

            if debug:
                if i == 0 or i == len(coords) - 1:
                    ring = Point(c).buffer(20).simplify(1)
                    self.canvas.pattern.add_block([p for p in ring.exterior.coords])

                ring = Point(c).buffer(10).simplify(10)
                self.canvas.pattern.add_block([p for p in ring.exterior.coords])

            self.canvas.pattern += c

        yield self.canvas.pattern
