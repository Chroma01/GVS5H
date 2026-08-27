import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    R = int(data[1])
    C = int(data[2])
    S = data[3].strip()
    dr = 0
    dc = 0
    seen = {(0, 0)}
    ans = []
    for ch in S:
        if ch == 'N':
            dr -= 1
        elif ch == 'S':
            dr += 1
        elif ch == 'W':
            dc -= 1
        elif ch == 'E':
            dc += 1
        target = (dr - R, dc - C)
        if target in seen:
            ans.append('1')
        else:
            ans.append('0')
        seen.add((dr, dc))
    sys.stdout.write(''.join(ans))

if __name__ == "__main__":
    solve()