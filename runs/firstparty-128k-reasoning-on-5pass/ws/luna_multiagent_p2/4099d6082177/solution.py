import sys


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n_groups, k = data[0], data[1]
    v_count = n_groups * k

    graph = [[] for _ in range(v_count + 1)]
    pos = 2
    for _ in range(v_count - 1):
        u = data[pos]
        v = data[pos + 1]
        pos += 2
        graph[u].append(v)
        graph[v].append(u)

    parent = [0] * (v_count + 1)
    order = []
    stack = [1]
    parent[1] = -1

    while stack:
        v = stack.pop()
        order.append(v)
        for to in graph[v]:
            if to != parent[v]:
                parent[to] = v
                stack.append(to)

    # state[v]:
    #   -1 = impossible
    #    0 = subtree fully decomposed
    #   >0 = one unfinished path ending at v, with this many vertices
    state = [0] * (v_count + 1)

    for v in reversed(order):
        active_count = 0
        first_length = 0
        second_length = 0

        for to in graph[v]:
            if to == parent[v]:
                continue

            child_state = state[to]
            if child_state == -1:
                state[v] = -1
                break

            if child_state > 0:
                active_count += 1
                if active_count == 1:
                    first_length = child_state
                elif active_count == 2:
                    second_length = child_state
                else:
                    state[v] = -1
                    break
        else:
            if active_count == 0:
                if k == 1:
                    state[v] = 0
                else:
                    state[v] = 1
            elif active_count == 1:
                length = first_length + 1
                if length > k:
                    state[v] = -1
                elif length == k:
                    state[v] = 0
                else:
                    state[v] = length
            else:
                if first_length + second_length + 1 == k:
                    state[v] = 0
                else:
                    state[v] = -1

    print("Yes" if state[1] == 0 else "No")


if __name__ == "__main__":
    solve()