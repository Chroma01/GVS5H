import sys
from functools import lru_cache


def predict(n, feats):
    m, p, x, i, o, f = feats

    if n & 1:
        return (m & 1) == 1

    # Even N.
    if o == 0:
        return ((p + (i // 2)) & 1) == 1

    if o <= 2:
        return True

    return p != f


def solve_large(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * n
    comp = [-1] * n
    comp_info = []

    for s in range(n):
        if color[s] != -1:
            continue

        cid = len(comp_info)
        color[s] = 0
        comp[s] = cid
        stack = [s]
        a = 1
        b = 0

        while stack:
            u = stack.pop()
            cu = color[u]
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = cu ^ 1
                    comp[v] = cid
                    if color[v] == 0:
                        a += 1
                    else:
                        b += 1
                    stack.append(v)

        comp_info.append((a + b, a, b))

    c = len(comp_info)
    e_count = [0] * c
    for u, v in edges:
        e_count[comp[u]] += 1

    p = 0
    x = 0
    i = 0
    o = 0
    f = 0

    for cid, (size, a, b) in enumerate(comp_info):
        p ^= (a * b - e_count[cid]) & 1

        if size == 1:
            x += 1
            i += 1
        elif size & 1:
            x += 1
            o += 1
        else:
            if a & 1:
                f ^= 1

    return predict(n, (len(edges), p, x, i, o, f))


def reduced_dp(max_c=16):
    @lru_cache(maxsize=None)
    def win(state):
        i, o, e0, e1, p = state

        # Internal move: adding a missing edge inside a component toggles p.
        # Only p=1 -> p=0 is needed for P/N determination.
        if p == 1:
            if not win((i, o, e0, e1, 0)):
                return True

        # isolated + isolated -> odd/odd even component, p unchanged
        if i >= 2:
            if not win((i - 2, o, e0, e1 + 1, p)):
                return True

        # isolated + odd -> even/even with p toggled, or odd/odd with p unchanged
        if i >= 1 and o >= 1:
            if not win((i - 1, o - 1, e0 + 1, e1, 1 - p)):
                return True
            if not win((i - 1, o - 1, e0, e1 + 1, p)):
                return True

        # isolated + even/even -> odd component, p toggled
        if i >= 1 and e0 >= 1:
            if not win((i - 1, o + 1, e0 - 1, e1, 1 - p)):
                return True

        # isolated + odd/odd -> odd component, p unchanged
        if i >= 1 and e1 >= 1:
            if not win((i - 1, o + 1, e0, e1 - 1, p)):
                return True

        # odd + odd -> even/even with p toggled, or odd/odd with p unchanged
        if o >= 2:
            if not win((i, o - 2, e0 + 1, e1, 1 - p)):
                return True
            if not win((i, o - 2, e0, e1 + 1, p)):
                return True

        # odd + even/even -> odd component, p toggled
        if o >= 1 and e0 >= 1:
            if not win((i, o, e0 - 1, e1, 1 - p)):
                return True

        # odd + odd/odd -> odd component, p unchanged
        if o >= 1 and e1 >= 1:
            if not win((i, o, e0, e1 - 1, p)):
                return True

        # even/even + even/even -> even/even, p toggled
        if e0 >= 2:
            if not win((i, o, e0 - 1, e1, 1 - p)):
                return True

        # even/even + odd/odd -> odd/odd, p toggled
        if e0 >= 1 and e1 >= 1:
            if not win((i, o, e0 - 1, e1, 1 - p)):
                return True

        # odd/odd + odd/odd -> even/even, p toggled
        if e1 >= 2:
            if not win((i, o, e0 + 1, e1 - 2, 1 - p)):
                return True

        return False

    states = []
    for i in range(max_c + 1):
        for o in range(max_c + 1 - i):
            for e0 in range(max_c + 1 - i - o):
                for e1 in range(max_c + 1 - i - o - e0):
                    if (i + o) & 1:
                        continue
                    for p in (0, 1):
                        states.append((i, o, e0, e1, p))

    mismatches = []
    for s in states:
        i, o, e0, e1, p = s
        x = i + o
        f = e1 & 1
        pred_win = predict(2, (0, p, x, i, o, f))
        dp_win = win(s)
        if pred_win != dp_win:
            mismatches.append((s, dp_win, pred_win))

    print(f"Reduced even-N DP max_c={max_c}")
    print(f"states={len(states)} mismatches={len(mismatches)}")
    if mismatches:
        for s, dp_win, pred_win in mismatches[:20]:
            print(f"mismatch state={s} dp={dp_win} predict={pred_win}")

    specific = [(0, 4, 0, 1, 1), (0, 6, 0, 0, 0)]
    for s in specific:
        w = win(s)
        print(f"specific state {s} losing={not w}")
        if w:
            print("ERROR: specific state is winning")


def main():
    data = sys.stdin.read().strip()

    if not data:
        reduced_dp(16)
        return

    parts = list(map(int, data.split()))
    if not parts:
        return

    n, m = parts[0], parts[1]
    edges = []
    idx = 2
    for _ in range(m):
        u = parts[idx] - 1
        v = parts[idx + 1] - 1
        idx += 2
        edges.append((u, v))

    print("Aoki" if solve_large(n, edges) else "Takahashi")


if __name__ == "__main__":
    main()