import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    events = []  # (x, type, y): type 0 = W (processed first), 1 = B
    for _ in range(m):
        x = int(next(it))
        y = int(next(it))
        c = next(it)
        if c == b'W':
            events.append((x, 0, y))
        else:
            events.append((x, 1, y))
    events.sort(key=lambda e: (e[0], e[1]))
    INF = float('inf')
    min_wy = INF
    for x, t, y in events:
        if t == 0:
            if y < min_wy:
                min_wy = y
        else:
            if min_wy <= y:
                sys.stdout.write("No\n")
                return
    sys.stdout.write("Yes\n")

main()