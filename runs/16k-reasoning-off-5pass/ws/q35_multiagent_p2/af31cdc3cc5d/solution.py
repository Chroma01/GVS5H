import sys
import heapq

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    n = int(input_data[0])
    a = list(map(int, input_data[1:n+1]))
    
    if n <= 1:
        print(0)
        return

    # We need to manage the list of numbers and their neighbors.
    # We'll use a doubly linked list structure via arrays for O(1) deletion and neighbor lookup.
    # left[i] is the index of the element to the left of i
    # right[i] is the index of the element to the right of i
    left = [i - 1 for i in range(n)]
    right = [i + 1 for i in range(n)]
    
    # To handle removals, we mark indices as removed.
    removed = [False] * n
    
    # Priority queue to store pairs: (-score, i, j)
    # We use negative score because heapq is a min-heap.
    # i is the left index, j is the right index.
    # We ensure i < j.
    pq = []
    
    for i in range(n - 1):
        score = abs(a[i] - a[i+1])
        heapq.heappush(pq, (-score, i, i+1))
        
    total_score = 0
    pairs_removed = 0
    target_pairs = n // 2
    
    while pq and pairs_removed < target_pairs:
        neg_score, i, j = heapq.heappop(pq)
        score = -neg_score
        
        # If either element is already removed, skip
        if removed[i] or removed[j]:
            continue
            
        # If they are not adjacent in the current list, skip
        # This can happen if we created a new pair but it was already processed or invalidated
        # Actually, with the linked list, if i and j are not removed, we check if they are neighbors.
        if right[i] != j or left[j] != i:
            continue
            
        # Remove i and j
        removed[i] = True
        removed[j] = True
        total_score += score
        pairs_removed += 1
        
        # Connect the left neighbor of i and the right neighbor of j
        l = left[i]
        r = right[j]
        
        if l != -1:
            right[l] = r
        if r != n:
            left[r] = l
            
        # If both l and r are valid indices, create a new pair
        if l != -1 and r != n:
            new_score = abs(a[l] - a[r])
            heapq.heappush(pq, (-new_score, l, r))
            
    print(total_score)

if __name__ == '__main__':
    solve()