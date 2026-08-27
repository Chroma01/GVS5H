import sys

def main():
    input = sys.stdin.buffer.readline
    n, x = map(int, input().split())

    u = [0] * n
    d = [0] * n
    total = 0

    for i in range(n):
        u[i], d[i] = map(int, input().split())
        total += u[i] + d[i]

    best = [0] * n

    cur = 10**30
    for i in range(n):
        cur = min(u[i], cur + x)
        best[i] = cur

    cur = 10**30
    for i in range(n - 1, -1, -1):
        cur = min(u[i], cur + x)
        if cur < best[i]:
            best[i] = cur

    h = min(d[i] + best[i] for i in range(n))
    print(total - n * h)

if __name__ == "__main__":
    main()