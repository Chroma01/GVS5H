import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1].decode()

    positions = [i for i, ch in enumerate(s) if ch == '1']
    transformed = [p - i for i, p in enumerate(positions)]

    median = transformed[len(transformed) // 2]
    answer = sum(abs(value - median) for value in transformed)

    print(answer)

if __name__ == "__main__":
    solve()