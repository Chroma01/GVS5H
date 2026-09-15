import sys


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, x = data[0], data[1]
    U = [0] * n
    D = [0] * n

    total = 0
    min_sum = 10**30
    p = 2

    for i in range(n):
        u = data[p]
        d = data[p + 1]
        p += 2
        U[i] = u
        D[i] = d
        s = u + d
        total += s
        if s < min_sum:
            min_sum = s

    U0 = U[0]
    D0 = D[0]
    rng = range(1, n)

    def feasible(h, U=U, D=D, x=x, rng=rng, U0=U0, D0=D0):
        # Reachable interval for the current upper tooth length.
        lo = h - D0
        if lo < 0:
            lo = 0
        hi = U0
        if hi > h:
            hi = h

        if lo > hi:
            return False

        for i in rng:
            # Values reachable from the previous interval within distance x.
            lo -= x
            hi += x

            # Intersect with the valid interval for this tooth.
            l = h - D[i]
            if l < 0:
                l = 0
            if l > lo:
                lo = l

            r = U[i]
            if r > h:
                r = h
            if r < hi:
                hi = r

            if lo > hi:
                return False

        return True

    low = 0
    high = min_sum

    while low < high:
        mid = (low + high + 1) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid - 1

    ans = total - n * low
    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    main()