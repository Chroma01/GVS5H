import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = list(map(int, data[1:1 + n]))
    # gaps d_k = x[k] - x[k-1] for k = 1..n-1 (1-indexed k)
    # weight w_k = n - k
    # parity classes based on k % 2
    gaps = [[], []]
    weights = [[], []]
    for k in range(1, n):
        p = k & 1
        gaps[p].append(x[k] - x[k - 1])
        weights[p].append(n - k)
    total = n * x[0]
    for p in (0, 1):
        gaps[p].sort(reverse=True)
        weights[p].sort()
        for g, w in zip(gaps[p], weights[p]):
            total += g * w
    print(total)

main()