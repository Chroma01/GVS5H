import sys

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    a = data[1:1+n]
    max_sum = 2 * max(a)
    ans = 0
    for v in range(max_sum.bit_length()):
        h = 1 << v
        m = h << 1
        mask = m - 1
        d = {}
        get = d.get
        for x in a:
            r = x & mask
            p = get(r)
            if p is None:
                d[r] = [1, x]
                # get remains bound to d.get, okay after insertion? d.get method still valid.
            else:
                p[0] += 1
                p[1] += x
        sv = 0
        for r, p in d.items():
            c = (h - r) & mask
            if r < c:
                q = d.get(c)
                if q is not None:
                    sv += p[0] * q[1] + q[0] * p[1]
            elif r == c:
                sv += (p[0] + 1) * p[1]
        ans += sv // h
    print(ans)

if __name__ == "__main__":
    solve()