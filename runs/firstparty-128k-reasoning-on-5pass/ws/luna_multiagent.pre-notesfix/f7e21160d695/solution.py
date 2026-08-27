import sys


def read_k_values(k):
    values = []
    while len(values) < k:
        values.extend(map(int, sys.stdin.buffer.readline().split()))
    return values


def main():
    input_stream = sys.stdin.buffer

    n, m, k = map(int, input_stream.readline().split())

    edges = []
    for _ in range(m):
        u, v, w = map(int, input_stream.readline().split())
        edges.append((w, u - 1, v - 1))
    edges.sort()

    a = read_k_values(k)
    b = read_k_values(k)

    diff = [0] * n
    for x in a:
        diff[x - 1] += 1
    for x in b:
        diff[x - 1] -= 1

    dsu_parent = list(range(n))
    dsu_size = [1] * n
    component_node = list(range(n))

    left = [-1] * n
    right = [-1] * n
    node_weight = [0] * n

    def find(x):
        while dsu_parent[x] != x:
            dsu_parent[x] = dsu_parent[dsu_parent[x]]
            x = dsu_parent[x]
        return x

    for w, u, v in edges:
        ru = find(u)
        rv = find(v)
        if ru == rv:
            continue

        if dsu_size[ru] < dsu_size[rv]:
            ru, rv = rv, ru

        new_node = len(left)
        left.append(component_node[ru])
        right.append(component_node[rv])
        node_weight.append(w)
        diff.append(0)

        dsu_parent[rv] = ru
        dsu_size[ru] += dsu_size[rv]
        component_node[ru] = new_node

    root = component_node[find(0)]

    order = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node)
        if left[node] != -1:
            stack.append(left[node])
            stack.append(right[node])

    answer = 0
    for node in reversed(order):
        if left[node] == -1:
            continue

        x = diff[left[node]]
        y = diff[right[node]]

        if x > 0 and y < 0:
            answer += min(x, -y) * node_weight[node]
        elif x < 0 and y > 0:
            answer += min(-x, y) * node_weight[node]

        diff[node] = x + y

    print(answer)


if __name__ == "__main__":
    main()