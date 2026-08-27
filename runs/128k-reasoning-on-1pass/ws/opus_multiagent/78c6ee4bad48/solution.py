import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    X = list(map(int, data[1:1 + n]))
    # gaps d_k = X[k] - X[k-1] for k = 1..n-1 (1-based gap index)
    odd = []
    even = []
    prev = X[0]
    for k in range(1, n):
        cur = X[k]
        g = cur - prev
        prev = cur
        if k & 1:
            odd.append(g)
        else:
            even.append(g)
    odd.sort()
    even.sort()
    total = n * X[0]
    io = 0
    ie = 0
    for k in range(1, n):
        if k & 1:
            g = odd[io]
            io += 1
        else:
            g = even[ie]
            ie += 1
        total += (n - k) * g
    sys.stdout.write(str(total) + "\n")

main()