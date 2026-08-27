class Solution:
    def minLength(self, s: str, numOps: int) -> int:
        n = len(s)
        if n == 0:
            return 0
        
        max_zero_run = 0
        max_one_run = 0
        current_zero = 0
        current_one = 0
        
        for char in s:
            if char == '0':
                current_zero += 1
                current_one = 0
                max_zero_run = max(max_zero_run, current_zero)
            else:
                current_one += 1
                current_zero = 0
                max_one_run = max(max_one_run, current_one)
        
        # We want to find the minimum x such that we can reduce both runs to <= x
        # using at most numOps.
        # For a run of length L, to get max segment <= x, we need k flips where:
        # ceil(L / (k+1)) <= x  =>  k+1 >= ceil(L/x)  =>  k >= ceil(L/x) - 1
        # ceil(L/x) can be computed as (L + x - 1) // x using integer division.
        
        # Iterate x from 1 upwards. The maximum possible answer is max(max_zero_run, max_one_run).
        # Since n <= 1000, a linear scan is efficient.
        
        for x in range(1, max(max_zero_run, max_one_run) + 1):
            # Calculate ops needed for zero run
            if max_zero_run > 0:
                k0 = (max_zero_run + x - 1) // x - 1
            else:
                k0 = 0
            
            # Calculate ops needed for one run
            if max_one_run > 0:
                k1 = (max_one_run + x - 1) // x - 1
            else:
                k1 = 0
            
            if k0 + k1 <= numOps:
                return x
        
        return max(max_zero_run, max_one_run)