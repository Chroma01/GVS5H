import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3]

    base = 4 * N + 10
    offset = 2 * N + 5

    seen = {offset * base + offset}  # encoded (0, 0)

    x = 0
    y = 0
    out = bytearray()

    add = seen.add
    contains = seen.__contains__

    for ch in S:
        if ch == 78:      # 'N'
            x -= 1
        elif ch == 87:    # 'W'
            y -= 1
        elif ch == 83:    # 'S'
            x += 1
        else:             # 'E'
            y += 1

        add((x + offset) * base + (y + offset))

        if contains((x - R + offset) * base + (y - C + offset)):
            out.append(49)  # '1'
        else:
            out.append(48)  # '0'

    sys.stdout.buffer.write(out)

if __name__ == "__main__":
    main()