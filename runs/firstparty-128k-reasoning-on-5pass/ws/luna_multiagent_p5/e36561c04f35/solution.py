import sys
import heapq


def solve_case(a):
    n = len(a)

    prev = [-1] + list(range(n - 1))
    nxt = list(range(1, n)) + [-1]
    alive = [True] * n
    version = [0] * n
    heap = []

    # Objective = adjacent swaps already made + current number of runs.
    answer = 1
    for i in range(1, n):
        if a[i] != a[i - 1]:
            answer += 1

    def delta_of(left):
        right = nxt[left]
        if right == -1 or a[left] == a[right]:
            return None

        p = prev[left]
        q = nxt[right]

        before = 0
        if p != -1 and a[p] == a[left]:
            before += 1
        if q != -1 and a[right] == a[q]:
            before += 1

        after = 0
        if p != -1 and a[p] == a[right]:
            after += 1
        if q != -1 and a[left] == a[q]:
            after += 1

        # Original indices determine the inversion change.
        inv_delta = -1 if left > right else 1

        # Runs = number of elements - number of equal adjacent pairs.
        return inv_delta + before - after

    def refresh(x):
        if x == -1 or not alive[x]:
            return
        version[x] += 1
        delta = delta_of(x)
        if delta is not None:
            heapq.heappush(heap, (delta, x, version[x]))

    for i in range(n - 1):
        refresh(i)

    while heap:
        delta, left, ver = heapq.heappop(heap)

        if not alive[left] or version[left] != ver:
            continue

        right = nxt[left]
        if right == -1 or a[left] == a[right]:
            continue

        # Strictly positive exchanges are never useful.
        # For zero exchanges, use only the orientation that increases
        # the original-position inversion count; this prevents cycles.
        if delta > 0 or (delta == 0 and left > right):
            break

        p = prev[left]
        q = nxt[right]

        if p != -1:
            nxt[p] = right
        prev[right] = p

        nxt[right] = left
        prev[left] = right

        nxt[left] = q
        if q != -1:
            prev[q] = left

        answer += delta

        refresh(p)
        refresh(right)
        refresh(left)

    return answer


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    t = data[0]
    pos = 1
    result = []

    for _ in range(t):
        n = data[pos]
        pos += 1
        a = data[pos:pos + n]
        pos += n
        result.append(str(solve_case(a)))

    sys.stdout.write("\n".join(result))


if __name__ == "__main__":
    main()