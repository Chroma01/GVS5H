import sys
from array import array

MOD = 998244353

def solve_case(H, W, rows):
    m = H * W
    n = 2 * m

    # 0..m-1: horizontal seams x[i][j], from (i,j) right to (i,j+1) left
    # m..2m-1: vertical seams y[i][j], from (i,j) bottom to (i+1,j) top
    parent = array('i', range(n))
    parity = bytearray(n)   # XOR value from a node to its parent
    rank = bytearray(n)
    components = n

    def find(x):
        start = x
        total = 0
        while parent[x] != x:
            total ^= parity[x]
            x = parent[x]
        root = x

        x = start
        remaining = total
        while parent[x] != x:
            nxt = parent[x]
            edge = parity[x]
            parent[x] = root
            parity[x] = remaining
            remaining ^= edge
            x = nxt

        return root, total

    def unite(a, b, required):
        nonlocal components
        ra, xa = find(a)
        rb, xb = find(b)

        if ra == rb:
            return (xa ^ xb) == required

        # parity from either root to the other must be xa xor xb xor required.
        link_parity = xa ^ xb ^ required

        if rank[ra] < rank[rb]:
            parent[ra] = rb
            parity[ra] = link_parity
        else:
            parent[rb] = ra
            parity[rb] = link_parity
            if rank[ra] == rank[rb]:
                rank[ra] += 1

        components -= 1
        return True

    for i in range(H):
        base = i * W
        prev_base = ((i - 1) % H) * W
        for j in range(W):
            cell = base + j

            # For cell (i,j):
            # left = x[i][j-1], right = x[i][j]
            # top = y[i-1][j], bottom = y[i][j]
            left = base + (j - 1 if j else W - 1)
            right = cell
            top = m + prev_base + j
            bottom = m + cell

            if rows[i][j] == 65:  # 'A'
                # Exactly one horizontal and one vertical edge are used.
                if not unite(left, right, 1):
                    return 0
                if not unite(top, bottom, 1):
                    return 0
            else:  # 'B'
                # Horizontal pair or vertical pair.
                if not unite(left, right, 0):
                    return 0
                if not unite(top, bottom, 0):
                    return 0
                if not unite(left, top, 1):
                    return 0

    return pow(2, components, MOD)


def main():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    T = int(next(it))
    ans = []

    for _ in range(T):
        H = int(next(it))
        W = int(next(it))
        rows = [next(it) for _ in range(H)]
        ans.append(str(solve_case(H, W, rows)))

    print("\n".join(ans))


if __name__ == "__main__":
    main()