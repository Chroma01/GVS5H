import sys

def main():
    input = sys.stdin.readline
    N = int(input())
    S = input().strip()
    T = input().strip()

    A = 26
    UNSET = -1
    f = [UNSET] * A          # required target for each letter of S
    appears = [False] * A    # letter appears in S

    for i in range(N):
        s = ord(S[i]) - 97
        t = ord(T[i]) - 97
        appears[s] = True
        if f[s] == UNSET:
            f[s] = t
        elif f[s] != t:
            # one source letter must become two different targets: impossible
            print(-1)
            return

    # Unconstrained letters (absent from S) are fixed points
    for c in range(A):
        if f[c] == UNSET:
            f[c] = c

    # Base cost: every letter of S that must change is renamed exactly once.
    # Acyclic parts are always feasible by renaming from the sink backwards.
    ans = 0
    for c in range(A):
        if appears[c] and f[c] != c:
            ans += 1

    # Detect non-trivial cycles in the functional graph.
    # Edges only arise from letters of S, so every cycle letter appears in S.
    state = [0] * A  # 0 = unvisited, 1 = on current path, 2 = done
    nontrivial_cycles = 0
    for start in range(A):
        if state[start] != 0:
            continue
        path = []
        cur = start
        while state[cur] == 0:
            state[cur] = 1
            path.append(cur)
            cur = f[cur]
        if state[cur] == 1:
            # nodes from cur onward in path form a cycle
            idx = path.index(cur)
            cyc = path[idx:]
            if len(cyc) > 1:
                nontrivial_cycles += 1
        for node in path:
            state[node] = 2

    if nontrivial_cycles:
        # Each non-trivial cycle needs one extra rotation operation using a
        # buffer letter that does not appear in S. One absent letter can
        # buffer all cycles sequentially (it ends empty after each rotation).
        # If all 26 letters appear in S, no buffer exists -> impossible.
        if all(appears):
            print(-1)
            return
        ans += nontrivial_cycles

    print(ans)

main()