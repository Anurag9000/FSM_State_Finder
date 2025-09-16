# Binary Pattern Detector FSM Generator

A Python tool that automatically generates **Finite State Machines (FSMs)** for binary pattern detection.
Given a binary sequence (e.g. `1011`), the tool produces:

* **Synthesizable Verilog HDL code** for a sequence detector (handles overlapping patterns)
* **Graphviz diagrams** (DOT, PNG, SVG) to visualize the state machine

---

## Features

* Converts any binary pattern into a **deterministic finite automaton (DFA)**
* Generates clean Verilog `always @(*)` + `case` next-state logic
* Supports **overlapping detection** (e.g., `1011` detected even in `10111`)
* Exports **FSM diagrams** (DOT + rendered PNG/SVG) for documentation and debugging
* Automatically manages Graphviz path setup (Windows-friendly)
* Saves outputs to a `diagrams/` folder for organization

---

## Example

Input pattern:

```bash
python FSM_Mach.py 1011
```

Generated outputs:

* `fsm_1011.v` → Verilog FSM module
* `fsm_1011.dot` / `fsm_1011.png` → Graphviz diagram

**FSM Diagram (for pattern `1011`):**

![FSM Example](diagrams/fsm_1011.png)

---

## Usage

1. Clone the repo and install [Graphviz](https://graphviz.org/download/).
2. Run the script with your desired binary pattern:

```bash
python FSM_Mach.py 1101
```

3. Find generated Verilog and diagrams in the `diagrams/` folder.

---

## Technical Details

* **States**: `S0 … Sk` (where `k = len(pattern)`)
* **Transitions**: Computed using prefix-function style logic (handles overlaps)
* **Verilog Module**: Synthesizable, Moore-style FSM
* **Visualization**: Directed graph with labeled edges (`0` / `1` inputs)

---

## Applications

* **Digital Design Education**: Teaching FSMs and sequence detection
* **FPGA/ASIC Prototyping**: Quick sequence detector generation
* **Documentation**: Attaching FSM diagrams alongside Verilog modules
* **Research Tools**: Bridging automata theory with practical HDL design

---

## Roadmap / Possible Extensions

* Support **non-binary alphabets** (ASCII, DNA, etc.)
* Add **Mealy vs Moore machine options**
* Generate **testbenches** for simulation
* Build a **CLI/GUI** for easier use

---

## License

MIT License
