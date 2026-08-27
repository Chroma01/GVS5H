import sys

# Increase recursion depth just in case
sys.setrecursionlimit(200005)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        T_str = next(iterator)
    except StopIteration:
        return
        
    T = int(T_str)
    results = []
    
    # Fenwick Tree implementation
    class FenwickTree:
        def __init__(self, size):
            self.n = size
            self.tree = [0] * (self.n + 1)
        
        def update(self, i, delta):
            while i <= self.n:
                self.tree[i] += delta
                i += i & (-i)
        
        def query(self, i):
            s = 0
            while i > 0:
                s += self.tree[i]
                i -= i & (-i)
            return s
        
        # Find the smallest index `idx` such that query(idx) >= k
        # This is equivalent to finding the k-th present element (1-based rank k)
        def find_kth(self, k):
            idx = 0
            current_sum = 0
            # Iterate from highest power of 2 down to 1
            bit_mask = 1 << (self.n.bit_length())
            while bit_mask > 0:
                t_idx = idx + bit_mask
                if t_idx <= self.n and current_sum + self.tree[t_idx] < k:
                    idx = t_idx
                    current_sum += self.tree[t_idx]
                bit_mask >>= 1
            return idx + 1

    for _ in range(T):
        try:
            N = int(next(iterator))
            A = []
            for _ in range(N):
                A.append(int(next(iterator)))
        except StopIteration:
            break
            
        if N == 0:
            results.append(0)
            continue
            
        # Precompute positions for each value
        pos = {}
        for idx, val in enumerate(A):
            if val not in pos:
                pos[val] = []
            pos[val].append(idx)
            
        ft = FenwickTree(N)
        for i in range(N):
            ft.update(i + 1, 1)
            
        # Pointers for each value to track the next available index in pos[v]
        ptr = {v: 0 for v in pos}
        
        head_idx = 0 
        total_ops = 0
        
        while head_idx < N:
            # Find the current head index (the first present element)
            # Since we maintain head_idx, we just need to ensure it's present.
            # If it was deleted, we need to find the next one.
            # However, our logic updates head_idx to the next present element after deletion.
            # So we just need to check if head_idx is valid.
            # But to be safe against edge cases or logic drift, let's find the first present element.
            # Actually, finding the first present element is finding the 1st element.
            # But if the array is empty, ft.query(N) == 0.
            
            if ft.query(N) == 0:
                break
                
            # Find the index of the current head (1st present element)
            # We can use binary search or the find_kth method.
            # Since we need to do this often, find_kth is O(log N).
            # But wait, we might have updated head_idx manually.
            # Let's trust head_idx is correct from previous step, but verify.
            # Actually, simpler: just use find_kth(1) to get the current head.
            # But if we just deleted the head, we need the next one.
            # Let's rely on the logic flow: after deletion, we set head_idx to the next element.
            # So we just need to ensure head_idx is valid.
            
            # Check if head_idx is present
            # If not, find the next present index.
            # Since we delete in blocks, head_idx should be the start of the block.
            # If head_idx was deleted, we need to find the next one.
            # Let's implement a robust way to get the current head.
            
            # Re-find current head to be safe
            # The current head is the element with rank 1.
            # But if we just deleted a block ending at rank R, the new head is rank R+1.
            # We can track the current rank of the head.
            # Let's restart the loop logic to be cleaner.
            
            # Actually, let's just use the `find_kth` method to get the current head index.
            # But we need to know the rank of the current head to calculate swaps.
            # Let's track `current_head_rank`.
            pass

        # Let's refactor the loop to be cleaner
        # We need to track the rank of the current head element.
        # Initially, head is at rank 1.
        
        current_head_rank = 1
        total_ops = 0
        
        while current_head_rank <= ft.query(N):
            # Find the original index of the current head
            head_idx = ft.find_kth(current_head_rank)
            val = A[head_idx]
            
            # Find the next occurrence of `val` that is present
            next_occ_idx = -1
            p = ptr[val]
            while p < len(pos[val]):
                idx = pos[val][p]
                if idx > head_idx:
                    # Check if present
                    # We can check rank: rank(idx) should be > rank(head_idx)
                    # But simpler: check if it's present.
                    # Since we have sorted indices, we can just check presence.
                    # To check presence efficiently: query(idx) - query(idx-1) == 1
                    if ft.query(idx) - ft.query(idx-1) == 1:
                        next_occ_idx = idx
                        break
                p += 1
            ptr[val] = p
            
            if next_occ_idx != -1:
                # Calculate swaps needed
                # We need to bring next_occ_idx to position 1 (index 0 in 0-based, rank 2)
                # The number of elements between head_idx and next_occ_idx is (rank(next) - rank(head) - 1)
                # These elements need to be swapped past.
                r_head = current_head_rank
                r_next = ft.query(next_occ_idx)
                
                swaps = r_next - r_head - 1
                total_ops += swaps
                
                # Now we have a block of `val` starting at rank `r_head`.
                # We need to count the length of this block.
                # The block includes head_idx, next_occ_idx, and any subsequent `val`s immediately following.
                # "Immediately following" means the next present element after next_occ_idx must be `val`.
                
                block_len = 2
                delete_indices = [head_idx, next_occ_idx]
                
                # Check subsequent elements
                # We start checking from the element after next_occ_idx.
                # The rank of the element after next_occ_idx is r_next + 1.
                curr_rank = r_next + 1
                
                while True:
                    # Find the index with rank `curr_rank`
                    # If curr_rank > total present, break
                    if curr_rank > ft.query(N):
                        break
                    
                    next_idx = ft.find_kth(curr_rank)
                    if A[next_idx] == val:
                        block_len += 1
                        delete_indices.append(next_idx)
                        curr_rank += 1
                    else:
                        break
                
                # Delete the block
                total_ops += 1
                
                # Remove from BIT
                for idx in delete_indices:
                    ft.update(idx + 1, -1)
                
                # Update current_head_rank
                # The last deleted element had rank `r_last` (before deletion).
                # After deletion, the next element has rank `r_last` (since one element is removed before it? No).
                # Let's trace:
                # Before deletion: elements at ranks 1..block_len are deleted.
                # The element at rank `block_len + 1` becomes the new head.
                # So new current_head_rank = block_len + 1.
                # Wait, `block_len` is the count of deleted elements.
                # So the new head is at rank `block_len + 1`.
                
                current_head_rank = block_len + 1
                
            else:
                # No next occurrence, delete single element
                total_ops += 1
                ft.update(head_idx + 1, -1)
                
                # The element at rank `current_head_rank` is deleted.
                # The next element is at rank `current_head_rank + 1`.
                current_head_rank += 1

        results.append(total_ops)

    print('\n'.join(map(str, results)))

if __name__ == '__main__':
    solve()