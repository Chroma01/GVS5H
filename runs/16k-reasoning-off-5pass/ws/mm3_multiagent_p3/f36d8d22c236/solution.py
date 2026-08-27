import sys
sys.setrecursionlimit(1 << 25)

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    S = data[1].strip()
    T = data[2].strip()
    # 0..25
    target = [-1] * 26
    has_self = [False] * 26
    for i in range(N):
        a = ord(S[i]) - 97
        b = ord(T[i]) - 97
        if a == b:
            has_self[a] = True
        else:
            if has_self[a]:
                print(-1)
                return
            if target[a] == -1:
                target[a] = b
            elif target[a] != b:
                print(-1)
                return
    # build graph: edge from a to target[a] if target[a] != -1
    # detect cycle
    # Since out-degree <= 1, we can use DFS with states
    state = [0] * 26  # 0=unvisited, 1=visiting, 2=visited
    def dfs(u):
        if state[u] == 1:
            return True  # cycle
        if state[u] == 2:
            return False
        state[u] = 1
        v = target[u]
        if v != -1:
            if dfs(v):
                return True
        state[u] = 2
        return False
    for i in range(26):
        if dfs(i):
            print(-1)
            return
    # count edges
    edges = sum(1 for x in target if x != -1)
    print(edges)

if __name__ == "__main__":
    solve()