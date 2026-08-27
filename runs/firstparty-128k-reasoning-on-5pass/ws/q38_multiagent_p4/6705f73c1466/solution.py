import sys

def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return

    n = int(data[0])
    s = data[1].strip()

    q = []
    j = 0
    for idx, ch in enumerate(s):
        if ch == '1':
            q.append(idx - j)
            j += 1

    if not q:
        print(0)
        return

    median = q[len(q) // 2]
    ans = sum(abs(x - median) for x in q)
    print(ans)

if __name__ == "__main__":
    main()