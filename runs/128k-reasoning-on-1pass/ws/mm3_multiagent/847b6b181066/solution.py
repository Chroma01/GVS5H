import sys

def solve() -> None:
    data = sys.stdin.read().split()
    if len(data) < 4:
        return
    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3].strip()

    # direction mapping
    d = {
        'N': (-1, 0),
        'W': (0, -1),
        'S': (1, 0),
        'E': (0, 1)
    }

    # current global offset (cumulative wind displacement)
    off_r, off_c = 0, 0

    # relative coordinates of all smoke particles w.r.t. the current offset
    rel = {(0, 0)}          # initially only the origin

    out = []

    for ch in S:
        dr, dc = d[ch]
        off_r += dr
        off_c += dc

        # Query: does (R, C) contain smoke at time t+0.5 ?
        if (R - off_r, C - off_c) in rel:
            out.append('1')
        else:
            out.append('0')

        # Generate new smoke at origin if it is empty
        if ( -off_r, -off_c) not in rel:
            rel.add((-off_r, -off_c))

    sys.stdout.write(''.join(out))

if __name__ == "__main__":
    solve()