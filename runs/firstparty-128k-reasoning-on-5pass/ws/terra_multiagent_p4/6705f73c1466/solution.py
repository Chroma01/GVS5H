import sys

def main():
    input = sys.stdin.readline
    n = int(input())
    s = input().strip()

    transformed = []
    for i, ch in enumerate(s):
        if ch == '1':
            transformed.append(i - len(transformed))

    median = transformed[len(transformed) // 2]
    answer = sum(abs(x - median) for x in transformed)
    print(answer)

if __name__ == "__main__":
    main()