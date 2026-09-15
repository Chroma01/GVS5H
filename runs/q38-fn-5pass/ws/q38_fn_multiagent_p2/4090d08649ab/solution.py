import sys


def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n = data[0]
    occ = [[] for _ in range(n + 2)]

    for i in range(1, n + 1):
        occ[data[i]].append(i)
    del data

    total = n * (n + 1) // 2

    # avoid[v] = number of subarrays that do NOT contain value v
    avoid = [0] * (n + 2)
    single_sum = 0

    for v in range(1, n + 1):
        lst = occ[v]
        if not lst:
            av = total
        else:
            prev = 0
            s = 0
            for p in lst:
                g = p - prev - 1
                s += g * (g + 1) // 2
                prev = p
            g = n - prev
            s += g * (g + 1) // 2
            av = s

        avoid[v] = av
        single_sum += total - av

    pair_sum = 0

    for x in range(1, n):
        lx = occ[x]
        ly = occ[x + 1]

        # If either value never appears, no subarray contains both.
        if not lx or not ly:
            continue

        # Count subarrays avoiding both x and x+1 by merging their occurrence lists.
        i = j = 0
        lenx = len(lx)
        leny = len(ly)
        prev = 0
        s = 0

        while i < lenx and j < leny:
            if lx[i] < ly[j]:
                p = lx[i]
                i += 1
            else:
                p = ly[j]
                j += 1

            g = p - prev - 1
            s += g * (g + 1) // 2
            prev = p

        while i < lenx:
            p = lx[i]
            i += 1
            g = p - prev - 1
            s += g * (g + 1) // 2
            prev = p

        while j < leny:
            p = ly[j]
            j += 1
            g = p - prev - 1
            s += g * (g + 1) // 2
            prev = p

        g = n - prev
        s += g * (g + 1) // 2

        avoid_both = s
        pair_sum += total - avoid[x] - avoid[x + 1] + avoid_both

    ans = single_sum - pair_sum
    sys.stdout.write(str(ans) + "\n")


if __name__ == "__main__":
    solve()