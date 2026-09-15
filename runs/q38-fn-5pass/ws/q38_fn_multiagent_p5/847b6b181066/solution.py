import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3]

    r = 0
    c = 0

    seen = {(0, 0)}
    ans = []
    append = ans.append
    add = seen.add

    for ch in S:
        if ch == 78:       # 'N'
            r -= 1
        elif ch == 87:     # 'W'
            c -= 1
        elif ch == 83:     # 'S'
            r += 1
        else:              # 'E'
            c += 1

        if (r - R, c - C) in seen:
            append('1')
        else:
            append('0')

        add((r, c))

    sys.stdout.write(''.join(ans))

if __name__ == "__main__":
    main()