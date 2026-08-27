import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1].decode()

    positions = [i for i, ch in enumerate(s) if ch == '1']
    adjusted = [p - i for i, p in enumerate(positions)]

    median = adjusted[len(adjusted) // 2]
    answer = sum(abs(value - median) for value in adjusted)

    print(answer)

if __name__ == "__main__":
    solve()