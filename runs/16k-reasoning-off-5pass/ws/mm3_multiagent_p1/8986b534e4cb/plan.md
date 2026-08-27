We need to determine feasibility of assigning integer edge weights on a line of N towns so that a given subset of journeys (start S_i → end T_i) have stamina 0 at endpoints and positive at interior towns.

Key observations:
- Each person’s path is a contiguous interval [min(S,T), max(S,T)].
- The stamina profile is determined by cumulative sum of w along the interval, with start at 0.
- Required: cumulative sum at both endpoints is 0, and strictly positive at all interior points.

For a fixed interval of length L = |S-T|, the feasibility of choosing w (independent of other intervals) reduces to existence of a sequence of L integers w_1..w_L such that:
  - Partial sums P_0=0, P_k>0 for 1≤k<L, P_L=0.
This is a classic condition: the sequence of partial sums forms a Dyck-like path staying strictly above zero except at ends. This is possible iff the interval length is **even** (L must be even). Because sum of L signed integers equaling zero with all partial sums positive forces even number of steps (alternating +1 and -1 works).

Thus each person i requires |S_i - T_i| to be even. If any selected person has odd distance, answer is No immediately.

If all distances are even, can we always assign weights to satisfy all simultaneously? Not necessarily — overlapping intervals impose constraints on shared edges.

But note: we can set edge weights independently per person, and assign a global weight to each road. The global assignment must work for all selected people simultaneously.

The structure: Each person i requires that along their interval, the cumulative sum stays >0 except at ends. This is a linear inequality system on the w_j's.

Observation: If we set w_j = (-1)^{j} (alternating 1,-1,1,-1,...), then the partial sum pattern repeats with period 2: after even number of steps we return to 0, after odd steps we are at 1. This satisfies all intervals of even length: interior points are at 1 > 0, endpoints at 0. So this single global assignment works for **all** even-length intervals.

Wait, but is that true? Consider interval from town 2 to town 5 (length 3, odd) - we don't care. Even length intervals: start at s, end at s+2k. Partial sum at interior point t: sum_{j=s}^{t-1} w_j. With alternating w starting with w_1=1, w_2=-1, etc., the sum from s to s+2k-1 is 0 (since pairs cancel). The sum at an odd offset is 1. Indeed, partial sums depend only on parity of offset: positive (1) at odd offsets, 0 at even. So any even-length interval has positive interior stamina (1) and 0 at both ends. So **any set of people whose distances are all even can be satisfied with the same alternating assignment**.

Therefore, the answer for a query is "Yes" iff all persons in [L,R] have even |S_i - T_i|.

This is a simple range query: precompute an array even[i] = 1 if |S_i - T_i| is even, else 0. For each query [L,R], check if sum of even[L..R] == (R-L+1). If yes, "Yes", else "No".

We need to support up to M=2e5, Q=2e5, so prefix sums work in O(1) per query.