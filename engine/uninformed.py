class UninformedDFSSolver:
    def __init__(self, grid):
        self.grid = [row[:] for row in grid]
        self.steps_log = []
        self.states_explored = 0
        self.backtracks = 0

    def solve(self):
        success = self._backtrack(0, 0)
        return success, self.steps_log, self.states_explored, self.backtracks

    def _backtrack(self, r, c):
        if c == 9:
            r += 1
            c = 0
        if r == 9:
            return True

        if self.grid[r][c] != 0:
            return self._backtrack(r, c + 1)

        self.states_explored += 1
        for val in range(1, 10):
            self.steps_log.append({"r": r, "c": c, "val": val, "action": "inspecting", "domain": list(range(1, 10))})
            if self._is_valid(r, c, val):
                self.grid[r][c] = val
                self.steps_log.append({"r": r, "c": c, "val": val, "action": "assign", "domain": [val]})
                
                if self._backtrack(r, c + 1):
                    return True
                
                self.grid[r][c] = 0
                self.backtracks += 1
                self.steps_log.append({"r": r, "c": c, "val": 0, "action": "backtrack", "domain": list(range(1, 10))})
        return False

    def _is_valid(self, r, c, val):
        for i in range(9):
            if self.grid[r][i] == val or self.grid[i][c] == val:
                return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if self.grid[i][j] == val:
                    return False
        return True