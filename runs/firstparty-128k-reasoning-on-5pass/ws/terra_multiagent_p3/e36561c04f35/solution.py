import sys
import heapq


def solve_case(a):
    values = []
    sizes = []

    for x in a:
        if values and values[-1] == x:
            sizes[-1] += 1
        else:
            values.append(x)
            sizes.append(1)

    m = len(values)
    if m == 1:
        return 1

    value = [0] + values
    size = [0] + sizes

    prev = [0] * (m + 1)
    nxt = [0] * (m + 1)
    alive = [False] + [True] * m

    for i in range(1, m + 1):
        prev[i] = i - 1
        nxt[i] = i + 1 if i < m else 0

    def reducible(x):
        if x == 0 or not alive[x]:
            return False

        y = nxt[x]
        if y == 0 or size[y] != 1:
            return False

        z = nxt[y]
        if z == 0 or size[z] != 1:
            return False

        w = nxt[z]
        return (
            w != 0
            and value[x] == value[z]
            and value[y] == value[w]
        )

    heap = []
    for i in range(1, m + 1):
        if reducible(i):
            heapq.heappush(heap, i)

    reductions = 0

    while heap:
        x = heapq.heappop(heap)
        if not reducible(x):
            continue

        y = nxt[x]
        z = nxt[y]
        w = nxt[z]

        # X^p, Y, X, Y^q -> X^(p+1), Y^(q+1)
        size[x] += 1
        size[w] += 1

        alive[y] = False
        alive[z] = False
        nxt[x] = w
        prev[w] = x

        reductions += 1

        # Recheck windows whose forward four-run view changed.
        u = x
        for _ in range(4):
            if u == 0:
                break
            if reducible(u):
                heapq.heappush(heap, u)
            u = prev[u]

        if reducible(w):
            heapq.heappush(heap, w)

    return m - reductions


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    pos = 1
    ans = []

    for _ in range(t):
        n = data[pos]
        pos += 1
        ans.append(str(solve_case(data[pos:pos + n])))
        pos += n

    sys.stdout.write("\n".join(ans))


if __name__ == "__main__":
    main()