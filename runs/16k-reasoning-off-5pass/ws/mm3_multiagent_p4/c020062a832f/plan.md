We need inversion counts for each cyclic shift `k` of `A[i]` modulo `M`. For each k, define B_i = (A_i + k) mod M. We can write the inversion count for a given k as:

inv(k) = inv0 - X(k) + Y(k) + Z(k)

where:
- inv0 is the inversion count of the original A (k=0)
- X(k) = number of pairs (i<j) with A_i <= A_j but (A_i+k) mod M > (A_j+k) mod M (i.e., pairs that cross the wrap-around boundary and become non-inversions when we add k)
- Y(k) = number of pairs (i<j) with A_i > A_j but (A_i+k) mod M <= (A_j+k) mod M (i.e., pairs that stop being inversions)
- Z(k) = number of pairs (i<j) with A_i < A_j and (A_i+k) mod M > (A_j+k) mod M (new inversions created)

Equivalently, after adding k, only pairs where one of A_i, A_j is < k and the other is >= k can have their relative order change. Let cnt_ge = number of i with A_i >= k, cnt_lt = number with A_i < k. For k>0:
- inv(k) = inv(k-1) - 2*cnt_ge[k] + N

This is a known O(N+M) approach. We maintain inv as we increment k from 0 to M-1. cnt_ge[k] = number of A_i in [k, M-1] = N - (number of A_i < k). We can precompute freq of each value and prefix sums.

Algorithm:
1. Read N, M, array A.
2. Compute inv0 via BIT (Fenwick) on values 0..M-1.
3. Compute freq[v] for v in 0..M-1.
4. Compute prefix sum pref[k] = number of elements < k = pref[k-1] + freq[k-1].
5. For each k from 1 to M:
   - cnt_ge = N - pref[k]  (elements >= k)
   - inv = inv - 2*cnt_ge + N
   - Output inv

Start with inv0 for k=0, then compute for k=1..M-1. (For k=M it's same as k=0.)