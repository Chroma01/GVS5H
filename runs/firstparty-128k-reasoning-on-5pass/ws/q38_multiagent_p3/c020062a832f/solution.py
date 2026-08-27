import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m = data[0], data[1]
    a = data[2:2 + n]

    # Inversion count for k = 0 using a Fenwick tree over values 0..m-1.
    bit = [0] * (m + 1)
    inv = 0

    for i, x in enumerate(a):
        j = x + 1
        s = 0
        while j:
            s += bit[j]
            j &= j - 1
        inv += i - s

        j = x + 1
        while j <= m:
            bit[j] += 1
            j += j & -j

    # delta[p] = change in inversion count when original value p wraps
    # from M-1 to 0.
    # For each occurrence of p:
    #   + number of earlier non-p elements
    #   - number of later non-p elements
    delta = [0] * m

    cnt = [0] * m
    total = 0
    for x in a:
        delta[x] += total - cnt[x]
        cnt[x] += 1
        total += 1

    cnt = [0] * m
    total = 0
    for x in reversed(a):
        delta[x] -= total - cnt[x]
        cnt[x] += 1
        total += 1

    ans = inv
    out = [str(ans)]

    # Transition k -> k+1 wraps original value p = M-1-k.
    # For outputs k = 1..M-1, add delta[M-1], delta[M-2], ..., delta[1].
    for p in range(m - 1, 0, -1):
        ans += delta[p]
        out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()