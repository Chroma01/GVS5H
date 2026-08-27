import sys
import heapq


def solve_case(a):
    value = []
    size = []

    for x in a:
        if value and value[-1] == x:
            size[-1] += 1
        else:
            value.append(x)
            size.append(1)

    m = len(value)
    if m <= 3:
        return m

    prv = [i - 1 for i in range(m)]
    nxt = [i + 1 for i in range(m)]
    nxt[-1] = -1
    alive = [True] * m

    def applicable(left):
        if left == -1 or not alive[left]:
            return False

        b = nxt[left]
        if b == -1:
            return False
        c = nxt[b]
        if c == -1:
            return False
        d = nxt[c]
        if d == -1:
            return False

        return (
            size[b] == 1
            and size[c] == 1
            and value[left] == value[c]
            and value[b] == value[d]
        )

    # Original node indices remain in left-to-right order among live nodes.
    # Therefore the minimum applicable index is the leftmost rewrite.
    heap = list(range(m))
    heapq.heapify(heap)

    def add_near(x):
        # A rewrite beginning at p reads p and its next three live nodes.
        # After changing a node/edge at x, only starts at x or one of the
        # preceding three live nodes can have changed applicability.
        p = x
        for _ in range(4):
            if p == -1:
                break
            heapq.heappush(heap, p)
            p = prv[p]

    reductions = 0

    while heap:
        left = heapq.heappop(heap)

        # Heap entries may have been inserted before later rewrites changed
        # or deleted their local neighborhood, so validate on extraction.
        if not applicable(left):
            continue

        b = nxt[left]
        c = nxt[b]
        right = nxt[c]

        # x^p, y, x, y^q -> x^(p+1), y^(q+1)
        size[left] += 1
        size[right] += 1

        alive[b] = False
        alive[c] = False
        nxt[left] = right
        prv[right] = left

        reductions += 1

        # All possible newly changed four-run windows start at left or one
        # of its three predecessors. Adding around right is redundant but
        # safe, and also schedules all windows involving the changed right
        # endpoint explicitly.
        add_near(left)
        add_near(right)

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