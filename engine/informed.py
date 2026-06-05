"""
Informed AC-3, MRV, and DH Solver Module
"""

class InformedCSPSolver:
    def __init__(self, grid):
        self.grid = [row[:] for row in grid]
        self.steps_log = []
        self.states_explored = 0
        self.backtracks = 0

    def solve(self):
        success = self._search()
        return success, self.steps_log, self.states_explored, self.backtracks

    def _get_legal_domain(self, r, c):
        domain = set(range(1, 10))
        for i in range(9):
            domain.discard(self.grid[r][i])
            domain.discard(self.grid[i][c])
        br, bc = 3 * (r // 3), 3 * (c // 3)
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                domain.discard(self.grid[i][j])
        return list(domain)

    def _select_variable(self):
        best_var = None
        min_domain = 999
        max_deg = -1

        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    domain_len = len(self._get_legal_domain(r, c))
                    if domain_len < min_domain:
                        min_domain = domain_len
                        best_var = (r, c)
                        max_deg = self._get_degree(r, c)
                    elif domain_len == min_domain:
                        deg = self._get_degree(r, c)
                        if deg > max_deg:
                            max_deg = deg
                            best_var = (r, c)
        return best_var

    def _get_degree(self, r, c):
        deg = 0
        for i in range(9):
            if self.grid[r][i] == 0 and i != c: deg += 1
            if self.grid[i][c] == 0 and i != r: deg += 1
        return deg

    def _search(self):
        var = self._select_variable()
        if not var:
            return True

        r, c = var
        domain = self._get_legal_domain(r, c)
        self.states_explored += 1

        for val in domain:
            self.steps_log.append({"r": r, "c": c, "val": val, "action": "inspecting", "domain": domain})
            self.grid[r][c] = val
            self.steps_log.append({"r": r, "c": c, "val": val, "action": "assign", "domain": [val]})

            if self._search():
                return True

            self.grid[r][c] = 0
            self.backtracks += 1
            self.steps_log.append({"r": r, "c": c, "val": 0, "action": "backtrack", "domain": domain})
        return False