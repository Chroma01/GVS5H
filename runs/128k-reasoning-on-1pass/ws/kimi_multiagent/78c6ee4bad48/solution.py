import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    x = list(map(int, data[1:1 + n]))

    gaps = [x[i + 1] - x[i] for i in range(n - 1)]

    # For four consecutive sorted points with gaps (a, b, c):
    # (A, A+a, A+a+b, A+a+b+c) -> (A, A+c, A+b+c, A+a+b+c),
    # so the sorted gaps become (c, b, a): only g[i] and g[i+2] swap.
    # Thus parity of gap index is invariant, and same-parity adjacent swaps
    # generate every permutation inside each parity class.
    odd = []
    even = []
    for idx, g in enumerate(gaps, start=1):
        if idx & 1:
            odd.append(g)
        else:
            even.append(g)

    odd.sort()
    even.sort()

    # Sum = n*x[0] + sum((n-k) * gap_k). Weights n-k decrease with k,
    # so by rearrangement each parity class gets small gaps left, large gaps right.
    new_gaps = [0] * (n - 1)
    oi = ei = 0
    for k in range(1, n):
        if k & 1:
            new_gaps[k - 1] = odd[oi]
            oi += 1
        else:
            new_gaps[k - 1] = even[ei]
            ei += 1

    ans = n * x[0]
    for k in range(1, n):
        ans += (n - k) * new_gaps[k - 1]

    print(ans)

if __name__ == "__main__":
    main()