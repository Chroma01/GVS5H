import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3]

    seen = {(0, 0)}
    r = 0
    c = 0
    ans = bytearray()

    for ch in S:
        if ch == 78:      # 'N'
            r -= 1
        elif ch == 87:    # 'W'
            c -= 1
        elif ch == 83:    # 'S'
            r += 1
        else:             # 'E'
            c += 1

        if (r - R, c - C) in seen:
            ans.append(49)  # '1'
        else:
            ans.append(48)  # '0'

        seen.add((r, c))

    sys.stdout.buffer.write(ans + b'\n')

if __name__ == "__main__":
    main()