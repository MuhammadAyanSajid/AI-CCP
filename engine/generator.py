"""
Procedural Grid Generator Module
"""
import random

class SudokuEngine:
    def __init__(self):
        pass

    def generate_completed_grid(self):
        grid = [[0]*9 for _ in range(9)]
        self._fill_grid(grid)
        return grid

    def _fill_grid(self, grid):
        for r in range(9):
            for c in range(9):
                if grid[r][c] == 0:
                    nums = list(range(1, 10))
                    random.shuffle(nums)
                    for num in nums:
                        if self.is_consistent(grid, r, c, num):
                            grid[r][c] = num
                            if self._fill_grid(grid):
                                return True
                            grid[r][c] = 0
                    return False
        return True

    def is_consistent(self, grid, r, c, val):
        for i in range(9):
            if grid[r][i] == val and i != c:
                return False
            if grid[i][c] == val and i != r:
                return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if grid[i][j] == val and (i != r or j != c):
                    return False
        return True

    def generate_puzzle(self, difficulty):
        completed = self.generate_completed_grid()
        puzzle = [row[:] for row in completed]
        clues_target = {
            "easy": 42,
            "medium": 34,
            "hard": 26,
            "expert": 17
        }.get(difficulty, 34)

        cells_to_remove = 81 - clues_target
        coords = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(coords)

        for i in range(cells_to_remove):
            r, c = coords[i]
            puzzle[r][c] = 0
        return puzzle