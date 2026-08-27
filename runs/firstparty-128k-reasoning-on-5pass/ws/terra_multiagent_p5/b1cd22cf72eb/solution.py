import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    x = data[1]

    u = [0] * n
    d = [0] * n
    total = 0

    p = 2
    for i in range(n):
        u[i] = data[p]
        d[i] = data[p + 1]
        total += u[i] + d[i]
        p += 2

    left_min = [0] * n
    best = 10**30
    for i in range(n):
        best = min(u[i], best + x)
        left_min[i] = best

    best = 10**30
    h_max = 10**30
    for i in range(n - 1, -1, -1):
        best = min(u[i], best + x)
        reachable_upper = min(left_min[i], best)
        h_max = min(h_max, d[i] + reachable_upper)

    print(total - n * h_max)

if __name__ == "__main__":
    main()