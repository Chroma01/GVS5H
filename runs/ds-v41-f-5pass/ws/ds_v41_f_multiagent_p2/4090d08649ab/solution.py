import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    a = data[1:1 + n]

    # last[v] = most recent position where value v occurred before current R
    last = [0] * (n + 2)

    total = 0   # sum_{L=1..R} f(L, R)
    ans = 0

    for r, x in enumerate(a, start=1):
        px = last[x]

        # For L in [px+1, R], value x is newly present: +1 each.
        total += r - px

        # If a neighbour is present in A[L..R-1], x joins it and cancels one run.
        if x > 1:
            py = last[x - 1]
            if py > px:
                total -= py - px

        if x < n:
            py = last[x + 1]
            if py > px:
                total -= py - px

        ans += total
        last[x] = r

    sys.stdout.write(str(ans))


if __name__ == "__main__":
    main()