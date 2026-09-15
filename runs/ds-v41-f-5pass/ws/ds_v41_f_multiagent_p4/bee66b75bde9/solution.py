import sys

def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1

    Ld = {}  # row -> max black Y (lower bound on a_row)
    Ud = {}  # row -> min white Y - 1 (upper bound on a_row)

    for _ in range(M):
        x = int(data[idx]); y = int(data[idx + 1]); c = data[idx + 2]; idx += 3
        if c == b'B':
            if x not in Ld or y > Ld[x]:
                Ld[x] = y
        else:
            u = y - 1
            if x not in Ud or u < Ud[x]:
                Ud[x] = u

    rows = set(Ld) | set(Ud)

    # Per-row feasibility
    for r in rows:
        if Ld.get(r, 0) > Ud.get(r, N):
            print("No")
            return

    # Sweep constrained rows ascending; prefix min of upper bounds must stay >= lower bound
    cur = N  # prefix minimum of U over processed rows
    for r in sorted(rows):
        u = Ud.get(r, N)
        if u < cur:
            cur = u
        if cur < Ld.get(r, 0):
            print("No")
            return

    print("Yes")

main()