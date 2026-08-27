import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    r = int(data[1])
    c = int(data[2])
    s = data[3]

    x = 0
    y = 0
    seen = {(0, 0)}
    contains = seen.__contains__
    add = seen.add
    ans = bytearray()

    for ch in s:
        if ch == 78:      # 'N'
            x -= 1
        elif ch == 87:    # 'W'
            y -= 1
        elif ch == 83:    # 'S'
            x += 1
        else:             # 'E'
            y += 1

        if contains((x - r, y - c)):
            ans.append(49)  # '1'
        else:
            ans.append(48)  # '0'

        add((x, y))

    ans.append(10)  # newline
    sys.stdout.buffer.write(ans)

if __name__ == "__main__":
    main()