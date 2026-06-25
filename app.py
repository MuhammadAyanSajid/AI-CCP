import os
import json
import time
from urllib.parse import parse_qs
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from engine.generator import SudokuEngine
from engine.uninformed import UninformedDFSSolver
from engine.informed import InformedCSPSolver
from engine.propagation import ForwardCheckingSolver
from engine.local_search import LocalSearchSASolver

class UnifiedAppHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress generic terminal request outputs

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            
            # Resolve templates/index.html path dynamically
            template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
            with open(template_path, "r", encoding="utf-8") as f:
                index_html = f.read()
            self.wfile.write(index_html.encode("utf-8"))
        else:
            self.send_error(404, "Target Asset Not Found")

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        params = parse_qs(body)

        if self.path == "/api/generate":
            diff = params.get("difficulty", ["medium"])[0]
            
            # Handle special configuration modes explicitly on the backend
            if diff == "empty":
                puzzle = [[0]*9 for _ in range(9)]
            else:
                engine = SudokuEngine()
                puzzle = engine.generate_puzzle(diff)
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"grid": puzzle}).encode("utf-8"))

        elif self.path == "/api/solve":
            grid_str = params.get("grid", [""])[0]
            algo = params.get("algo", ["naive"])[0]
            
            if not grid_str:
                self.send_error(400, "Missing Matrix Parameters")
                return

            grid = json.loads(grid_str)
            
            # Instantiate the corresponding modular engine solver
            if algo == "naive":
                solver = UninformedDFSSolver(grid)
            elif algo == "mrv":
                solver = InformedCSPSolver(grid)
            elif algo == "forward_checking":
                solver = ForwardCheckingSolver(grid)
            else:
                solver = LocalSearchSASolver(grid)

            start = time.perf_counter()
            success, trace, states, backtracks = solver.solve()
            elapsed_ms = (time.perf_counter() - start) * 1000.0

            response_data = {
                "success": success,
                "steps": trace,
                "states": states,
                "backtracks": backtracks,
                "time_taken": elapsed_ms
            }

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))

        elif self.path == "/api/benchmark":
            grid_str = params.get("grid", [""])[0]
            if not grid_str:
                self.send_error(400, "Missing Grid Parameter")
                return
            
            grid = json.loads(grid_str)
            
            solvers = [
                ("Uninformed DFS", UninformedDFSSolver(grid)),
                ("Informed (AC-3+MRV)", InformedCSPSolver(grid)),
                ("Propagation (FC)", ForwardCheckingSolver(grid)),
                ("Local Search (SA)", LocalSearchSASolver(grid))
            ]

            results = []
            for name, solver in solvers:
                start = time.perf_counter()
                success, _, states, backtracks = solver.solve()
                elapsed_ms = (time.perf_counter() - start) * 1000.0
                results.append({
                    "name": name,
                    "success": success,
                    "states": states,
                    "backtracks": backtracks,
                    "time": elapsed_ms
                })

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(results).encode("utf-8"))

def run_server():
    # Read the dynamically assigned PORT from the environment, defaulting to 8000 locally
    port = int(os.environ.get("PORT", 8000))
    server_address = ("", port)
    
    httpd = ThreadingHTTPServer(server_address, UnifiedAppHandler)
    print("=" * 60)
    print(f"CSP Multi-Threaded Server is running.")
    print(f"Port: {port}")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n Server shutting down.")
        httpd.server_close()

if __name__ == "__main__":
    run_server()