import sys
import heapq

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
    except StopIteration:
        return

    # If N < 2, no operations can be performed
    if N < 2:
        print(0)
        return

    # Initialize doubly linked list using arrays
    # L[i] stores the index of the left neighbor of i
    # R[i] stores the index of the right neighbor of i
    L = [i - 1 for i in range(N)]
    R = [i + 1 for i in range(N)]
    R[N - 1] = -1  # Right of last element is None

    # Max-heap to store (-difference, left_index, right_index)
    # We store left_index to identify the pair uniquely
    pq = []

    # Initialize heap with all adjacent pairs
    for i in range(N - 1):
        diff = abs(A[i] - A[i+1])
        heapq.heappush(pq, (-diff, i, i+1))

    total_score = 0
    operations_count = 0

    while pq:
        neg_diff, u, v = heapq.heappop(pq)
        diff = -neg_diff

        # Check if u and v are still adjacent
        # u should be the left neighbor of v
        if L[v] != u:
            continue

        # Perform the operation: remove u and v
        total_score += diff
        operations_count += 1

        # Update linked list
        left_neighbor = L[u]
        right_neighbor = R[v]

        # Remove u and v
        if left_neighbor != -1:
            R[left_neighbor] = right_neighbor
        if right_neighbor != -1:
            L[right_neighbor] = left_neighbor

        # If a new pair is formed, add it to the heap
        if left_neighbor != -1 and right_neighbor != -1:
            new_diff = abs(A[left_neighbor] - A[right_neighbor])
            heapq.heappush(pq, (-new_diff, left_neighbor, right_neighbor))

        # Check if we have removed enough pairs
        # We need to remove N-1 pairs to leave 1 element
        if operations_count == N - 1:
            break

    print(total_score)

if __name__ == '__main__':
    solve()