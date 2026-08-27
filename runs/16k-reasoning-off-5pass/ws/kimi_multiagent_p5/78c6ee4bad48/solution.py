import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = list(map(int, data[1:1 + n]))
    # gaps g_k = x_{k+1} - x_k, 1-indexed conceptually
    odd = []  # gaps at odd 1-based indices: 1, 3, 5, ...
    even = []  # gaps at even 1-based indices: 2, 4, 6, ...
    for k in range(1, n):
        g = x[k] - x[k - 1]
        if k % 2 == 1:
            odd.append(g)
        else:
            even.append(g)
    # Operation reverses 3 consecutive gaps => swaps gaps at distance 2.
    # So gaps can be permuted arbitrarily within each parity class.
    # Sum = N*x_1 + sum_{k=1}^{N-1} (N-k)*g_k, weights N-k decrease with k.
    # Minimize: assign ascending gaps to increasing indices (descending weights)
    # within each parity class (rearrangement inequality).
    odd.sort()
    even.sort()
    ans = n * x[0]
    io = ie = 0
    for k in range(1, n):
        if k % 2 == 1:
            g = odd[io]
            io += 1
        else:
            g = even[ie]
            ie += 1
        ans += (n - k) * g
    sys.stdout.write(str(ans) + "\n")

main()