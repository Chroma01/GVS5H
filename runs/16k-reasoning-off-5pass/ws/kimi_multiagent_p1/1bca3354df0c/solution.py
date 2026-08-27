import sys
sys.setrecursionlimit(1 << 25)

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1

    adj = [[] for _ in range(N)]
    for _ in range(M):
        u = int(data[idx]) - 1; idx += 1
        v = int(data[idx]) - 1; idx += 1
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * N
    O = 0          # number of odd-sized components
    E = 0          # number of even-sized components
    F = 0          # sum over components of a*b, minus M at the end
    sum_a = 0      # sum of one side per component (for the O == 0 fixed-parity case)

    for s in range(N):
        if color[s] != -1:
            continue
        color[s] = 0
        stack = [s]
        cnt = [1, 0]
        while stack:
            u = stack.pop()
            for w in adj[u]:
                if color[w] == -1:
                    color[w] = color[u] ^ 1
                    cnt[color[w]] += 1
                    stack.append(w)
        a, b = cnt[0], cnt[1]
        F += a * b
        sum_a += a
        if (a + b) & 1:
            O += 1
        else:
            E += 1

    F -= M

    if N & 1:
        # A+B = N odd => A*B always even => total moves parity = parity of M.
        aoki = (M & 1) == 1
    elif O == 0:
        # All component sizes even => every d_i even => sign choices change D by
        # multiples of 4 => A*B parity fixed. Compute it with any alignment.
        aoki = ((sum_a * (N - sum_a) - M) & 1) == 1
    elif O == 2:
        # First player immediately performs the last parity-deciding merge
        # (merges the two odd components, choosing the alignment that makes the
        # total number of moves odd) and wins.
        aoki = True
    else:
        # O >= 4. The last odd-involving merge is decisive (its maker chooses the
        # parity of the total move count and wins). In the race for it, every
        # safe move (fill, even-even merge, odd-even merge, odd-odd merge from
        # O >= 6) changes E + F by an odd amount or leaves its parity under the
        # mover's control, and the player first forced to move at O = 4 with
        # E + F even loses. Hence: losing iff E + F is even.
        aoki = ((E + F) & 1) == 1

    sys.stdout.write("Aoki\n" if aoki else "Takahashi\n")

main()