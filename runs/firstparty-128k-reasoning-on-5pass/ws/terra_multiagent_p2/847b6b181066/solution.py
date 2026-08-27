import sys

def main():
    input = sys.stdin.readline
    N, R, C = map(int, input().split())
    S = input().strip()

    pr = pc = 0
    seen = {(0, 0)}
    ans = []

    for ch in S:
        if ch == 'N':
            pr -= 1
        elif ch == 'S':
            pr += 1
        elif ch == 'W':
            pc -= 1
        else:
            pc += 1

        if (pr - R, pc - C) in seen:
            ans.append('1')
        else:
            ans.append('0')

        seen.add((pr, pc))

    print(''.join(ans))

if __name__ == "__main__":
    main()