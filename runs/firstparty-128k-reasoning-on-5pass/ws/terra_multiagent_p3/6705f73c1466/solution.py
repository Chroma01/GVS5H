import sys

def main():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    adjusted = []
    rank = 0
    for pos, ch in enumerate(s):
        if ch == '1':
            adjusted.append(pos - rank)
            rank += 1

    median = adjusted[len(adjusted) // 2]
    answer = sum(abs(x - median) for x in adjusted)
    print(answer)

if __name__ == "__main__":
    main()