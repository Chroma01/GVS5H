import sys

def main():
    input = sys.stdin.readline
    N, R, C = map(int, input().split())
    S = input().strip()

    r = c = 0
    seen = {(0, 0)}
    ans = []

    for ch in S:
        if ch == 'N':
            r -= 1
        elif ch == 'S':
            r += 1
        elif ch == 'W':
            c -= 1
        else:
            c += 1

        ans.append('1' if (r - R, c - C) in seen else '0')

        seen.add((r, c))

    print(''.join(ans))

if __name__ == "__main__":
    main()