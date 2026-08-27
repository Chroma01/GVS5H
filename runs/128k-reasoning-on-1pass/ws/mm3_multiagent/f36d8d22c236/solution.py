import sys

def solve() -> None:
    input = sys.stdin.readline
    N_line = input()
    if not N_line:
        return
    N = int(N_line)
    S = input().strip()
    T = input().strip()

    # target[a] = letter that a has to become (only for a in S)
    target = [-1] * 26
    for i in range(N):
        a = ord(S[i]) - 97
        b = ord(T[i]) - 97
        if target[a] == -1:
            target[a] = b
        elif target[a] != b:
            print(-1)
            return

    # letters that appear in S
    inS = [False] * 26
    for ch in S:
        inS[ord(ch) - 97] = True

    # letters that appear in S or in T
    inL = [False] * 26
    for ch in S:
        inL[ord(ch) - 97] = True
    for ch in T:
        inL[ord(ch) - 97] = True

    U_size = sum(inS)                 # |U|
    f = 0
    for a in range(26):
        if inS[a] and target[a] == a:
            f += 1                    # fixed points

    # count cycles of length >= 2
    visited = [False] * 26
    C = 0
    for start in range(26):
        if not inS[start] or visited[start]:
            continue
        path = []
        pos = {}
        cur = start
        while True:
            if not inS[cur]:                 # reached a sink
                for v in path:
                    visited[v] = True
                break
            if visited[cur]:
                for v in path:
                    visited[v] = True
                break
            if cur in pos:                    # found a cycle
                idx = pos[cur]
                cycle_len = len(path) - idx
                if cycle_len >= 2:
                    C += 1
                for v in path:
                    visited[v] = True
                break
            pos[cur] = len(path)
            path.append(cur)
            cur = target[cur]
        # loop always breaks inside, no extra handling needed

    L_size = sum(inL)                 # |L|
    free = 26 - L_size
    extra = max(0, C - free)
    ans = U_size - f + C + extra
    print(ans)


if __name__ == "__main__":
    solve()