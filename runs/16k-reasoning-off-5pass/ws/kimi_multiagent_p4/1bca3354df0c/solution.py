import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    adj = [[] for _ in range(N + 1)]
    for _ in range(M):
        u = int(data[idx]); v = int(data[idx + 1]); idx += 2
        adj[u].append(v)
        adj[v].append(u)

    color = [-1] * (N + 1)
    total = 0          # S = sum over components of (a*b - m_c)
    odd_comp = 0       # number of components with odd size
    for s in range(1, N + 1):
        if color[s] != -1:
            continue
        color[s] = 0
        q = deque([s])
        a = b = 0
        m_c = 0
        while q:
            u = q.popleft()
            if color[u] == 0:
                a += 1
            else:
                b += 1
            m_c += len(adj[u])
            for w in adj[u]:
                if color[w] == -1:
                    color[w] = color[u] ^ 1
                    q.append(w)
        m_c //= 2
        total += a * b - m_c
        if (a + b) & 1:
            odd_comp += 1

    # Game analysis (see NOTES):
    #   The game always ends at a single complete bipartite graph K_{A,B},
    #   so the total number of moves is T = A*B - M.
    #   * N odd : A*B is always even  ->  T ≡ M (mod 2).
    #   * N even: T ≡ N/2 + D/2 + M (mod 2), D = |sum ±(a_i - b_i)|.
    #     - no odd-sized component: D/2 is forced and T ≡ S (mod 2).
    #     - odd-sized components exist: the parity of D/2 is a free bit
    #       seized by the first player, except when every component is an
    #       isolated vertex and N/2 is even (second player pairs up).
    if N & 1:
        win = (M & 1) == 1
    else:
        if odd_comp == 0:
            win = (total & 1) == 1
        else:
            if M == 0 and (N // 2) % 2 == 0:
                win = False
            else:
                win = (total & 1) == 0
    sys.stdout.write("Aoki\n" if win else "Takahashi\n")

main()