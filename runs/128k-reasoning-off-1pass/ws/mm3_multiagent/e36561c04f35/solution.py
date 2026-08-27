import sys
import threading

def main():
    input = sys.stdin.read().split()
    idx = 0
    T = int(input[idx]); idx += 1
    out = []
    for _ in range(T):
        N = int(input[idx]); idx += 1
        A = []
        for i in range(N):
            A.append(int(input[idx])); idx += 1
        
        # Compress to runs
        runs = []
        for x in A:
            if not runs or runs[-1] != x:
                runs.append(x)
        m = len(runs)
        
        # Map values to ranks 1..M based on order of first appearance
        val_to_rank = {}
        rank = 0
        for x in A:
            if x not in val_to_rank:
                rank += 1
                val_to_rank[x] = rank
        M = rank
        
        # For each value, find first and last run index
        first_run = {}
        last_run = {}
        for i, v in enumerate(runs):
            if v not in first_run:
                first_run[v] = i
            last_run[v] = i
        
        # For each run, we need to know how many distinct values with greater rank
        # are "active" (their interval contains the current run index).
        # We process runs left to right and maintain a BIT of active values.
        # 
        # The answer is M (for deletions) + sum over runs of (count of active values with rank > current rank).
        # 
        # However, to make this work correctly for all cases (including alternating patterns),
        # we need a different approach. The correct solution is:
        # 
        # We count the number of pairs (i, j) with i < j such that:
        #   - runs[i] > runs[j] in value
        #   - there is no run between i and j with value strictly between runs[j] and runs[i]
        # 
        # This is equivalent to counting "inversions" in the run sequence where we only count
        # an inversion if no intermediate run has a value between the two.
        # 
        # Actually, the simplest correct formulation is:
        # Answer = M + (number of pairs of runs (i, j) with i < j where runs[i] > runs[j] 
        #                and runs[i]'s value has a later last occurrence than runs[j]'s value)
        # 
        # No wait, the correct answer for the problem is:
        # We process the runs. For each run with value v, we look at all values w > v that 
        # have appeared in a run before the current one and whose last run is at or after 
        # the current run. The number of such w is added to the answer.
        # 
        # But we also need to add the number of such w that will appear in runs after the 
        # current one but whose first run is before the current run and whose last run is 
        # after the current run... this is getting complex.
        # 
        # The definitive correct solution uses the following insight:
        # The minimum number of operations equals the number of distinct values plus the 
        # number of "inversions" in the compressed run sequence, where an inversion between 
        # run i and run j (i < j) is counted if runs[i] > runs[j] and the values runs[i] and 
        # runs[j] "interleave" in a specific way.
        # 
        # The precise definition: an inversion is counted for a pair of values (u, v) with 
        # u > v if the first occurrence of u is before the first occurrence of v AND the 
        # last occurrence of u is after the last occurrence of v.
        # 
        # This counts "nesting" where a larger value completely surrounds a smaller value.
        
        # Let me implement the nesting approach
        nested_count = 0
        for u in val_to_rank:
            for v in val_to_rank:
                if u == v:
                    continue
                if val_to_rank[u] > val_to_rank[v]:
                    # u has higher rank (appears later in value ordering? No, rank is order of first appearance)
                    # We need u > v in VALUE
                    if u > v:  # Check actual value comparison
                        if first_run[u] < first_run[v] and last_run[u] > last_run[v]:
                            nested_count += 1
        
        ans = M + nested_count
        
        out.append(str(ans))
    
    sys.stdout.write('\n'.join(out) + '\n')

threading.Thread(target=main).start()