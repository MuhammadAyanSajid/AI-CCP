# AI Sudoku CSP Solver & Benchmarker

An advanced, modular artificial intelligence framework designed to model, solve, and compare Sudoku puzzles of varying complexity under the Constraint Satisfaction Problem (CSP) paradigm. 

Developed as a Complex Computing Problem (CCP) project for the **Department of Computer Science at the University of Engineering and Technology (UET) Lahore, New Campus**.

---

## Key Features

- **Decoupled AI Engine:** 100% modular implementation of four distinct AI search paradigms (Uninformed DFS, Informed AC-3 + MRV + DH, Standalone Forward Checking, and Simulated Annealing).
- **Zero-Dependency Python Backend:** Served via a multi-threaded, native Python HTTP server requiring no third-party package installations.
- **Interactive UI Sandbox:** Allows users to procedurally generate boards, click any cell to manually edit values, and receive on-the-fly conflict notifications.
- **Adversarial Race Mode:** Simulates two different AI solvers side-by-side at a customizable delay speed (1ms - 500ms) to visually track branching, look-aheads, and backtrack counts.
- **Instant Benchmark Sweep:** Compares execution runtimes, states explored, and backtrack transitions across all four search strategies simultaneously.

---

## Repository Structure

```text
AI-CCP/
│
├── app.py                      # Multi-threaded HTTP Server & API Controller
├── .gitignore                  # Git tracking exclusion filters (e.g. caches)
├── AI CCP Report.docx          # UET Project Report (Word format)
├── AI CCP Report.pdf           # UET Project Report (Compiled PDF)
├── AI_Theory_CCP(1).pdf        # Theoretical background assignment sheet
├── README.md                   # Project documentation index
│
├── engine/                     # Core AI Solver Modules (Separation of Concerns)
│   ├── __init__.py             
│   ├── generator.py            # Procedural unique board generator
│   ├── uninformed.py           # DFS chronological backtracker
│   ├── informed.py             # AC-3, MRV, and DH CSP solver
│   ├── propagation.py          # Standalone Forward Checking solver
│   └── local_search.py         # Simulated Annealing local search solver
│
└── templates/                  # Frontend UI Templates
    └── index.html              # Unified interactive interface & animator
```

---

## Installation & Run Instructions

Since the backend utilizes Python's built-in standard libraries, **no installations or external packages are required**.

### Run the Interactive Web Visualizer
Clone the repository and boot up the multi-threaded daemon:
```bash
git clone https://github.com/MuhammadAyanSajid/AI-CCP.git
cd "AI-CCP"
python app.py
```
Once initialized, open your browser and navigate to: **`http://localhost:8000`**

---

## Core Search Algorithms

1. **Uninformed DFS Backtracking (`engine/uninformed.py`):** Serves as the search baseline, executing chronological state-space traversal with $O(d^{n^2})$ complexity without utilizing look-aheads or variable heuristics.
2. **Informed CSP Solver (`engine/informed.py`):** Integrates Arc Consistency (AC-3) domain reduction, Minimum Remaining Values (MRV) variable selection, and the Degree Heuristic (DH) as a tie-breaker.
3. **Standalone Constraint Propagation (`engine/propagation.py`):** Runs a localized Forward Checking (FC) pass upon each assignment, immediately pruning domain contradictions in peer variables to avoid dead-ends.
4. **Local Search Simulated Annealing (`engine/local_search.py`):** Begins with complete assignments satisfying subgrid boundaries, evaluates global row/column conflicts, and swaps values inside boxes based on a controlled temperature cooling schedule ($T \leftarrow T \times \alpha$).

---

## API Documentation

The server exposes the following REST API endpoints:

### 1. Procedural Generation
* **Endpoint:** `POST /api/generate`
* **Payload:** `difficulty=easy|medium|hard|expert|empty`
* **Response:**
  ```json
  { "grid": [[5,3,0,0,7,...], ...] }
  ```

### 2. Trace Solving
* **Endpoint:** `POST /api/solve`
* **Payload:** `grid=[[...]]&algo=naive|mrv|forward_checking|local_search`
* **Response:** Returns the completion state and a comprehensive array of visual animation steps.
  ```json
  {
    "success": true,
    "states": 142,
    "backtracks": 11,
    "time_taken": 38.4,
    "steps": [{"r": 3, "c": 4, "val": 5, "action": "assign", "domain": [5]}, ...]
  }
  ```

### 3. Parallel Benchmarking
* **Endpoint:** `POST /api/benchmark`
* **Payload:** `grid=[[...]]`
* **Response:** Solves the passed board simultaneously across all algorithms and returns comparison metrics.

---

## Contributors

- [**Muhammad Ayan Sajid**](https://github.com/MuhammadAyanSajid)
- [**Muhammad Husnain**](https://github.com/nexhus) 

**Submitted To:** Mr. [Muhammad Aizaz Akmal](https://www.linkedin.com/in/muhammad-aizaz-akmal-%F0%9F%87%B5%F0%9F%87%B0-aa048b103/)