import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    K = int(data[0])
    S = data[1]
    T = data[2]
    n = len(S)
    m = len(T)

    if abs(n - m) > K:
        sys.stdout.write("No\n")
        return

    if n > m:
        S, T = T, S
        n, m = m, n

    if K >= m:
        sys.stdout.write("Yes\n")
        return

    BLOCK = 4096

    def lce(x, y, s=S, t=T, n=n, m=m, BLOCK=BLOCK):
        while x < n and y < m:
            if s[x] != t[y]:
                break
            bl = BLOCK
            rs = n - x
            if rs < bl:
                bl = rs
            rt = m - y
            if rt < bl:
                bl = rt
            if bl == 1:
                x += 1
                y += 1
                continue
            if s[x:x + bl] == t[y:y + bl]:
                x += bl
                y += bl
            else:
                # The first character is known to match.
                x += 1
                y += 1
                bl -= 1
                while bl and s[x] == t[y]:
                    x += 1
                    y += 1
                    bl -= 1
                if bl == 0:
                    continue
                break
        return x

    off = K
    size = 2 * K + 1
    V = [-1] * size

    x = lce(0, 0)
    V[off] = x
    if x == n and x == m:
        sys.stdout.write("Yes\n")
        return

    for e in range(1, K + 1):
        curr = V[:]
        for d in range(-e, e + 1):
            idx = d + off
            old = V[idx]
            best = old

            # Delete one character from S: previous diagonal d-1.
            if d > -K:
                v = V[idx - 1]
                if v >= 0:
                    x0 = v + 1
                    if x0 <= n and x0 > best:
                        y0 = x0 - d
                        if 0 <= y0 <= m:
                            best = x0

            # Insert one character into S (consume T): previous diagonal d+1.
            if d < K:
                v = V[idx + 1]
                if v >= 0:
                    x0 = v
                    if x0 <= n and x0 > best:
                        y0 = x0 - d
                        if 0 <= y0 <= m:
                            best = x0

            # Substitute: same diagonal.
            if old >= 0:
                x0 = old + 1
                if x0 <= n and x0 > best:
                    y0 = x0 - d
                    if 0 <= y0 <= m:
                        best = x0

            if best > old:
                y = best - d
                if 0 <= y <= m:
                    if best == n or y == m:
                        x = best
                    else:
                        x = lce(best, y)
                    curr[idx] = x
                    if x == n and x - d == m:
                        sys.stdout.write("Yes\n")
                        return
        V = curr

    sys.stdout.write("No\n")

if __name__ == "__main__":
    solve()