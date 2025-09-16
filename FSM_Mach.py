# pip install graphviz
# Also install the Graphviz system binary (dot.exe). If not installed, you'll still get a .dot file.
# Windows-only convenience: add Graphviz bin to PATH at runtime (safe if already present).
import os
import platform
import subprocess
from graphviz import Digraph

# (Optional) Ensure Graphviz bin is on PATH for this process (adjust path if your install differs)
GV_BIN = r"C:\Program Files\Graphviz\bin"
if os.path.isdir(GV_BIN) and GV_BIN not in os.environ.get("PATH", ""):
    os.environ["PATH"] += os.pathsep + GV_BIN

OUT_DIR = os.path.join(os.getcwd(), "diagrams")
os.makedirs(OUT_DIR, exist_ok=True)

def build_transitions(pattern: str):
    seq = [ch for ch in pattern.strip()]
    plen = len(seq)

    def nxt(state_len, bit):
        temp = seq[:state_len] + [bit]
        limit = min(len(temp), plen)
        for size in range(limit, -1, -1):
            suffix = temp[-size:] if size > 0 else []
            prefix = seq[:size]
            if suffix == prefix:
                return size
        return 0

    transitions = {}
    for st in range(plen + 1):
        transitions[st] = {'0': nxt(st, '0'), '1': nxt(st, '1')}
    return transitions, plen

def verilog_case(transitions, plen):
    lines = []
    lines.append("always @(*) begin")
    lines.append("    case (present_state)")
    for st in range(plen + 1):
        t0 = transitions[st]['0']
        t1 = transitions[st]['1']
        lines.append(f"        S{st}: next_state = din ? S{t1} : S{t0};")
    lines.append("        default: next_state = S0;")
    lines.append("    endcase")
    lines.append("end")
    return "\n".join(lines)

def graphviz_fsm(transitions, plen, title="Pattern FSM", highlight_accept=True):
    g = Digraph(comment=title, graph_attr={"rankdir": "LR", "fontsize": "12"})
    # Start arrow
    g.node("start", shape="point")
    g.edge("start", "S0", label="")

    # Nodes (accepting state = final match S{plen})
    for st in range(plen + 1):
        shape = "doublecircle" if (highlight_accept and st == plen) else "circle"
        g.node(f"S{st}", shape=shape)

    # Edges
    for st in range(plen + 1):
        for bit in ("0", "1"):
            to = transitions[st][bit]
            g.edge(f"S{st}", f"S{to}", label=bit)

    return g

def open_file(path: str):
    try:
        if platform.system() == "Windows":
            os.startfile(path)  # type: ignore[attr-defined]
        elif platform.system() == "Darwin":
            subprocess.run(["open", path], check=False)
        else:
            subprocess.run(["xdg-open", path], check=False)
    except Exception as e:
        print(f"(Could not auto-open file) {e}")

def main():
    while True:
        pattern = input("Enter pattern: ").strip()
        if not pattern:
            break

        transitions, plen = build_transitions(pattern)
        print("\n// ===== Verilog next-state logic =====")
        print(verilog_case(transitions, plen))

        print("\n// ===== Graphviz diagram =====")
        dot = graphviz_fsm(transitions, plen, title=f"FSM for pattern '{pattern}'")
        base = f"fsm_{pattern}"

        # Save DOT in diagrams/
        dot_path = dot.save(filename=f"{base}.dot", directory=OUT_DIR)
        print(f"Wrote DOT: {dot_path}")

        # Render PNG + SVG in diagrams/
        try:
            png_path = dot.render(filename=base, directory=OUT_DIR, format="png", cleanup=True)
            svg_path = dot.render(filename=base, directory=OUT_DIR, format="svg", cleanup=True)
            print(f"Rendered PNG: {png_path}")
            print(f"Rendered SVG: {svg_path}")

            # Auto-open the PNG
            open_file(png_path)
        except Exception as e:
            print(f"(Render skipped: install Graphviz system binary to render images) {e}")

if __name__ == "__main__":
    main()
