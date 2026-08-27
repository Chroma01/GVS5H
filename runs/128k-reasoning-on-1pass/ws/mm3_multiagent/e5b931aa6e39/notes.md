
## ideation
```python
import sys
import math

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])

    ans = None
    d = 1
    # Only d = x - y with d^3 < N needs to be examined.
    while d * d * d <= N:
        if N % d == 0:
            M = N // d                     # M = x^2 + x*y + y^2
            delta = 12 * M - 3 * d * d     # discriminant of the quadratic in y
            if delta >= 0:
                s = math.isqrt(delta)
                if s * s == delta:
                    num = s - 3 * d         # numerator of y
                    if num > 0 and num % 6 == 0:
                        y = num // 6
                        x = y + d
                        if x**3 - y**3 == N:
                            ans = (x, y)
                            break
        d += 1

    if ans:
        print(ans[0], ans[1])
    else:
        print(-1)

if __name__ == "__main__":
    solve()
```
