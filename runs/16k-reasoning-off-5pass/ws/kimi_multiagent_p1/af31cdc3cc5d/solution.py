import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))

    # Linked list representation for dynamic adjacency
    prev = [-1] * n
    next = [-1] * n
    for i in range(n):
        prev[i] = i - 1
        next[i] = i + 1 if i + 1 < n else -1

    # Priority queue of (negative difference, left index, right index)
    pq = []
    for i in range(n - 1):
        heapq.heappush(pq, (-abs(A[i] - A[i+1]), i, i+1))

    removed = [False] * n
    total = 0

    while pq:
        neg_diff, l, r = heapq.heappop(pq)
        diff = -neg_diff

        # Skip if already removed or no longer adjacent
        if removed[l] or removed[r] or next[l] != r:
            continue

        # Pair l and r
        total += diff
        removed[l] = True
        removed[r] = True

        # Update linked list
        pl = prev[l]
        nr = next[r]

        if pl != -1:
            next[pl] = nr
        if nr != -1:
            prev[nr] = pl

        # Add new adjacent pair if both neighbors exist
        if pl != -1 and nr != -1:
            heapq.heappush(pq, (-abs(A[pl] - A[nr]), pl, nr))

    print(total)

main()