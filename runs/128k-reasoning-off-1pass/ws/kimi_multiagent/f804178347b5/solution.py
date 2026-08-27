import sys

def solve():
    data = sys.stdin.read().split()
    n = int(data[0])
    a = data[1].strip()
    size = 3 ** n
    base = size + 1  # any cost is at most 3^n, so this separates f0 and f1 safely

    # Leaf encoding: pair = f0 * base + f1
    # bit '0': f0 = 0, f1 = 1  -> pair = 1
    # bit '1': f0 = 1, f1 = 0  -> pair = base
    vals = [1 if ch == '0' else base for ch in a]

    # Bottom-up reduction: for each internal node, forcing value v requires
    # at least 2 of 3 children to be v -> sum of the two smallest child costs.
    while len(vals) > 1:
        nxt = []
        for i in range(0, len(vals), 3):
            p0 = vals[i]
            p1 = vals[i + 1]
            p2 = vals[i + 2]
            f0_0, f1_0 = divmod(p0, base)
            f0_1, f1_1 = divmod(p1, base)
            f0_2, f1_2 = divmod(p2, base)
            s0 = f0_0 + f0_1 + f0_2
            new_f0 = s0 - max(f0_0, f0_1, f0_2)
            s1 = f1_0 + f1_1 + f1_2
            new_f1 = s1 - max(f1_0, f1_1, f1_2)
            nxt.append(new_f0 * base + new_f1)
        vals = nxt

    f0, f1 = divmod(vals[0], base)
    # The current output's cost is 0; the answer is the cost of the opposite value.
    print(f0 if f1 == 0 else f1)

solve()