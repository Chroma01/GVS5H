import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))

    # per row: [max_black, min_white] (None for missing)
    row_info = {}

    for _ in range(M):
        x = int(next(it))
        y = int(next(it))
        c = next(it).decode()          # 'B' or 'W'
        if x not in row_info:
            row_info[x] = [0, None]    # max_black, min_white
        if c == 'B':
            if y > row_info[x][0]:
                row_info[x][0] = y
        else:  # 'W'
            wm = row_info[x][1]
            if wm is None or y < wm:
                row_info[x][1] = y

    # Build list of constrained rows with their intervals [L, R]
    rows = []
    for x, (bm, wm) in row_info.items():
        L = bm                         # at least 0 if no black cell
        if wm is not None:
            R = wm - 1                 # a[x] ≤ wm‑1
        else:
            R = N
        if L > R:                      # contradictory requirements
            print("No")
            return
        rows.append((x, L, R))

    rows.sort()                        # increasing row index

    cur = N                            # maximal value we may use
    for _, L, R in rows:
        allowed = R if R < cur else cur   # min(R, cur)
        if allowed < L:
            print("No")
            return
        cur = allowed

    print("Yes")

if __name__ == "__main__":
    solve()