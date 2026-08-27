import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = [int(next(it)) for _ in range(N)]

    # gaps[i] = X[i+1] - X[i]  (i = 0..N-2)
    gaps = [X[i+1] - X[i] for i in range(N - 1)]

    # Separate gaps by the parity of their 1‑based index.
    # Index 1,3,5,... (i even) are odd gaps; index 2,4,6,... (i odd) are even gaps.
    odd_gaps = []
    even_gaps = []
    for i, g in enumerate(gaps):
        if i % 2 == 0:
            odd_gaps.append(g)
        else:
            even_gaps.append(g)

    # Within each parity we can permute the gaps arbitrarily.
    # To minimise Σ (N-i)·g_i we should put the smallest gaps at the smallest i
    # (i.e. at the positions with the largest weight N-i).
    odd_gaps.sort()
    even_gaps.sort()

    # Reconstruct the optimal gap sequence.
    new_gaps = [0] * (N - 1)
    for i, g in enumerate(odd_gaps):
        new_gaps[2 * i] = g
    for i, g in enumerate(even_gaps):
        new_gaps[2 * i + 1] = g

    # Total sum = N·x_1 + Σ_{i=1}^{N-1} (N-i)·g_i
    total = N * X[0]
    for i, g in enumerate(new_gaps):
        total += (N - i - 1) * g

    print(total)

if __name__ == "__main__":
    solve()