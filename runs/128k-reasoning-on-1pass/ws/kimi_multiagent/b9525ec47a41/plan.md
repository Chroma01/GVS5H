```python
import sys

MOD = 998244353

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = data[1].decode()

    # Product matrix [[a,b],[c,d]], start with identity.
    a, b, c, d = 1, 0, 0, 1

    for ch in s:
        if ch == '0':
            e, f, g, h = 2, 0, 1, 1
        else:
            e, f, g, h = 3, 1, 1, 1

        # [[a,b],[c,d]] *= [[e,f],[g,h]]
        na = (a * e + b * g) % MOD
        nb = (a * f + b * h) % MOD
        nc = (c * e + d * g) % MOD
        nd = (c * f + d * h) % MOD
        a, b, c, d = na, nb, nc, nd

    ans = (a + d - 2) % MOD
    print(ans)

main()
```