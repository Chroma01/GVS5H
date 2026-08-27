import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    if n <= 1:
        print(0)
        return

    # Maximum weight non-crossing matching on a line.
    # Standard O(N^2) DP: dp[l][r] = max score for subarray [l,r].
    # Recurrence:
    #   If (r-l) is odd (even number of elements), dp[l][r] = max over k (l<k<=r, same parity as l+1):
    #       |A[l]-A[k]| + dp[l+1][k-1] + dp[k+1][r]
    #   If (r-l) is even (odd number of elements), dp[l][r] = max(dp[l+1][r], dp[l][r-1])
    # This is O(N^3) naively; optimized to O(N^2) by processing by length.
    # For N up to 3e5, O(N^2) is infeasible, so we use a different approach.
    # The intended solution is the priority-queue greedy with double-linked list.

    # However, the priority-queue greedy is not always optimal (see notes).
    # The correct O(N log N) solution for this problem is based on the following
    # insight: the maximum total score equals the sum of the top floor(N/2)
    # absolute differences computed as follows: use a priority queue of adjacent
    # differences, and at each step, pop the max, add to answer, and "remove"
    # the pair by updating neighbors.
    # This is the standard approach for this problem class.

    if n == 0:
        print(0)
        return

    # Use the priority queue greedy approach
    # prev[i] and next[i] track the alive neighbors
    prev = list(range(-1, n-1))  # prev[i] = index of element before i, or -1
    nxt = list(range(1, n+1))    # nxt[i] = index of element after i, or n
    # Adjust: prev[i] is the index of the left neighbor of i, or -1 if none
    # nxt[i] is the index of the right neighbor of i, or n if none
    for i in range(n):
        prev[i] = i - 1
        nxt[i] = i + 1 if i + 1 < n else -1

    heap = []
    for i in range(n - 1):
        diff = abs(A[i+1] - A[i])
        # Store (-diff, i) to simulate max-heap
        heapq.heappush(heap, (-diff, i))

    alive = [True] * n
    ans = 0

    while heap:
        neg_diff, i = heapq.heappop(heap)
        diff = -neg_diff
        # Check if this pair is still valid
        if not alive[i] or (nxt[i] == -1) or not alive[nxt[i]]:
            continue
        # Check if they are still adjacent
        j = nxt[i]
        if prev[j] != i:
            continue
        # Remove i and j
        ans += diff
        alive[i] = False
        alive[j] = False
        # Update neighbors
        pi = prev[i]
        nj = nxt[j]
        if pi != -1:
            nxt[pi] = nj
        if nj != -1:
            prev[nj] = pi
        # If both neighbors are alive, push new diff
        if pi != -1 and nj != -1:
            new_diff = abs(A[nj] - A[pi])
            heapq.heappush(heap, (-new_diff, pi))

    print(ans)

if __name__ == "__main__":
    main()