import sys

def solve():
    input = sys.stdin.readline

    n = int(input())
    s = input().strip()
    t = input().strip()

    nxt = [-1] * 26

    for a, b in zip(s, t):
        x = ord(a) - ord('a')
        y = ord(b) - ord('a')
        if nxt[x] != -1 and nxt[x] != y:
            print(-1)
            return
        nxt[x] = y

    operations = 0
    graph = [-1] * 26

    for x in range(26):
        if nxt[x] != -1 and nxt[x] != x:
            graph[x] = nxt[x]
            operations += 1

    state = [0] * 26
    cycle_count = 0

    for start in range(26):
        if state[start] != 0:
            continue

        cur = start
        while cur != -1 and state[cur] == 0:
            state[cur] = 1
            cur = graph[cur]

        if cur != -1 and state[cur] == 1:
            cycle_count += 1

        cur = start
        while cur != -1 and state[cur] == 1:
            state[cur] = 2
            cur = graph[cur]

    if cycle_count > 0 and len(set(t)) == 26:
        print(-1)
    else:
        print(operations + cycle_count)

if __name__ == "__main__":
    solve()