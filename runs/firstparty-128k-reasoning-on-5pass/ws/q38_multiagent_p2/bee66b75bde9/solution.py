import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    m = int(data[1])
    pts = []
    idx = 2

    for _ in range(m):
        x = int(data[idx])
        y = int(data[idx + 1])
        c = data[idx + 2]
        idx += 3
        pts.append((x, y, 0 if c == b'B' else 1))

    pts.sort(key=lambda p: (-p[0], p[2]))

    max_y = 0
    for _, y, kind in pts:
        if kind == 0:
            if y > max_y:
                max_y = y
        else:
            if y <= max_y:
                sys.stdout.write("No\n")
                return

    sys.stdout.write("Yes\n")

if __name__ == "__main__":
    main()