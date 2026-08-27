import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = [int(next(it)) for _ in range(N)]
    if N == 1:
        print(X[0])
        return
    # Compute gaps
    gaps = [X[i+1] - X[i] for i in range(N-1)]
    odd_gaps = []
    even_gaps = []
    for i, g in enumerate(gaps):
        if i % 2 == 0:
            odd_gaps.append(g)
        else:
            even_gaps.append(g)
    odd_gaps.sort()
    even_gaps.sort()
    # Reconstruct new gaps
    new_gaps = [0] * (N-1)
    oi = 0
    ei = 0
    for i in range(N-1):
        if i % 2 == 0:
            new_gaps[i] = odd_gaps[oi]
            oi += 1
        else:
            new_gaps[i] = even_gaps[ei]
            ei += 1
    # Compute sum: S = N * X[0] + sum_{k=0}^{N-2} (N-1-k) * new_gaps[k]
    total = N * X[0]
    for k, g in enumerate(new_gaps):
        total += (N - 1 - k) * g
    print(total)

if __name__ == "__main__":
    solve()