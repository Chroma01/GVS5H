import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    pos = 0
    N = int(data[pos]); pos += 1
    M = int(data[pos]); pos += 1

    adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        u = int(data[pos]); v = int(data[pos + 1]); pos += 2
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * (N + 1)

    Esum = 0   # sum over even-size components of (colour-class size mod 2)
    o = 0      # number of odd-size components
    B = 0      # number of odd-size components with size >= 3
    Ce = 0     # number of even-size components
    D = 0      # sum over all components of d = a*b - e

    for s in range(1, N + 1):
        if color[s] != -1:
            continue
        color[s] = 0
        stack = [s]
        c0 = 0
        c1 = 0
        deg = 0
        while stack:
            u = stack.pop()
            if color[u] == 0:
                c0 += 1
            else:
                c1 += 1
            deg += len(adj[u])
            cu = color[u]
            for w in adj[u]:
                if color[w] == -1:
                    color[w] = cu ^ 1
                    stack.append(w)

        size = c0 + c1
        e = deg // 2
        D += c0 * c1 - e
        if size & 1:
            o += 1
            if size >= 3:
                B += 1
        else:
            Ce += 1
            Esum += (c0 & 1)

    if N & 1:
        aoki = (M & 1) == 1
    else:
        if B == 0:
            aoki = ((Esum + M + (o // 2)) & 1) == 1
        elif B <= 2:
            aoki = True
        else:
            aoki = (((o // 2) + D + Ce) & 1) == 1

    sys.stdout.write("Aoki\n" if aoki else "Takahashi\n")

main()