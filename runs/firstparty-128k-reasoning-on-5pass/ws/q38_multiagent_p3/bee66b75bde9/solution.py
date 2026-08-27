import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    M = int(data[1])

    bounds = {}
    idx = 2

    for _ in range(M):
        x = int(data[idx])
        y = int(data[idx + 1])
        c = data[idx + 2]
        idx += 3

        if x in bounds:
            l, u = bounds[x]
        else:
            l, u = 0, N

        if c == b'B':
            if y > l:
                l = y
        else:
            v = y - 1
            if v < u:
                u = v

        bounds[x] = (l, u)

    max_l = 0

    for x in sorted(bounds.keys(), reverse=True):
        l, u = bounds[x]
        if l > max_l:
            max_l = l
        if max_l > u:
            sys.stdout.write("No\n")
            return

    sys.stdout.write("Yes\n")

if __name__ == "__main__":
    main()