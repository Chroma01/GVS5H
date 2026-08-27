```python
import sys

def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    N, M, A, B = data[:4]
    L = [0] * M
    R = [0] * M
    p = 4
    for i in range(M):
        L[i] = data[p]
        R[i] = data[p + 1]
        p += 2

    # Fixed step length case.
    if A == B:
        d = A
        if (N - 1) % d != 0:
            print("No")
            return
        r = 1 % d
        for i in range(M):
            first = L[i] + ((r - L[i]) % d)
            if first <= R[i]:
                print("No")
                return
        print("Yes")
        return

    # A < B. A bad interval of length >= B can never be jumped over.
    for i in range(M):
        if R[i] - L[i] + 1 >= B:
            print("No")
            return

    diff = B - A
    # For steps A..B, every offset >= T is representable in an open good region.
    k0 = (A - 1 + diff - 1) // diff
    T = A * k0
    C = T + 2 * B  # long good gaps longer than this are saturated

    bad = bytearray(1)  # 1-based; index 0 dummy
    prev = 1
    for i in range(M):
        glen = L[i] - prev
        if glen > 0:
            bad.extend(b"\x00" * (glen if glen <= C else C))
        bad.extend(b"\x01" * (R[i] - L[i] + 1))
        prev = R[i] + 1

    final_long = False
    final_start = -1
    glen = N - prev + 1
    if glen > C:
        final_long = True
        final_start = len(bad)  # next 1-based index
        bad.extend(b"\x00" * C)
    else:
        bad.extend(b"\x00" * glen)

    n = len(bad) - 1
    f = bytearray(n + 1)
    f[1] = 1

    cnt = 0  # number of reachable squares in window [x-B, x-A]
    for x in range(2, n + 1):
        add = x - A
        if add >= 1 and f[add]:
            cnt += 1
        rem = x - B - 1
        if rem >= 1 and f[rem]:
            cnt -= 1
        if not bad[x] and cnt > 0:
            f[x] = 1

    if final_long:
        ok = any(f[final_start:])
    else:
        ok = bool(f[n])

    print("Yes" if ok else "No")

main()
```