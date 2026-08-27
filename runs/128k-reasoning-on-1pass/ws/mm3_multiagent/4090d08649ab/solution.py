import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    A = [int(next(it)) for _ in range(N)]

    # 1. Sum of distinct counts over all subarrays
    last_pos = [0] * (N + 2)          # last occurrence of each value (1..N)
    total_distinct = 0
    for i, v in enumerate(A):
        prev = last_pos[v]            # previous occurrence (0 if none)
        # i is 0‑based, position = i+1
        total_distinct += (i + 1 - prev) * (N - i)
        last_pos[v] = i + 1

    # 2. Sum of adjacent value pairs over all subarrays
    last = [0] * (N + 2)              # last occurrence while scanning
    cur = 0                           # Σ_{v=1}^{N-1} min(last[v], last[v+1]) for current R
    total_adj = 0

    for i, a in enumerate(A):
        # pairs that can change: (a-1, a) and (a, a+1)
        vs = []
        if a > 1:
            vs.append(a - 1)
        if a < N:
            vs.append(a)

        # old minima before updating last[a]
        old_mins = [min(last[v], last[v + 1]) for v in vs]

        # update last occurrence of a
        last[a] = i + 1

        # recompute minima and update cur
        for v, old in zip(vs, old_mins):
            new = min(last[v], last[v + 1])
            cur += new - old

        total_adj += cur

    # 3. Final answer
    ans = total_distinct - total_adj
    sys.stdout.write(str(ans))

if __name__ == "__main__":
    solve()