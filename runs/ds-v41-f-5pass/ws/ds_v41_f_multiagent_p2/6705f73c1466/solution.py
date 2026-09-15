import sys

def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0])
    S = data[1].decode()

    # Collect 1-indexed positions of '1'
    t = []
    j = 0
    for i, ch in enumerate(S, 1):
        if ch == '1':
            j += 1
            t.append(i - j)

    if not t:
        print(0)
        return

    t.sort()
    median = t[len(t) // 2]
    ans = sum(abs(x - median) for x in t)
    print(ans)

main()