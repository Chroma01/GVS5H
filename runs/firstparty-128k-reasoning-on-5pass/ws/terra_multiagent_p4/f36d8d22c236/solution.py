import sys

def main():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    t = input().strip()

    to = [-1] * 26

    for a, b in zip(s, t):
        x = ord(a) - ord('a')
        y = ord(b) - ord('a')
        if to[x] != -1 and to[x] != y:
            print(-1)
            return
        to[x] = y

    edges = 0
    for x in range(26):
        if to[x] != -1 and to[x] != x:
            edges += 1

    state = [0] * 26
    cycles = 0

    for start in range(26):
        if state[start] != 0:
            continue

        cur = start
        while cur != -1 and state[cur] == 0:
            state[cur] = 1
            nxt = to[cur]
            if nxt == -1 or nxt == cur:
                cur = -1
            else:
                cur = nxt

        if cur != -1 and state[cur] == 1:
            cycles += 1

        cur = start
        while cur != -1 and state[cur] == 1:
            state[cur] = 2
            nxt = to[cur]
            if nxt == -1 or nxt == cur:
                break
            cur = nxt

    if cycles > 0 and len(set(t)) == 26:
        print(-1)
    else:
        print(edges + cycles)

if __name__ == "__main__":
    main()