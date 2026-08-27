import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); R = int(data[1]); C = int(data[2])
    S = data[3] if len(data) > 3 else b''
    M = 4 * N + 5
    seen = {0}
    add = seen.add
    r = 0
    c = 0
    out = []
    ap = out.append
    nN = 78  # 'N'
    nW = 87  # 'W'
    nS = 83  # 'S'
    # 'E' = 69
    base = -R * M - C
    for ch in S:
        if ch == nN:
            r -= 1
        elif ch == nW:
            c -= 1
        elif ch == nS:
            r += 1
        else:
            c += 1
        k = r * M + c
        add(k)
        ap('1' if (k + base) in seen else '0')
    sys.stdout.write(''.join(out) + '\n')

main()