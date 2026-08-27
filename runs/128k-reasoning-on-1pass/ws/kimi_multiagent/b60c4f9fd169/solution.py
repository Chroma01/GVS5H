import sys

def main():
    data = sys.stdin.buffer.read().split()
    K = int(data[0])
    S = data[1]
    T = data[2]
    n, m = len(S), len(T)
    write = sys.stdout.write

    # Necessary condition: each insert/delete changes length by 1
    if n - m > K or m - n > K:
        write("No\n")
        return

    NEG = -10**9
    off = K + 1
    size = 2 * K + 3
    target = n - m  # diagonal of the goal cell (n, m)

    def lcp(i, j):
        # length of longest common prefix of S[i:] and T[j:], via
        # exponential + binary search on C-speed bytes comparisons
        maxl = n - i
        r = m - j
        if r < maxl:
            maxl = r
        length = 0
        step = 1
        while length + step <= maxl and S[i + length:i + length + step] == T[j + length:j + length + step]:
            length += step
            step += step
        step >>= 1
        while step:
            if length + step <= maxl and S[i + length:i + length + step] == T[j + length:j + length + step]:
                length += step
            step >>= 1
        return length

    # Furthest-reach (Landau-Vishkin/Myers style) DP over diagonals.
    # prev[off + k] = max i such that S[:i] -> T[:i-k] costs <= d.
    prev = [NEG] * size
    prev[off] = lcp(0, 0)
    if target == 0 and prev[off] >= n:
        write("Yes\n")
        return

    for d in range(1, K + 1):
        cur = [NEG] * size
        for k in range(-d, d + 1):
            ok = off + k
            best = NEG
            # substitution: stay on diagonal k, advance both
            v = prev[ok] + 1
            if v > best and v <= n and v - k <= m:
                best = v
            # deletion: come from diagonal k-1, advance i only
            v = prev[ok - 1] + 1
            if v > best and v <= n:
                best = v
            # insertion: come from diagonal k+1, advance j only
            v = prev[ok + 1]
            if v > best and v - k <= m:
                best = v
            if best < 0:
                continue
            i = best
            j = i - k
            # free matches ("snake")
            if i < n and j < m:
                i += lcp(i, j)
            cur[ok] = i
        if cur[off + target] >= n:
            write("Yes\n")
            return
        prev = cur

    write("No\n")

main()