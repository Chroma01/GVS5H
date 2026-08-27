import sys

def main():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()

    positions = [i for i, ch in enumerate(s) if ch == '1']
    m = len(positions)

    median = positions[m // 2] - (m // 2)
    answer = sum(abs((pos - i) - median) for i, pos in enumerate(positions))

    print(answer)

if __name__ == "__main__":
    main()