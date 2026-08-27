import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    x = int(data[1])

    f = [0] * n
    d = [0] * n
    total = 0

    idx = 2
    for i in range(n):
        u = int(data[idx])
        di = int(data[idx + 1])
        idx += 2
        f[i] = u
        d[i] = di
        total += u + di

    # f[i] = min_j (U[j] + X * |i - j|)
    # Left-to-right pass: candidates j <= i
    for i in range(1, n):
        v = f[i - 1] + x
        if f[i] > v:
            f[i] = v

    # Right-to-left pass: candidates j >= i
    for i in range(n - 2, -1, -1):
        v = f[i + 1] + x
        if f[i] > v:
            f[i] = v

    h = min(f[i] + d[i] for i in range(n))
    print(total - n * h)

if __name__ == "__main__":
    main()