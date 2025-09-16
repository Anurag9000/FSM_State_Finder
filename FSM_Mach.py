def main(pattern):
    seq = [ch for ch in pattern.strip()]
    plen = len(seq)

    def next(state_len, bit):
        temp_seq = seq[:state_len] + [bit]
        limit = min(len(temp_seq), plen)
        for size in range(limit, -1, -1):
            suffix = temp_seq[-size:] if size > 0 else []
            prefix = seq[:size]
            if suffix == prefix:
                return size
        return 0

    code = []
    code.append("always @(*) begin")
    code.append("    case (present_state)")
    for st in range(plen + 1):
        nxt0 = next(st, '0')
        nxt1 = next(st, '1')
        code.append(f"        S{st}: next_state = din ? S{nxt1} : S{nxt0};")
    code.append("        default: next_state = S0;")
    code.append("    endcase")
    code.append("end")
    return "\n".join(code)


while True:
    inp = input("Enter pattern: ")
    if not inp:
        break
    print(main(inp), end="\n\n")
