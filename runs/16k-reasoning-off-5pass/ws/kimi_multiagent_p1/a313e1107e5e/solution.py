import sys
from bisect import bisect_left

def main():
    input = sys.stdin.readline
    N, Q = map(int, input().split())
    A = list(map(int, input().split()))
    queries = []
    xs = []
    for i in range(Q):
        R, X = map(int, input().split())
        queries.append((R, X, i))
        xs.append(X)

    # Coordinate compression of A and X
    all_vals = sorted(set(A + xs))
    comp = {v: i + 1 for i, v in enumerate(all_vals)}  # 1-based
    M = len(all_vals)

    # Compress A
    A_comp = [comp[a] for a in A]

    # Sort elements by value
    elements = sorted([(A[i], i + 1, A_comp[i]) for i in range(N)])  # (value, index, comp_value)

    # Sort queries by X
    queries.sort(key=lambda x: x[1])

    # Sparse 2D Fenwick tree: dictionary of dictionaries
    # bit[x][y] = max value in the rectangle [1..x] x [1..y]
    bit = [dict() for _ in range(N + 1)]

    def update(x, y, val):
        while x <= N:
            y_dict = bit[x]
            y0 = y
            while y0 <= M:
                if y0 in y_dict:
                    if y_dict[y0] < val:
                        y_dict[y0] = val
                else:
                    y_dict[y0] = val
                y0 += y0 & -y0
            x += x & -x

    def query(x, y):
        res = 0
        while x > 0:
            y_dict = bit[x]
            y0 = y
            while y0 > 0:
                if y0 in y_dict:
                    if y_dict[y0] > res:
                        res = y_dict[y0]
                y0 -= y0 & -y0
            x -= x & -x
        return res

    ans = [0] * Q
    ptr = 0
    for R, X, idx in queries:
        # Add all elements with value <= X
        while ptr < N and elements[ptr][0] <= X:
            val, pos, comp_val = elements[ptr]
            # Find max LIS ending before pos with value < val
            best = query(pos - 1, comp_val - 1)
            dp = best + 1
            update(pos, comp_val, dp)
            ptr += 1
        # Answer query: max LIS in prefix R with values <= X
        ans[idx] = query(R, comp[X])

    sys.stdout.write('\n'.join(map(str, ans)) + '\n')

if __name__ == '__main__':
    main()