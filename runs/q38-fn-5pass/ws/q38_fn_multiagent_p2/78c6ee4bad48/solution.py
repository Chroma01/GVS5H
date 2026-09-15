import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N = data[0]
    X = data[1:1 + N]

    odd_gaps = []
    even_gaps = []

    # gap index j is 1-based: j = i + 1 in 0-based loop
    # odd j corresponds to even i, even j corresponds to odd i
    for i in range(N - 1):
        gap = X[i + 1] - X[i]
        if i % 2 == 0:
            odd_gaps.append(gap)
        else:
            even_gaps.append(gap)

    odd_gaps.sort()
    even_gaps.sort()

    ans = N * X[0]

    # Odd gap positions: j = 1, 3, 5, ...
    for idx, gap in enumerate(odd_gaps):
        j = 2 * idx + 1
        ans += (N - j) * gap

    # Even gap positions: j = 2, 4, 6, ...
    for idx, gap in enumerate(even_gaps):
        j = 2 * idx + 2
        ans += (N - j) * gap

    print(ans)

if __name__ == "__main__":
    main()