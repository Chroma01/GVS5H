import sys

def solve() -> None:
    input = sys.stdin.readline
    N, M = map(int, input().split())
    # lower bound L_i (max column of a black cell in row i)
    L = {}
    # upper bound U_i (min(column-1) of a white cell in row i)
    U = {}

    for _ in range(M):
        x_str, y_str, c = input().split()
        x = int(x_str)
        y = int(y_str)
        if c == 'B':
            # update max y for black cells in this row
            if x in L:
                if y > L[x]:
                    L[x] = y
            else:
                L[x] = y
        else:  # c == 'W'
            # update min (y-1) for white cells in this row
            val = y - 1
            if x in U:
                if val < U[x]:
                    U[x] = val
            else:
                U[x] = val

    # collect all rows that have any constraint
    rows = set(L.keys()) | set(U.keys())
    constrained = []
    for r in rows:
        li = L.get(r, 0)
        ui = U.get(r, N)
        if li > ui:
            print("No")
            return
        constrained.append((r, li, ui))

    constrained.sort(key=lambda x: x[0])

    prev = N  # current maximum allowed R_i
    for r, li, ui in constrained:
        ub = ui if ui < prev else prev  # min(ui, prev)
        if li > ub:
            print("No")
            return
        # we can set R_r = ub; keep prev as large as possible
        prev = ub

    print("Yes")

if __name__ == "__main__":
    solve()