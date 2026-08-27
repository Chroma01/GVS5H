import sys

def main():
    input = sys.stdin.readline

    N = int(input())
    S = input().strip()
    T = input().strip()

    to = [-1] * 26

    for a, b in zip(S, T):
        x = ord(a) - 97
        y = ord(b) - 97
        if to[x] != -1 and to[x] != y:
            print(-1)
            return
        to[x] = y

    edges = 0
    nxt = [-1] * 26
    for x in range(26):
        if to[x] != -1 and to[x] != x:
            edges += 1
            nxt[x] = to[x]

    state = [0] * 26
    cycles = 0

    for start in range(26):
        if state[start] != 0:
            continue

        path = []
        v = start

        while v != -1 and state[v] == 0:
            state[v] = 1
            path.append(v)
            v = nxt[v]

        if v != -1 and state[v] == 1:
            cycles += 1

        for u in path:
            state[u] = 2

    if cycles > 0 and len(set(T)) == 26:
        print(-1)
    else:
        print(edges + cycles)

if __name__ == "__main__":
    main()