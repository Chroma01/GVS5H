import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    x = data[1]

    u = [0] * n
    d = [0] * n
    total = 0

    idx = 2
    for i in range(n):
        ui = data[idx]
        di = data[idx + 1]
        idx += 2
        u[i] = ui
        d[i] = di
        total += ui + di

    a = u[:]

    for i in range(1, n):
        v = a[i - 1] + x
        if v < a[i]:
            a[i] = v

    for i in range(n - 2, -1, -1):
        v = a[i + 1] + x
        if v < a[i]:
            a[i] = v

    h = min(a[i] + d[i] for i in range(n))
    ans = total - n * h
    print(ans)

if __name__ == "__main__":
    main()