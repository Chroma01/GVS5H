import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, x = data[0], data[1]
    u = [0] * n
    d = [0] * n
    total = 0

    p = 2
    for i in range(n):
        u[i] = data[p]
        d[i] = data[p + 1]
        total += u[i] + d[i]
        p += 2

    nearest_upper = [0] * n

    best = 10**30
    for i in range(n):
        if i == 0:
            best = u[i]
        else:
            best = min(u[i], best + x)
        nearest_upper[i] = best

    best = 10**30
    for i in range(n - 1, -1, -1):
        if i == n - 1:
            best = u[i]
        else:
            best = min(u[i], best + x)
        nearest_upper[i] = min(nearest_upper[i], best)

    h_max = min(d[i] + nearest_upper[i] for i in range(n))
    print(total - n * h_max)

if __name__ == "__main__":
    main()