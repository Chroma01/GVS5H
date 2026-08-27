import sys

def solve():
    input = sys.stdin.readline
    N, R, C = map(int, input().split())
    S = input().strip()

    dr = dc = 0
    seen = {(0, 0)}
    ans = []

    for ch in S:
        if ch == 'N':
            dr -= 1
        elif ch == 'S':
            dr += 1
        elif ch == 'W':
            dc -= 1
        else:  # E
            dc += 1

        if (dr - R, dc - C) in seen:
            ans.append('1')
        else:
            ans.append('0')

        seen.add((dr, dc))

    print(''.join(ans))

if __name__ == "__main__":
    solve()