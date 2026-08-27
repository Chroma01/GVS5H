import sys
from array import array

MOD = 998244353

def solve_case(h, w, grid):
    m = h * w
    n = 2 * m

    # parent[x] < 0 means root, with -parent[x] as component size.
    parent = array('i', [-1]) * n
    parity = bytearray(n)  # parity[x] = x XOR parent[x]
    components = n

    def find(x):
        r = x
        total = 0
        while parent[r] >= 0:
            total ^= parity[r]
            r = parent[r]

        # Path compression. At each point total is current node XOR root.
        cur = x
        cur_parity = total
        while cur != r:
            nxt = parent[cur]
            edge_parity = parity[cur]
            parent[cur] = r
            parity[cur] = cur_parity
            cur_parity ^= edge_parity
            cur = nxt

        return r, total

    def unite(x, y, value):
        nonlocal components

        rx, px = find(x)
        ry, py = find(y)

        if rx == ry:
            return (px ^ py) == value

        # x XOR y = value
        # Therefore root_x XOR root_y = px XOR py XOR value.
        root_parity = px ^ py ^ value

        if parent[rx] > parent[ry]:
            rx, ry = ry, rx

        parent[rx] += parent[ry]
        parent[ry] = rx
        parity[ry] = root_parity
        components -= 1
        return True

    for i in range(h):
        row = grid[i]
        base = i * w
        top_base = (i - 1 if i else h - 1) * w

        for j, ch in enumerate(row):
            cur = base + j

            right = cur
            left = base + (j - 1 if j else w - 1)
            bottom = m + cur
            top = m + top_base + j

            if ch == 65:  # 'A'
                if not unite(left, right, 1) or not unite(top, bottom, 1):
                    return 0
            else:  # 'B'
                if (not unite(left, right, 0) or
                    not unite(top, bottom, 0) or
                    not unite(left, top, 1)):
                    return 0

    return pow(2, components, MOD)


def main():
    input = sys.stdin.buffer.readline
    t = int(input())
    ans = []

    for _ in range(t):
        h, w = map(int, input().split())
        grid = [input().strip() for _ in range(h)]
        ans.append(str(solve_case(h, w, grid)))

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()