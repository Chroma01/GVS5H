from typing import List

class Solution:
    def permute(self, n: int, k: int) -> List[int]:
        # Precompute factorials for P(n, k) calculation
        # P(n, k) = n! / (n-k)!
        # Since n <= 100, we can precompute factorials up to 100
        fact = [1] * (n + 1)
        for i in range(2, n + 1):
            fact[i] = fact[i - 1] * i
            
        def perm(n_val: int, k_val: int) -> int:
            if k_val > n_val:
                return 0
            return fact[n_val] // fact[n_val - k_val]

        # Count total odd and even numbers in 1..n
        cnt_odd = (n + 1) // 2
        cnt_even = n // 2
        
        # Calculate total alternating permutations starting with Odd
        # Pattern: O, E, O, E...
        # Number of odd positions: ceil(n/2)
        # Number of even positions: floor(n/2)
        odd_pos_count = (n + 1) // 2
        even_pos_count = n // 2
        
        # Ways to fill odd positions with available odds: P(cnt_odd, odd_pos_count)
        # Ways to fill even positions with available evens: P(cnt_even, even_pos_count)
        total_start_odd = perm(cnt_odd, odd_pos_count) * perm(cnt_even, even_pos_count)
        
        # Calculate total alternating permutations starting with Even
        # Pattern: E, O, E, O...
        # Number of even positions: ceil(n/2)
        # Number of odd positions: floor(n/2)
        even_pos_count_start_even = (n + 1) // 2
        odd_pos_count_start_even = n // 2
        
        total_start_even = perm(cnt_even, even_pos_count_start_even) * perm(cnt_odd, odd_pos_count_start_even)
        
        total_permutations = total_start_odd + total_start_even
        
        if k > total_permutations:
            return []
        
        # Determine starting parity
        # If k <= total_start_odd, start with Odd, else start with Even
        start_odd = k <= total_start_odd
        
        # Available numbers
        available_odd = list(range(1, cnt_odd + 1))
        available_even = list(range(2, cnt_even + 2))
        
        result = []
        current_odd_count = cnt_odd
        current_even_count = cnt_even
        
        # Determine the sequence of parities required
        # If start_odd is True: odd_pos_left = odd_pos_count, even_pos_left = even_pos_count
        # If start_even: even_pos_left = even_pos_count_start_even, odd_pos_left = odd_pos_count_start_even
        
        odd_pos_left = odd_pos_count if start_odd else odd_pos_count_start_even
        even_pos_left = even_pos_count if start_odd else even_pos_count_start_even
        
        # Current required parity for the next position
        # 1 for Odd, 0 for Even
        current_parity = 1 if start_odd else 0
        
        for _ in range(n):
            # Identify candidates based on current_parity
            if current_parity == 1:
                candidates = available_odd
                # If we pick an odd number:
                # We consume 1 odd position and 1 odd number.
                # Remaining odd positions: odd_pos_left - 1
                # Remaining even positions: even_pos_left
                # Remaining odds: current_odd_count - 1
                # Remaining evens: current_even_count
                
                # The next required parity will be Even (since we alternate)
                # So we need to fill 'even_pos_left' even positions and 'odd_pos_left - 1' odd positions.
                # Ways = P(remaining_odds, remaining_odd_positions) * P(remaining_evens, remaining_even_positions)
                
                ways = perm(current_odd_count - 1, odd_pos_left - 1) * perm(current_even_count, even_pos_left)
                
                # Iterate through candidates to find the k-th
                for num in candidates:
                    if k <= ways:
                        result.append(num)
                        available_odd.remove(num)
                        current_odd_count -= 1
                        current_parity = 0 # Next must be even
                        odd_pos_left -= 1
                        break
                    else:
                        k -= ways
            else:
                # current_parity == 0 (Even)
                candidates = available_even
                # If we pick an even number:
                # We consume 1 even position and 1 even number.
                # Remaining even positions: even_pos_left - 1
                # Remaining odd positions: odd_pos_left
                # Remaining evens: current_even_count - 1
                # Remaining odds: current_odd_count
                
                # Next required parity will be Odd
                ways = perm(current_odd_count, odd_pos_left) * perm(current_even_count - 1, even_pos_left - 1)
                
                for num in candidates:
                    if k <= ways:
                        result.append(num)
                        available_even.remove(num)
                        current_even_count -= 1
                        current_parity = 1 # Next must be odd
                        even_pos_left -= 1
                        break
                    else:
                        k -= ways
                        
        return result

# Test cases
sol = Solution()

# Example 1
n1, k1 = 4, 6
res1 = sol.permute(n1, k1)
print(f"Example 1: n={n1}, k={k1} -> {res1}")
# Expected: [3, 4, 1, 2]

# Example 2
n2, k2 = 3, 2
res2 = sol.permute(n2, k2)
print(f"Example 2: n={n2}, k={k2} -> {res2}")
# Expected: [3, 2, 1]

# Example 3
n3, k3 = 2, 3
res3 = sol.permute(n3, k3)
print(f"Example 3: n={n3}, k={k3} -> {res3}")
# Expected: []