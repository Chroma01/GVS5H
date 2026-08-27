import sys

MOD = 998244353

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    S = data[2].strip()
    # Precompute next_state[i][c] = new LCS length when current LCS = i and we append character c
    # i ranges 0..N
    # We'll compute using DP over positions of S
    # For each character c, we compute an array best[j] for j=0..N representing the LCS length
    # between the prefix S[0..j-1] and the processed string (including the new character c).
    # Actually we need transition from a known LCS value i (which is the LCS between processed string and full S)
    # to new LCS value after appending c.
    # Since N is small, we can compute for each c a DP that given current LCS value i (0..N) returns new LCS.
    # Approach: For each c, compute an array dp_pos[j] = LCS length between processed string and S[0..j-1] after appending c.
    # But we need to know the LCS with full S, not just prefix. However we can compute the transition by considering
    # the effect of appending c to the whole string.
    # Standard LCS DP: let f[j] be LCS length between processed string and S[0..j-1] before adding c.
    # After adding c, new_f[j] = max( f[j], f[j-1] + (S[j-1]==c) ).
    # But we don't have f[j] individually; we only know the overall LCS = max_j f[j] = i.
    # However we can reconstruct the necessary information: we need to know for each j the value f[j] that is consistent with overall LCS = i.
    # Since N is tiny, we can enumerate all possible "profiles" f[0..N] that are achievable and have max = i.
    # But that's too many (exponential). Instead we can compute the transition directly using DP over the whole S.
    # Alternative: For each c, we can compute a DP that given the current LCS value i returns the new LCS value.
    # We can do this by simulating the LCS DP with the knowledge that the current LCS = i.
    # Since i is the maximum over j of f[j], we can consider the worst-case scenario? Actually we need the exact transition.
    # However we can compute the transition by considering the effect of adding c on the LCS DP table.
    # The LCS DP table is a matrix of size (len_processed+1) x (N+1). Adding a new character c corresponds to updating the last row.
    # The new LCS value is the maximum over j of the updated last row.
    # The updated last row depends on the previous last row (which we don't know fully) but we know its maximum = i.
    # However the transition might depend on the exact distribution of values in the last row.
    # Example: S = "ab", processed string = "a". The last row (for processed string length 1) is [1,1,0]? Actually:
    #   dp[0][*] = 0
    #   dp[1][0] = 0
    #   dp[1][1] = 1 (since S[0]='a' matches)
    #   dp[1][2] = 1 (since we can match 'a' with first char)
    # So max = 1. Now appending 'b': new row becomes:
    #   new[0] = 0
    #   new[1] = max(old[1], old[0]+0) = max(1,0)=1
    #   new[2] = max(old[2], old[1]+1) = max(1, 1+1)=2
    # So new LCS = 2.
    # If processed string was "b", last row: [0,0,1]? Actually:
    #   dp[1][1] = 0 (no match)
    #   dp[1][2] = 1 (match 'b' with second char)
    # max = 1. Appending 'b': new row:
    #   new[1] = max(0,0)=0
    #   new[2] = max(1, 0+1)=1
    # So new LCS = 1.
    # So transition depends on the exact last row, not just the max.
    # Therefore we need to keep track of the entire last row (or at least enough information) as state.
    # Since N ≤ 10, the last row has N+1 entries, each between 0 and N. That's at most (N+1)^(N+1) possibilities, too many.
    # But we can compress: the last row is non-decreasing? Actually LCS DP ensures that dp[i][j] is non-decreasing in j for fixed i.
    # Also dp[i][j] - dp[i][j-1] is 0 or 1. So the row is a sequence of integers from 0 to i, non-decreasing, with increments of 0 or 1.
    # The number of such sequences is C(N+1, i) or something? Actually it's the number of ways to choose i positions among N+1 to increase.
    # Since i ≤ N ≤ 10, the number of possible rows for a given i is at most sum_{k=0..i} C(N+1, k) which is manageable.
    # But we need to consider all i from 0..N. The total number of possible rows is sum_{i=0..N} C(N+1, i) = 2^(N+1) = at most 2048 for N=10.
    # That's small! So we can enumerate all possible "profiles" (last rows) as states.
    # However we also need to know the current LCS value (max of row) which is i. So we can group states by i.
    # But we can just treat the entire row as state, and compute transition for each character c.
    # Number of states: at most 2^(N+1) = 2048. For each state and each character (26), we compute next state.
    # Then DP over M steps: dp[state] = count. After M steps, sum over states whose max = k.
    # Complexity: O(M * 2^(N+1) * 26) = 100 * 2048 * 26 ≈ 5.3 million, fine.
    # Implementation: Represent a row as a tuple of length N+1. We can pack into an integer using base (N+1) or bitmask.
    # Since each entry is between 0 and N, we can pack into an integer using (N+1) bits per entry? Actually we can use a small integer encoding.
    # Simpler: use tuple as key in dictionary. Since number of states is small, dictionary overhead is fine.
    # But we need to precompute transitions for all possible rows and all characters.
    # Let's define a row as a list of length N+1: row[j] = LCS length between processed string and prefix S[0..j-1].
    # Properties: row[0] = 0, row is non-decreasing, row[j] - row[j-1] ∈ {0,1}, row[N] = current LCS value.
    # We can generate all such rows recursively.
    # Then for each row and each character c, compute new_row:
    #   new_row[0] = 0
    #   for j in 1..N:
    #       if S[j-1] == c:
    #           new_row[j] = max(row[j], row[j-1] + 1)
    #       else:
    #           new_row[j] = max(row[j], row[j-1])
    # Actually the standard LCS DP update for adding a character to the second string:
    #   new_dp[j] = max(old_dp[j], old_dp[j-1] + (S[j-1]==c))
    # But careful: The DP table is for the processed string (first string) and S (second string). When we append a character to the processed string, we are adding a row to the DP table.
    # The recurrence is:
    #   new_row[0] = 0
    #   for j from 1 to N:
    #       if S[j-1] == c:
    #           new_row[j] = max(row[j], row[j-1] + 1)
    #       else:
    #           new_row[j] = max(row[j], row[j-1])
    # This is correct.
    # Then we take new_row as the next state.
    # We also need to ensure that new_row satisfies the properties (it will automatically).
    # So we can precompute transition dict: trans[row_tuple][c] = new_row_tuple.
    # Then DP: dp = {initial_row: 1} where initial_row is all zeros (length N+1).
    # For each step in M:
    #   new_dp = defaultdict(int)
    #   for state, cnt in dp.items():
    #       for c in range(26):
    #           nxt = trans[state][c]
    #           new_dp[nxt] = (new_dp[nxt] + cnt) % MOD
    #   dp = new_dp
    # After M steps, answer for k is sum of dp[state] where max(state) == k.
    # Since N is small, we can store states as tuples.
    # Let's implement.

    # Generate all possible rows (profiles) that can appear.
    # A row is a tuple of length N+1, with row[0]=0, non-decreasing, increments 0 or 1.
    # We can generate by recursion: start with [0], then for each next position j from 1 to N, we can either keep same value or increase by 1, but cannot exceed j (since max LCS for prefix length j is j).
    # Actually the maximum possible value at position j is min(j, N) but since we are building from left to right, we can just allow increase by 1 at most.
    # So we generate all sequences of length N+1 where a[0]=0, a[j] ∈ {a[j-1], a[j-1]+1}.
    # This yields exactly 2^N possible rows? Let's count: at each of the N steps (j=1..N), we have 2 choices (increase or not). So 2^N rows.
    # But wait: is every such sequence achievable as a row of LCS DP? Yes, because we can construct a processed string that yields that row.
    # For example, to get a specific row, we can choose characters appropriately.
    # So total states = 2^N. For N=10, that's 1024. Even better.
    # Actually we need to consider that the row must be consistent with some processed string. But any non-decreasing sequence with increments 0 or 1 is achievable.
    # So we can generate all 2^N rows.

    # Let's generate all rows as tuples.
    from collections import defaultdict

    all_rows = []
    # recursion: current list, current value
    def gen(idx, current_val, row):
        if idx == N:
            row.append(current_val)
            all_rows.append(tuple(row))
            row.pop()
            return
        # option 1: keep same
        row.append(current_val)
        gen(idx+1, current_val, row)
        row.pop()
        # option 2: increase by 1 (if possible)
        if current_val + 1 <= N: # can increase
            row.append(current_val+1)
            gen(idx+1, current_val+1, row)
            row.pop()
    gen(0, 0, [])

    # Now precompute transitions for each row and each character.
    # trans[row][c] = new_row
    # We'll store as dict of dict: trans[row_tuple][c] = new_row_tuple
    # Since number of rows is small, we can compute on the fly or precompute.
    # Precompute for speed.
    trans = {}
    S_chars = S
    for row in all_rows:
        trans[row] = [None]*26
        for c_idx in range(26):
            c = chr(ord('a') + c_idx)
            new_row = [0]*(N+1)
            new_row[0] = 0
            # row is tuple, we need to access row[j]
            for j in range(1, N+1):
                if S_chars[j-1] == c:
                    new_row[j] = max(row[j], row[j-1] + 1)
                else:
                    new_row[j] = max(row[j], row[j-1])
            trans[row][c_idx] = tuple(new_row)

    # Initial state: row of all zeros.
    init_row = tuple([0]*(N+1))
    dp = {init_row: 1}
    for _ in range(M):
        new_dp = defaultdict(int)
        for state, cnt in dp.items():
            for c_idx in range(26):
                nxt = trans[state][c_idx]
                new_dp[nxt] = (new_dp[nxt] + cnt) % MOD
        dp = new_dp

    # Now compute answers for k=0..N
    ans = [0]*(N+1)
    for state, cnt in dp.items():
        k = state[N]  # max LCS value is the last entry
        ans[k] = (ans[k] + cnt) % MOD

    print(' '.join(str(ans[k]) for k in range(N+1)))

if __name__ == "__main__":
    solve()