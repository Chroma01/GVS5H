import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    s = data[1].decode()
    t = data[2].decode()

    A = 26
    # mapping[x] = required target of letter x, or -1 if unconstrained
    mapping = [-1] * A
    for sc, tc in zip(s, t):
        a = ord(sc) - 97
        b = ord(tc) - 97
        if mapping[a] == -1:
            mapping[a] = b
        elif mapping[a] != b:
            print(-1)
            return

    # Count non-self edges
    edges = 0
    for a in range(A):
        if mapping[a] != -1 and mapping[a] != a:
            edges += 1

    # Detect directed cycles in the functional graph (out-degree <= 1)
    visited = [0] * A  # 0 = unvisited, 1 = in current path, 2 = done
    cycles = 0
    cycle_nodes_total = 0
    for start in range(A):
        if visited[start] != 0:
            continue
        if mapping[start] == -1 or mapping[start] == start:
            visited[start] = 2
            continue
        path = []
        node = start
        while (node != -1 and visited[node] == 0
               and mapping[node] != -1 and mapping[node] != node):
            visited[node] = 1
            path.append(node)
            node = mapping[node]
        if node != -1 and visited[node] == 1:
            idx = path.index(node)
            cycles += 1
            cycle_nodes_total += len(path) - idx
        for nd in path:
            visited[nd] = 2

    # A cycle needs a buffer letter not on any cycle.
    # Chain letters can be processed first to free them, so the only
    # impossible case is when every one of the 26 letters lies on a cycle.
    if cycles > 0 and cycle_nodes_total == A:
        print(-1)
        return

    print(edges + cycles)

main()