import sys


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    s = data[1]
    t = data[2]

    # Required final destination of every source letter.
    required = [-1] * 26

    for sc, tc in zip(s, t):
        a = sc - 97
        b = tc - 97

        if required[a] == -1:
            required[a] = b
        elif required[a] != b:
            print(-1)
            return

    nxt = [-1] * 26
    indegree = [0] * 26
    edge_count = 0

    for a in range(26):
        b = required[a]
        if b != -1 and b != a:
            nxt[a] = b
            indegree[b] += 1
            edge_count += 1

    # Find directed cycles in this functional graph.  A cycle needs an
    # extra temporary operation only when it has no incoming tree edge,
    # i.e. every cycle vertex has indegree exactly one.
    visited = [False] * 26
    isolated_cycles = 0

    for start in range(26):
        if visited[start] or nxt[start] == -1:
            continue

        path = []
        position = {}
        cur = start

        while cur != -1 and not visited[cur] and cur not in position:
            position[cur] = len(path)
            path.append(cur)
            cur = nxt[cur]

        if cur != -1 and cur in position:
            cycle = path[position[cur]:]
            if all(indegree[v] == 1 for v in cycle):
                isolated_cycles += 1

        for v in path:
            visited[v] = True

    # If T uses all 26 letters, then S must also use all 26 letters.
    # Any actual rename would merge two currently present letters and
    # permanently reduce the number of distinct letters below 26.
    if edge_count > 0 and len(set(t)) == 26:
        print(-1)
        return

    print(edge_count + isolated_cycles)


if __name__ == "__main__":
    main()