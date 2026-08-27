import sys

def main():
    input = sys.stdin.readline

    N, R, C = map(int, input().split())
    S = input().strip()

    visited = {(0, 0)}
    pr = 0
    pc = 0
    answer = []

    for ch in S:
        if ch == 'N':
            pr -= 1
        elif ch == 'S':
            pr += 1
        elif ch == 'W':
            pc -= 1
        else:  # E
            pc += 1

        if (pr - R, pc - C) in visited:
            answer.append('1')
        else:
            answer.append('0')

        visited.add((pr, pc))

    print(''.join(answer))

if __name__ == "__main__":
    main()