import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    S = data[1].strip()
    T = data[2].strip()

    # f[a] = required target of letter a, or -1 if unconstrained
    f = [-1] * 26
    in_S = [False] * 26

    for i in range(n):
        a = ord(S[i]) - 97
        b = ord(T[i]) - 97
        in_S[a] = True
        if f[a] == -1:
            f[a] = b
        elif f[a] != b:
            print(-1)
            return

    # Nontrivial edges: a -> f[a] with f[a] != a
    # Functional graph on at most 26 nodes; find cycles via color marking.
    # state: 0 = unvisited, 1 = in current stack, 2 = done
    state = [0] * 26
    on_cycle = [False] * 26

    nodes = [a for a in range(26) if f[a] != -1 and f[a] != a]
    edges = len(nodes)
    cycles = 0

    for start in nodes:
        if state[start] != 0:
            continue
        # walk the chain, recording path
        path = []
        cur = start
        while cur != -1 and state[cur] == 0 and f[cur] != -1 and f[cur] != cur:
            state[cur] = 1
            path.append(cur)
            cur = f[cur]
        # check termination reason: stopped on a node currently in the stack -> cycle
        if cur != -1 and f[cur] != -1 and f[cur] != cur and state[cur] == 1:
            idx = path.index(cur)
            for node in path[idx:]:
                on_cycle[node] = True
            cycles += 1
        for node in path:
            state[node] = 2

    if cycles > 0:
        # need a buffer letter: a letter not appearing in S,
        # or a letter with a nontrivial edge that is not on a cycle
        # (tree nodes can be freed by processing their edge after all
        #  edges pointing into them, after which they vanish from the string)
        buffer = False
        for a in range(26):
            if not in_S[a]:
                buffer = True
                break
        if not buffer:
            for a in nodes:
                if not on_cycle[a]:
                    buffer = True
                    break
        if not buffer:
            print(-1)
            return

    print(edges + cycles)

main()