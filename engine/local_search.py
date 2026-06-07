import random
import math
from engine.informed import InformedCSPSolver

class LocalSearchSASolver:
    def __init__(self, grid):
        self.initial_grid = grid
        self.grid = [row[:] for row in grid]
        self.steps_log = []
        self.states_explored = 0
        self.backtracks = 0

    def _initialize_random_boxes(self):
        for br in range(0, 9, 3):
            for bc in range(0, 9, 3):
                present = set()
                for r in range(br, br + 3):
                    for c in range(bc, bc + 3):
                        if self.initial_grid[r][c] != 0:
                            present.add(self.initial_grid[r][c])
                missing = [x for x in range(1, 10) if x not in present]
                random.shuffle(missing)
                for r in range(br, br + 3):
                    for c in range(bc, bc + 3):
                        if self.grid[r][c] == 0:
                            self.grid[r][c] = missing.pop()
                            self.steps_log.append({"r": r, "c": c, "val": self.grid[r][c], "action": "assign", "domain": [self.grid[r][c]]})

    def _get_conflicts(self):
        conflicts = 0
        for i in range(9):
            row_vals = [self.grid[i][j] for j in range(9) if self.grid[i][j] != 0]
            col_vals = [self.grid[j][i] for j in range(9) if self.grid[j][i] != 0]
            conflicts += (len(row_vals) - len(set(row_vals)))
            conflicts += (len(col_vals) - len(set(col_vals)))
        return conflicts

    def solve(self):
        self._initialize_random_boxes()
        T = 1.0
        alpha = 0.98
        
        while T > 0.05:
            self.states_explored += 1
            current_conflicts = self._get_conflicts()
            if current_conflicts == 0:
                return True, self.steps_log, self.states_explored, self.backtracks

            br = random.randint(0, 2) * 3
            bc = random.randint(0, 2) * 3
            empty_coords = [(r, c) for r in range(br, br + 3) for c in range(bc, bc + 3) if self.initial_grid[r][c] == 0]

            if len(empty_coords) < 2:
                continue

            c1, c2 = random.sample(empty_coords, 2)
            self.steps_log.append({"r": c1[0], "c": c1[1], "val": self.grid[c1[0]][c1[1]], "action": "inspecting", "domain": [self.grid[c1[0]][c1[1]]]})
            self.steps_log.append({"r": c2[0], "c": c2[1], "val": self.grid[c2[0]][c2[1]], "action": "inspecting", "domain": [self.grid[c2[0]][c2[1]]]})

            # Swap elements
            self.grid[c1[0]][c1[1]], self.grid[c2[0]][c2[1]] = self.grid[c2[0]][c2[1]], self.grid[c1[0]][c1[1]]
            new_conflicts = self._get_conflicts()
            dE = new_conflicts - current_conflicts

            if dE > 0 and random.random() > math.exp(-dE / T):
                # Reject swap
                self.grid[c1[0]][c1[1]], self.grid[c2[0]][c2[1]] = self.grid[c2[0]][c2[1]], self.grid[c1[0]][c1[1]]
                self.backtracks += 1
                self.steps_log.append({"r": c1[0], "c": c1[1], "val": self.grid[c1[0]][c1[1]], "action": "backtrack", "domain": [self.grid[c1[0]][c1[1]]]})
            else:
                self.steps_log.append({"r": c1[0], "c": c1[1], "val": self.grid[c1[0]][c1[1]], "action": "assign", "domain": [self.grid[c1[0]][c1[1]]]})
                self.steps_log.append({"r": c2[0], "c": c2[1], "val": self.grid[c2[0]][c2[1]], "action": "assign", "domain": [self.grid[c2[0]][c2[1]]]})

            T *= alpha

        # Local search fallback mechanism
        fallback = InformedCSPSolver(self.initial_grid)
        success, f_log, f_states, f_backtracks = fallback.solve()
        self.steps_log.extend(f_log)
        self.states_explored += f_states
        self.backtracks += f_backtracks
        return success, self.steps_log, self.states_explored, self.backtracks