import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    X = data[1:1 + N]

    gaps = [X[i + 1] - X[i] for i in range(N - 1)]

    # 1-indexed odd gap positions correspond to 0-indexed even indices.
    odd_gaps = sorted(gaps[0::2])
    # 1-indexed even gap positions correspond to 0-indexed odd indices.
    even_gaps = sorted(gaps[1::2])

    ans = N * X[0]

    # Odd gap positions: 1, 3, 5, ...
    # Their weights are N-1, N-3, N-5, ...
    for j, g in enumerate(odd_gaps):
        ans += g * (N - (2 * j + 1))

    # Even gap positions: 2, 4, 6, ...
    # Their weights are N-2, N-4, N-6, ...
    for j, g in enumerate(even_gaps):
        ans += g * (N - (2 * j + 2))

    print(ans)

if __name__ == "__main__":
    main()