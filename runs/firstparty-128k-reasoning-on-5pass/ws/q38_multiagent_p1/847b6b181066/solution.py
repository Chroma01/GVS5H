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
    contains = seen.__contains__
    add = seen.add

    r = 0
    c = 0
    ans = bytearray(b'0' * N)

    for i, ch in enumerate(S):
        if ch == 78:      # 'N'
            r -= 1
        elif ch == 87:    # 'W'
            c -= 1
        elif ch == 83:    # 'S'
            r += 1
        else:             # 'E'
            c += 1

        if contains((r - R, c - C)):
            ans[i] = 49   # '1'
        add((r, c))

    sys.stdout.buffer.write(ans + b'\n')

if __name__ == "__main__":
    main()