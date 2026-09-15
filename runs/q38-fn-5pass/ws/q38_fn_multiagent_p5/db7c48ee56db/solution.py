import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, k = data[0], data[1]
    a = data[2:]

    total = 0
    for v in a:
        total ^= v

    # Complement symmetry:
    # XOR(chosen K) = total_xor XOR XOR(excluded N-K).
    if k <= n - k:
        r = k
        mask = 0
    else:
        r = n - k
        mask = total

    if r == 0:
        print(total)
        return

    if r == 1:
        if mask == 0:
            print(max(a))
        else:
            ans = 0
            for v in a:
                val = total ^ v
                if val > ans:
                    ans = val
            print(ans)
        return

    # Enumerate r-combinations of indices in lexicographic order.
    # Maintain the current XOR incrementally.
    idx = list(range(r))
    x = 0
    for i in range(r):
        x ^= a[i]

    ans = x ^ mask
    limits = list(range(n - r, n))

    arr = a
    lim = limits
    rr = r
    m = mask

    while True:
        i = rr - 1
        while i >= 0 and idx[i] == lim[i]:
            i -= 1
        if i < 0:
            break

        old = idx[i]
        new = old + 1
        idx[i] = new
        x ^= arr[old] ^ arr[new]

        j = i + 1
        newj = new + 1
        while j < rr:
            oldj = idx[j]
            if oldj != newj:
                x ^= arr[oldj] ^ arr[newj]
            idx[j] = newj
            j += 1
            newj += 1

        val = x ^ m
        if val > ans:
            ans = val

    print(ans)


if __name__ == "__main__":
    solve()