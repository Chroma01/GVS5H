import sys

def solve():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); X = int(data[1]); Y = int(data[2])
    S = data[3].decode(); T = data[4].decode()

    # Positions of 1s in S and T (0-indexed, increasing).
    ps = [i for i, c in enumerate(S) if c == '1']
    pt = [i for i, c in enumerate(T) if c == '1']
    if len(ps) != len(pt):
        print("No")
        return
    for a, b in zip(ps, pt):
        if (a - b) % X != 0:
            print("No")
            return

    # Positions of 0s; lengths match automatically since |S|=|T|=N and #1s match.
    zs = [i for i, c in enumerate(S) if c == '0']
    zt = [i for i, c in enumerate(T) if c == '0']
    for a, b in zip(zs, zt):
        if (a - b) % Y != 0:
            print("No")
            return

    print("Yes")

solve()