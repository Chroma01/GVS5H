import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    m = int(next(it))

    adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u = int(next(it)); v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    # N odd: S(N-S) is always even, total move parity == M parity.
    if n % 2 == 1:
        sys.stdout.write("Aoki\n" if m % 2 == 1 else "Takahashi\n")
        return

    # N even
    color = [-1] * (n + 1)
    visited = bytearray(n + 1)

    k = 0          # number of odd-size components
    c = 0          # number of even-size components
    S = 0          # sum over even components of (color-class size mod 2)  == #P components
    I = 0          # sum over components of (a*b - e)

    for s in range(1, n + 1):
        if visited[s]:
            continue
        visited[s] = 1
        color[s] = 0
        stack = [s]
        a = 0
        b = 0
        e = 0
        while stack:
            x = stack.pop()
            if color[x] == 0:
                a += 1
            else:
                b += 1
            for y in adj[x]:
                e += 1
                if not visited[y]:
                    visited[y] = 1
                    color[y] = 1 - color[x]
                    stack.append(y)
        e //= 2
        size = a + b
        if size & 1:
            k += 1
        else:
            c += 1
            S += a & 1
        I += a * b - e

    if k == 0:
        res = "Aoki" if (S + m) % 2 == 1 else "Takahashi"
    elif k == 2:
        res = "Aoki"
    elif c > 0:
        res = "Aoki"
    else:  # k >= 4 and c == 0
        res = "Aoki" if I % 2 == 1 else "Takahashi"

    sys.stdout.write(res + "\n")

main()