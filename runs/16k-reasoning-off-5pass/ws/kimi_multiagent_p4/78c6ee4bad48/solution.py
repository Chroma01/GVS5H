import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = list(map(int, data[1:1 + n]))
    # gaps g_k = x[k] - x[k-1], 1-indexed k = 1..n-1
    odd = []   # gaps at odd 1-indexed positions
    even = []  # gaps at even 1-indexed positions
    for k in range(1, n):
        g = x[k] - x[k - 1]
        if k & 1:
            odd.append(g)
        else:
            even.append(g)
    odd.sort()   # ascending
    even.sort()  # ascending
    # weights w_k = n - k, decreasing in k.
    # Minimize sum w_k * g_k within each parity class:
    # pair ascending gaps with descending weights (rearrangement inequality).
    ans = n * x[0]
    # odd class: k = 1, 3, 5, ... weights n-1, n-3, ... (descending)
    w = n - 1
    for g in odd:
        ans += w * g
        w -= 2
    # even class: k = 2, 4, 6, ... weights n-2, n-4, ... (descending)
    w = n - 2
    for g in even:
        ans += w * g
        w -= 2
    print(ans)

main()