from typing import List

class Solution:
    def maxProduct(self, nums: List[int], k: int, limit: int) -> int:
        n = len(nums)
        max_abs_sum = n * 12
        offset = max_abs_sum
        size = 2 * max_abs_sum + 1
        
        # dp[parity][sum_idx] = max product (only valid, <= limit kept)
        # We use a 2D array. -1 means unreachable.
        # We also track the "empty" base case. To handle taking the first element,
        # we can start with a virtual empty state. We can do this by initializing
        # with the empty state and then tracking non-emptiness separately.
        # But simpler: we just initialize dp with the empty state (parity 0, sum 0, product 1)
        # and also keep a set of "nonempty" states, or we can just not allow the answer
        # to be from the empty state by checking the length.
        # Since we need to maximize product and limit is small, we can store the max product.
        # However, as discussed, keeping only max product fails because a smaller product
        # might survive a multiplication that makes the max product invalid.
        # But note: if max product p_max and min product p_min for a state, and we take num,
        # p_min * num <= p_max * num. If p_max * num > limit, p_min * num might still be <= limit.
        # So we need to keep all products. But we can prune: for a state, if we have p1 < p2,
        # and p1 * 12 > limit, then p1 cannot be multiplied by any number >= 1 without exceeding limit.
        # So p1 is "dead" unless we multiply by 0. But we skip 0. So we can discard p1.
        # Actually, p1 * 1 = p1 <= limit, so p1 is not dead if we take 1s.
        # So we cannot easily prune. However, since limit <= 5000 and n <= 150, the number of
        # products per state is bounded. We can store sets of products.
        
        # Use dictionary to save memory: only store reachable states.
        # Each value is a set of products (all <= limit).
        dp = {}
        
        # We need to handle the first element properly. We can start with the empty state
        # and allow taking from it, but we must not consider the empty state as a valid answer.
        # We'll track a separate flag for the empty state, or we can just initialize with
        # the empty state and at the end ignore the case where product=1 and parity=0 and sum=0
        # and no elements taken? But other subsequences can also have product 1 (e.g., [1]).
        # So we need a robust way. We can store the length along with the product, or use a
        # separate dictionary for nonempty states.
        # Let's use a separate "has_empty" flag that persists: we can always take from an empty
        # state (product=1) as long as we haven't taken anything yet. But once we take something,
        # we are no longer empty. We can just process the first element manually, or we can
        # allow taking from empty at any time? No, that would allow empty subsequence to be
        # combined with elements, which is not right.
        # The empty state is only available before any elements are taken. So we can initialize
        # dp with the empty state, and also track that we have an empty state available.
        # When we take from empty, we go to nonempty. When we take from nonempty, we stay nonempty.
        # We can do this by having a special key for empty, or by initializing dp with the empty
        # state and then removing it from the "available to take" set after we process all elements?
        # Actually, the empty state is always available to be taken from, but only as the first element.
        # So we can do: for each element, we allow taking from the current empty state if it hasn't
        # been used yet. We can just process the first element separately.
        
        # Process first element
        num = nums[0]
        # Taking first element: parity 1, sum = num, product = num
        if num <= limit:
            new_par = 1
            new_s = offset + num
            if 0 <= new_s < size:
                key = (new_par, new_s)
                dp[key] = {num}
        
        # Process remaining elements
        for idx in range(1, n):
            num = nums[idx]
            new_dp = {}
            # Copy current states (skipping the number)
            for key, prods in dp.items():
                new_dp[key] = set(prods)
            
            # Transition: take the number
            for (par, s), prods in dp.items():
                new_par = 1 - par
                sign = 1 if par == 0 else -1
                new_s = s + sign * num
                if 0 <= new_s < size:
                    new_key = (new_par, new_s)
                    new_prods = set()
                    for p in prods:
                        new_prod = p * num
                        if new_prod > limit:
                            # Cap: since we only multiply by non-negative integers,
                            # and we can skip 0, any product > limit will remain > limit
                            # if we multiply by >0. So we can discard it.
                            # EXCEPT if we multiply by 0, it becomes 0. But we skip 0.
                            # So we discard.
                            continue
                        new_prods.add(new_prod)
                    if new_key in new_dp:
                        new_dp[new_key].update(new_prods)
                    else:
                        new_dp[new_key] = new_prods
            
            # Also allow taking from the "virtual" empty state if we haven't used it yet?
            # No, we already used it for the first element. After that, we can only
            # continue from existing subsequences.
            # But wait: what if we want to skip the first element and start from the second?
            # The first element was processed, and we added states that take it. We also need
            # to allow skipping it. We did that by copying dp to new_dp at the start of the loop.
            # But for the first element, we didn't have a loop to copy from empty. We need to
            # also allow skipping the first element. So we need to process the first element
            # in a loop like the others, but with the empty state available.
            
            dp = new_dp
        
        # Wait, the above processing of the first element is wrong because we didn't allow
        # skipping it. We need to process all elements uniformly.
        # Let's redo: start with the empty state.
        # We'll use a special "empty" state that is always available to take from, but once
        # we take from it, we are no longer empty. We can just initialize dp with the empty
        # state and also keep a separate set for the empty state.
        
        # Actually, the simplest is: dp = {(0, offset): {1}}  # empty subsequence
        # Then for each num, we allow taking from any state in dp, including the empty one.
        # The empty state has product 1. Taking from it gives product = num.
        # This correctly models skipping: we copy dp to new_dp.
        # The only issue is that the empty state itself is in dp, and we might take from it
        # multiple times? No, because we only take one element per step. The empty state is
        # always available at each step? No, the empty state is the initial state. We should
        # only be able to take from it at the beginning. But if we copy it forward, we could
        # take from it later, which would mean we take an element after having taken nothing,
        # which is equivalent to starting fresh. That's actually correct: we can always choose
        # to start a new subsequence at any point. But we are looking for a single subsequence.
        # The DP that keeps all states (including empty) at each step is equivalent to: we
        # process elements left to right, and we can either skip an element or take it.
        # If we take it, we add it to the current subsequence. The "empty" state at step i
        # means we haven't taken any elements up to i. Taking from it at step i means we
        # take element i as the first element. This is exactly what we want.
        # So we should keep the empty state in dp and allow taking from it at every step.
        # But then the empty state itself is a valid answer? The empty state has product 1,
        # parity 0, sum 0. If k=0, this would be a valid answer, but the problem says
        # non-empty subsequence. So we must exclude the empty state from the final answer.
        # We can do this by only considering states that have at least one element.
        # How to know if a state is nonempty? We can track the length. Or we can maintain
        # a separate set for nonempty states.
        # Let's maintain two DP tables: one for empty (just a boolean if empty is reachable)
        # and one for nonempty. But empty is always reachable (we can always skip everything).
        # So we can just say: empty state is always available to take from.
        # For nonempty, we only add to it when we take an element.
        
        # Restart DP with this approach.
        
        # nonempty_dp: key = (parity, sum_idx), value = set of products (all <= limit)
        nonempty_dp = {}
        
        # For each element, we can:
        # 1. Skip it: keep all existing nonempty states.
        # 2. Take it: from existing nonempty states, or from the "empty" state (which is always available).
        #    From empty: product = num, parity = 1, sum = num.
        
        for num in nums:
            # Start with skipping: copy current nonempty states
            new_nonempty = {k: set(v) for k, v in nonempty_dp.items()}
            
            # From empty (virtual): taking num as the first element
            if num <= limit:
                key = (1, offset + num)
                if 0 <= key[1] < size:
                    if key in new_nonempty:
                        new_nonempty[key].add(num)
                    else:
                        new_nonempty[key] = {num}
            
            # From existing nonempty states
            for (par, s), prods in nonempty_dp.items():
                new_par = 1 - par
                sign = 1 if par == 0 else -1
                new_s = s + sign * num
                if 0 <= new_s < size:
                    new_key = (new_par, new_s)
                    new_prods = set()
                    for p in prods:
                        new_prod = p * num
                        if new_prod > limit:
                            # Discard invalid: cannot become valid again because we only multiply by positive ints
                            # (and we skip 0). So it's permanently invalid.
                            continue
                        new_prods.add(new_prod)
                    if new_key in new_nonempty:
                        new_nonempty[new_key].update(new_prods)
                    else:
                        new_nonempty[new_key] = new_prods
            
            # Prune: for each state, we can keep only products that are not "dominated".
            # A product p1 is dominated by p2 (p2 > p1) if p1 * 12 > limit? Not necessarily.
            # But we can do a simple pruning: if we have p1 < p2, and p1 * 12 > limit, then p1
            # can never be multiplied by any number >= 1 without exceeding limit, EXCEPT if
            # the number is 1 (p1*1 = p1 <= limit). So if we take a 1, p1 stays p1.
            # If we take a number >= 2, p1 * 2 <= p1*12? Not necessarily, p1*2 could be <= limit.
            # So p1 is not dead. We cannot prune safely.
            # However, we can prune: if we have p1 < p2, and p1 * 12 > limit, and we have seen
            # all numbers? We don't know future.
            # Let's just keep all products. The sets are small enough.
            
            nonempty_dp = new_nonempty
        
        target_s = offset + k
        if not (0 <= target_s < size):
            return -1
        
        ans = -1
        for parity in range(2):
            key = (parity, target_s)
            if key in nonempty_dp:
                prods = nonempty_dp[key]
                if prods:
                    max_prod = max(prods)
                    if max_prod > ans:
                        ans = max_prod
        
        return ans