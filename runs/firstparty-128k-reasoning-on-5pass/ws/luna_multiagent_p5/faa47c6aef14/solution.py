import sys
from bisect import bisect_left


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    x = next(it) - 1

    a = [next(it) for _ in range(n)]
    b = [next(it) for _ in range(n)]
    p = [next(it) - 1 for _ in range(n)]
    q = [next(it) - 1 for _ in range(n)]

    inv_p = [0] * n
    inv_q = [0] * n
    for i in range(n):
        inv_p[p[i]] = i
        inv_q[q[i]] = i

    def build_sequence(inv, present):
        dist = [-1] * n
        dist[x] = 0
        path = []

        cur = x
        while True:
            cur = inv[cur]
            if cur == x:
                break
            dist[cur] = len(path) + 1
            path.append(cur)

        farthest = 0
        for i in range(n):
            if present[i]:
                if dist[i] == -1:
                    return None
                farthest = max(farthest, dist[i])

        if farthest == 0:
            return []

        return path[farthest - 1::-1]

    red = build_sequence(inv_p, a)
    blue = build_sequence(inv_q, b)

    if red is None or blue is None:
        print(-1)
        return

    pos_blue = [-1] * n
    for i, vertex in enumerate(blue):
        pos_blue[vertex] = i

    mapped = [pos_blue[vertex] for vertex in red if pos_blue[vertex] != -1]

    tails = []
    for value in mapped:
        index = bisect_left(tails, value)
        if index == len(tails):
            tails.append(value)
        else:
            tails[index] = value

    lcs = len(tails)
    print(len(red) + len(blue) - lcs)


if __name__ == "__main__":
    main()