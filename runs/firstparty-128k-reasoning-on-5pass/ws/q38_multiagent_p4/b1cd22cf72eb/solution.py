import sys

def main():
    input = sys.stdin.buffer.readline
    first = input().split()
    if not first:
        return

    n = int(first[0])
    x = int(first[1])

    u = [0] * n
    d = [0] * n
    total = 0

    for i in range(n):
        ui, di = map(int, input().split())
        u[i] = ui
        d[i] = di
        total += ui + di

    left = [0] * n
    left[0] = u[0]
    for i in range(1, n):
        left[i] = min(u[i], left[i - 1] + x)

    INF = 10**30
    right = INF
    h = INF

    for i in range(n - 1, -1, -1):
        right = min(u[i], right + x)
        e = min(left[i], right)
        h = min(h, e + d[i])

    print(total - n * h)

if __name__ == "__main__":
    main()