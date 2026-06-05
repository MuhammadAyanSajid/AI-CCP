"""
Constraint Propagation (Forward Checking) Module
"""

class ForwardCheckingSolver:
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

    def _search(self):
        best_var = None
        min_domain = 999
        for r in range(9):
            for c in range(9):
                if self.grid[r][c] == 0:
                    d_len = len(self._get_legal_domain(r, c))
                    if d_len < min_domain:
                        min_domain = d_len
                        best_var = (r, c)

        if not best_var:
            return True

        r, c = best_var
        domain = self._get_legal_domain(r, c)
        self.states_explored += 1

        for val in domain:
            self.steps_log.append({"r": r, "c": c, "val": val, "action": "inspecting", "domain": domain})
            self.grid[r][c] = val
            self.steps_log.append({"r": r, "c": c, "val": val, "action": "assign", "domain": [val]})

            # Forward Checking checks
            failed = False
            pruned_coords = []
            for idx in range(9):
                if idx != c and self.grid[r][idx] == 0:
                    peer_domain = self._get_legal_domain(r, idx)
                    if len(peer_domain) == 0:
                        failed = True
                        pruned_coords.append((r, idx))
                if idx != r and self.grid[idx][c] == 0:
                    peer_domain = self._get_legal_domain(idx, c)
                    if len(peer_domain) == 0:
                        failed = True
                        pruned_coords.append((idx, c))

            if failed:
                for pr, pc in pruned_coords:
                    self.steps_log.append({"r": pr, "c": pc, "val": 0, "action": "prune", "domain": []})
                self.grid[r][c] = 0
                self.backtracks += 1
                self.steps_log.append({"r": r, "c": c, "val": 0, "action": "backtrack", "domain": domain})
                continue

            if self._search():
                return True

            self.grid[r][c] = 0
            self.backtracks += 1
            self.steps_log.append({"r": r, "c": c, "val": 0, "action": "backtrack", "domain": domain})
        return False