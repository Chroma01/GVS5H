import sys

def main():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    positions = [i for i, ch in enumerate(s) if ch == '1']
    adjusted = [pos - i for i, pos in enumerate(positions)]

    median = adjusted[len(adjusted) // 2]
    answer = sum(abs(x - median) for x in adjusted)

    print(answer)

if __name__ == "__main__":
    main()