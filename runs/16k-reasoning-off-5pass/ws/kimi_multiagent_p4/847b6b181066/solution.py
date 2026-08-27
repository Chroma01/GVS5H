import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3]

    dx = 0
    dy = 0
    B = {(0, 0)}
    out = []
    for ch in S:
        if ch == 'N':
            dx -= 1
        elif ch == 'S':
            dx += 1
        elif ch == 'W':
            dy -= 1
        else:  # 'E'
            dy += 1
        cur = (dx, dy)
        if cur not in B:
            B.add(cur)
        if (dx - R, dy - C) in B:
            out.append('1')
        else:
            out.append('0')
    sys.stdout.write(''.join(out) + '\n')

main()