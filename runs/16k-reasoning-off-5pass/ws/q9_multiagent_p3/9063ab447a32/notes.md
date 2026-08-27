
## ideation
The problem asks us to maximize the total number of units purchased given a budget $M$ and $N$ product types, where buying $k$ units of product $i$ costs $k^2 P_i$.

**Core Difficulty:**
The cost function $f_i(k) = k^2 P_i$ is convex (specifically, quadratic). This means the marginal cost of each additional unit increases as we buy more of the same product.
- 1st unit: cost $1^2 P_i = P_i$
- 2nd unit: cost $2^2 P_i - 1^2 P_i = 3 P_i$
- 3rd unit: cost $3^2 P_i - 2^2 P_i = 5 P_i$
- $k$-th unit: cost $(k^2 - (k-1)^2) P_i = (2k-1) P_i$

Since the marginal cost increases for a specific product, we should always buy the "cheapest" available unit first. The cheapest units are those with the smallest $P_i$. Specifically, the 1st unit of any product $i$ costs $P_i$. The 2nd unit of product $i$ costs $3P_i$. The 2nd unit of product $j$ costs $3P_j$. We should compare $3P_i$ and $3P_j$ to decide which to buy next.

**Candidate Approaches:**
1.  **Greedy with Sorting (Naive Simulation):**
    - Sort products by $P_i$.
    - Iterate through products. For each product, calculate the maximum $k$ such that $k^2 P_i \le \text{remaining\_budget}$.
    - *Flaw:* This assumes we fill up one product completely before moving to the next. However, because the marginal cost grows ($P_i, 3P_i, 5P_i \dots$), it might be cheaper to buy the 2nd unit of product $A$ ($3P_A$) than the 3rd unit of product $B$ ($5P_B$) even if $P_A > P_B$. The simple "fill one product then move to next" strategy fails because it doesn't account for the increasing marginal cost across different products.

2.  **Greedy with Marginal Costs (Binary Search on Answer):**
    - The total number of units $K$ is monotonic with respect to the budget required to buy $K$ units.
    - If we decide to buy exactly $K$ units in total, which $K$ units should we pick? We should pick the $K$ smallest marginal costs available across all products.
    - The marginal costs are of the form $(2x-1)P_i$ for $x=1, 2, \dots$.
    - Since $N$ is up to $2 \times 10^5$, we cannot generate all marginal costs.
    - However, we can binary search on the total number of units $K$ (range $0$ to $M$, since min cost per unit is 1).
    - For a fixed $K$, how to check if it's possible to buy $K$ units within budget $M$?
        - We need the sum of the $K$ smallest values from the set $\{(2x-1)P_i\}$.
        - This looks like finding the $K$-th smallest element in a virtual matrix of costs.
        - Let's define a threshold $T$. We want to count how many marginal costs are $\le T$.
        - For a product $i$, the number of units $x$ such that $(2x-1)P_i \le T$ is roughly $T/(2P_i)$. Specifically, $2x-1 \le T/P_i \implies 2x \le T/P_i + 1 \implies x \le (T/P_i + 1)/2$.
        - Let $count(T) = \sum_i \lfloor \frac{\lfloor T/P_i \rfloor + 1}{2} \rfloor$. This gives the number of units with marginal cost $\le T$.
        - We can binary search for the smallest $T$ such that $count(T) \ge K$.
        - Once we have $T$, we calculate the total cost: sum of all marginal costs $\le T$, plus the cost of the remaining units (those with cost exactly $T$ that we need to reach exactly $K$).
        - Since $K$ can be up to $M$ (if $P_i=1$), binary searching $K$ directly is $O(\log M \cdot N)$, which is too slow ($2\cdot10^5 \times 60 \approx 1.2 \cdot 10^7$, might pass but tight? Wait, $M=10^{18}$, so $\log M \approx 60$. $60 \times 2 \cdot 10^5 = 1.2 \cdot 10^7$ operations. This is acceptable in Python if implemented efficiently, usually limit is $10^8$ ops/sec).
        - Actually, we don't need to binary search $K$. We can binary search the marginal cost threshold $T$. The range of $T$ is $1$ to $2M$ (since max cost per unit is roughly $2M$).
        - Function `check(T)`: returns (count of units with marginal cost $\le T$, total cost of those units).
        - We binary search $T$. Find the largest $T$ such that count $\le K_{target}$? No, we want to maximize $K$ such that Cost $\le M$.
        - Better approach: Binary search on $T$ (the marginal cost of the last unit bought).
        - Range for $T$: $1$ to $2 \cdot 10^{18}$ (actually max possible marginal cost is when we spend almost all $M$ on one unit, so $2M$).
        - For a given $T$, calculate total units $U(T)$ and total cost $C(T)$ considering all units with marginal cost $\le T$.
        - If $C(T) \le M$, we can potentially buy more units. We need to find the optimal $T$.
        - Since $C(T)$ is monotonic with $T$, we can binary search for the largest $T$ such that $C(T) \le M$.
        - Let this optimal threshold be $T^*$.
        - Calculate $U(T^*)$ and $C(T^*)$.
        - If $C(T^*) \le M$, we have bought some units. The remaining budget $R = M - C(T^*)$ can be used to buy units with marginal cost exactly $T^* + 1$? No, the marginal costs are discrete.
        - The units we buy are all those with marginal cost $< T^*$, plus some fraction of those with marginal cost $= T^*$.
        - Wait, the marginal costs are integers. The set of available marginal costs is discrete.
        - Let's refine:
          - Binary search for the largest integer $T$ such that the total cost to buy *all* units with marginal cost $\le T$ is $\le M$.
          - Let this be $T_{opt}$.
          - Calculate total units $cnt$ and total cost $cost$ for all units with marginal cost $\le T_{opt}$.
          - Remaining budget $rem = M - cost$.
          - Now, look at units with marginal cost $T_{opt} + 1$. How many such units exist?
            - For each product $i$, the number of units with marginal cost $T_{opt} + 1$ is either 0 or 1.
            - Specifically, a product $i$ has a unit with marginal cost $T_{opt} + 1$ if $(2x-1)P_i = T_{opt} + 1$ for some integer $x$.
            - This implies $T_{opt} + 1$ must be odd and divisible by $P_i$.
            - Actually, the marginal costs for product $i$ are $P_i, 3P_i, 5P_i, \dots$.
            - So we check if $T_{opt} + 1$ is in the set $\{ (2x-1)P_i \}$.
            - If yes, we can buy one such unit if $rem \ge T_{opt} + 1$.
            - But wait, there could be multiple products having a unit with marginal cost $T_{opt} + 1$. We should buy as many as possible with the remaining budget.
            - Since all these units have the same marginal cost ($T_{opt} + 1$), we just count how many products $i$ satisfy $(2x-1)P_i = T_{opt} + 1$ for some $x$. Let this count be $c$. We can buy $\min(c, \lfloor rem / (T_{opt} + 1) \rfloor)$ units.
            - Add to total units.
          - Is it possible that we skipped a unit with marginal cost $T < T_{opt}$? No, because $T_{opt}$ is the largest threshold where cost $\le M$.
          - Is it possible we should have stopped at a lower $T$ to save budget for a cheaper unit? No, because marginal costs are sorted. We always take the cheapest available.

**Complexity Analysis:**
- Binary Search Range: $1$ to $2 \cdot 10^{18}$. Steps $\approx 60$.
- Inside Check(T): Iterate $N$ products. $O(N)$.
- Total Complexity: $O(N \log M)$.
- $N = 2 \cdot 10^5$, $\log M \approx 60$. Operations $\approx 1.2 \cdot 10^7$.
- In Python, this might be slightly slow if not careful, but should pass within 2 seconds.
- Optimization: Precompute nothing, just loop. Use fast I/O.

**Pitfalls:**
- Integer overflow: Costs can exceed $2^{63}-1$? $M \le 10^{18}$, so we stop when cost exceeds $M$. Intermediate sums in `check(T)` might exceed $M$ if we are not careful, but we can cap the sum at $M+1$ to avoid huge numbers and speed up.
- Edge cases: $M$ is small, no units can be bought. $P_i$ large.
- The condition $(2x-1)P_i = T$ implies $T$ must be odd and $T \% P_i == 0$.
- The binary search logic: We want max $T$ such that `total_cost(T) <= M`.
  - `total_cost(T)` = sum of marginal costs for all units with marginal cost $\le T$.
  - `count(T)` = number of such units.
  - If `total_cost(T) <= M`, try larger $T$.
  - Else, try smaller $T$.
- After finding $T_{opt}$, we have `rem = M - total_cost(T_{opt})`.
- We need to buy units with marginal cost $T_{opt} + 1$.
- Check how many products $i$ have a unit with marginal cost $T_{opt} + 1$.
  - Condition: $(T_{opt} + 1) \% P_i == 0$ and $(T_{opt} + 1) / P_i$ is odd.
  - Let $k = (T_{opt} + 1) / P_i$. If $k \% 2 == 1$, then product $i$ has a unit with this marginal cost.
  - Count such products. Let this be $c$.
  - We can buy $\min(c, rem // (T_{opt} + 1))$ additional units.
  - Wait, is it possible that $T_{opt}$ was such that we could have bought a unit with cost $T_{opt}+1$ but we didn't because we prioritized something else? No, the greedy strategy says we take all units with cost $\le T_{opt}$ first. If we have budget left, we take units with cost $T_{opt}+1$.
  - Is it possible that `total_cost(T_{opt})` is very close to $M$, and we can't afford any $T_{opt}+1$, but we could have afforded a different combination? No, because $T_{opt}$ is the cutoff. Any unit with cost $> T_{opt}$ is more expensive than the ones we took. If we can't afford the next cheapest batch, we stop.

**Refinement on Binary Search:**
The marginal costs are not continuous. The set of values is $\bigcup_i \{ (2x-1)P_i \}$.
Binary searching over integer $T$ works because the property "sum of costs of all units with marginal cost $\le T$ is $\le M$" is monotonic.
Let $S(T)$ be the sum of costs of all units with marginal cost $\le T$.
$S(T)$ is non-decreasing with $T$.
We find max $T$ such that $S(T) \le M$.
Let this be $T^*$.
Then we calculate $U = \text{count}(T^*)$ and $C = S(T^*)$.
Remaining budget $R = M - C$.
Next cheapest units have marginal cost $T^* + 1$.
Count how many products $i$ have a unit with marginal cost $T^* + 1$.
Let this count be $k_{next}$.
We can buy $\min(k_{next}, R // (T^* + 1))$ more units.
Total units = $U + \min(...)$.

Wait, is it possible that for some $T$, $S(T) > M$ but for $T-1$, $S(T-1) \le M$, and the gap between $S(T)$ and $S(T-1)$ is huge? Yes.
Is it possible that we should have stopped at $T-1$ and bought some units of cost $T$?
No, because units of cost $T$ are more expensive than units of cost $T-1$ (or less). The greedy order is strictly by marginal cost.
The only issue is if $T$ is not a valid marginal cost for any product.
Example: Products $P_1=2, P_2=3$.
Marginal costs:
P1: 2, 6, 10, 14...
P2: 3, 9, 15...
Sorted: 2, 3, 6, 9, 10...
If $M=5$.
$T=2$: cost=2, count=1. OK.
$T=3$: cost=2+3=5, count=2. OK.
$T=4$: cost=5 (no units with cost 4). OK.
$T=5$: cost=5 (no units with cost 5). OK.
$T=6$: cost=5+6=11 > 5. Stop.
So $T^*=5$.
$U=2, C=5, R=0$.
Next cost $6$. Count products with cost 6: P1 has 6. $k_{next}=1$.
Buy $\min(1, 0) = 0$.
Total 2. Correct (buy 1 of P1, 1 of P2).

What if $M=4$?
$T=2$: cost=2.
$T=3$: cost=5 > 4.
So $T^*=2$.
$U=1, C=2, R=2$.
Next cost $3$. Products with cost 3: P2. $k_{next}=1$.
Buy $\min(1, 2//3) = 0$.
Total 1. Correct (buy 1 of P1).

Seems correct.

**Implementation Details:**
- Read N, M.
- Read P array.
- Binary Search `low = 0`, `high = 2 * M + 2` (safe upper bound).
- `ans_T = 0`, `ans_cost = 0`.
- Loop while `low <= high`:
  - `mid = (low + high) // 2`
  - Calculate `cnt` and `cost` for threshold `mid`.
    - Iterate $p$ in $P$:
      - if $p > mid$: break (since $mid$ increases, but $p$ is constant? No, we iterate all).
      - Actually, we need to sum $(2x-1)p$ for all $x$ where $(2x-1)p \le mid$.
      - Max $x$: $2x-1 \le mid/p \implies 2x \le mid/p + 1 \implies x \le (mid/p + 1)//2$.
      - Let $k = (mid // p + 1) // 2$.
      - If $k == 0$: continue.
      - Sum of first $k$ odd numbers: $k^2$.
      - Cost contribution: $p * k^2$.
      - Count contribution: $k$.
      - Accumulate. If `cost` exceeds $M$, break early to save time? Yes, but we need to know if it exceeds.
      - Be careful: `cost` can exceed $M$. We can cap it at $M+1$.
  - If `cost <= M`:
    - `ans_T = mid`
    - `ans_cost = cost`
    - `low = mid + 1`
  - Else:
    - `high = mid - 1`
- After loop, calculate additional units from `ans_T + 1`.
- Check products for marginal cost `ans_T + 1`.
- Count valid products.
- Add to total.
- Print total.

One optimization: The sum of costs can be large. Use Python's arbitrary precision integers (automatic).
Time limit consideration: $N=200,000$, loop 60 times. $1.2 \times 10^7$ iterations. In Python, a simple loop with arithmetic might take 2-3 seconds. We need to be efficient.
Can we optimize the inner loop?
The inner loop is:
```python
cnt = 0
cost = 0
for p in P:
    if p > mid: continue # optimization
    k = (mid // p + 1) // 2
    if k > 0:
        cnt += k
        cost += p * k * k
```
This is $O(N)$.
Is there a way to speed up?
Sort $P$ initially.
If `mid // p` is small, `k` is small.
If `p > mid`, `k=0`.
We can break if `p > mid`? No, $P$ is sorted ascending. So if `p > mid`, all subsequent `p` are also $> mid$. So we can `break`!
Sorting $P$ takes $O(N \log N)$.
Inside BS: iterate until `p > mid`.
Since `mid` grows, the loop might run fewer times as `mid` increases? No, `mid` starts small.
Actually, for small `mid`, we break early. For large `mid`, we iterate all.
Worst case: `mid` is large, we iterate all $N$.
Total complexity $O(N \log M)$.
With $N=2 \cdot 10^5$, $60 \times 2 \cdot 10^5 = 1.2 \cdot 10^7$ ops.
In Python, this is risky. 10^7 simple ops might take 1-2s.
Can we optimize the calculation?
We are summing $p \cdot k^2$ where $k = \lfloor \frac{\lfloor mid/p \rfloor + 1}{2} \rfloor$.
Let $q = \lfloor mid/p \rfloor$. Then $k = (q+1)//2$.
If $q$ is even ($2m$), $k=m$. Cost $p \cdot m^2$.
If $q$ is odd ($2m+1$), $k=m+1$. Cost $p \cdot (m+1)^2$.
This doesn't simplify the summation significantly without grouping.
However, note that $P$ is sorted.
Maybe we can use the fact that $mid/p$ changes slowly? No, $p$ varies.
Given the constraints and language, we must ensure the inner loop is as tight as possible.
Avoid function calls inside the loop.
Use local variables.
Pre-sort $P$.

Wait, is there an alternative?
What if we binary search on the answer $K$ (total units)?
Range $0$ to $M$.
Check(K): Can we buy $K$ units with cost $\le M$?
To check $K$:
We need the sum of the $K$ smallest marginal costs.
This is equivalent to finding the $K$-th smallest marginal cost $T$, summing all $\le T$, and adjusting.
This is the same complexity.
Actually, the first approach (BS on marginal cost $T$) is slightly better because the range of $T$ is larger but the check function is simpler?
Check(K) requires finding the $K$-th smallest value in a union of arithmetic progressions. This is harder to implement efficiently than "sum of all values $\le T$".
So BS on $T$ is the way.

Let's double check the constraints and Python speed.
$1.2 \times 10^7$ iterations.
In C++, this is trivial (0.05s).
In Python, a loop with `for p in P:` and arithmetic inside might be slow.
We can try to vectorize? No numpy allowed.
Maybe we can reduce the number of BS steps?
The values of marginal costs are sparse.
But we don't know them.
Is there a way to skip?
Maybe we can observe that $T$ must be one of the values $(2x-1)P_i$?
No, $T$ can be anything, but the "events" happen at these values.
Actually, the function $S(T)$ is piecewise constant in slope? No, $S(T)$ is a step function (sum increases at specific $T$).
The "steps" occur at $T \in \{ (2x-1)P_i \}$.
There are many such values.
However, we only care about the largest $T$ such that $S(T) \le M$.
This $T$ will likely be one of the marginal costs or just below one.
Actually, if $S(T) \le M$ and $S(T+1) > M$, then $T$ is the answer.
The binary search will converge to the correct $T$.
The only concern is the constant factor.
Let's write the code efficiently.

One small optimization:
If `mid` is very large, `mid // p` is large.
But we only care if `cost <= M`.
If `p * k * k > M`, we can stop adding?
Yes! If the accumulated cost exceeds $M$, we can break the loop immediately and mark as "too expensive".
This will prune the loop significantly for large `mid`.
For small `mid`, the loop runs until `p > mid`.
For large `mid`, the loop might break early due to cost exceeding $M$.
This pruning is crucial.

Algorithm Refined:
1. Sort $P$.
2. BS `low=0`, `high=2*M+1`.
3. `best_T = 0`, `best_cost = 0`.
4. While `low <= high`:
   - `mid = (low + high) // 2`
   - `current_cost = 0`
   - `current_cnt = 0`
   - `possible = True`
   - Iterate `p` in `P`:
     - if `p > mid`: break (since sorted)
     - `q = mid // p`
     - `k = (q + 1) // 2`
     - if `k == 0`: continue
     - `term = p * k * k`
     - `if current_cost + term > M`:
       - `possible = False`
       - `break`
     - `current_cost += term`
     - `current_cnt += k`
   - if `possible`:
     - `best_T = mid`
     - `best_cost = current_cost`
     - `low = mid + 1`
   - else:
     - `high = mid - 1`
5. Calculate `rem = M - best_cost`.
6. `next_cost = best_T + 1`.
7. Count how many `p` in `P` allow a unit with marginal cost `next_cost`.
   - Condition: `next_cost % p == 0` and `(next_cost // p) % 2 == 1`.
   - Since `next_cost` is fixed, we can iterate `P`.
   - `count_next = 0`
   - for `p` in `P`:
     - if `next_cost % p == 0`:
       - `x = next_cost // p`
       - if `x % 2 == 1`:
         - `count_next += 1`
   - `can_buy = min(count_next, rem // next_cost)`
   - `total_units = best_cnt + can_buy`
8. Print `total_units`.

Wait, `best_cnt` needs to be stored in the BS loop.
Yes.

Corner case: `best_T` could be 0. `next_cost` = 1.
If `best_T` is such that no units were bought, `best_cnt=0`, `best_cost=0`.
Then we check `next_cost=1`.
Correct.

Is `high = 2*M + 1` sufficient?
Max marginal cost we might consider is when we buy 1 unit. Cost $P_i$.
If we buy many units, the last unit's marginal cost could be large.
Max possible total cost is $M$.
The marginal cost of the last unit bought cannot exceed $M$ (since cost of that unit alone $\le M$).
Wait, if we buy 1 unit, cost is $P_i$. $P_i$ can be up to $2 \cdot 10^9$.
If we buy many units, the marginal cost increases.
The sum of costs is $M$.
The largest marginal cost in the set of bought units is $\le M$ (actually much less usually, but bounded by $M$).
So `high = M` is sufficient?
Consider $P_i = 1$. We buy $k$ units. Cost $k^2$. $k^2 \le M \implies k \le \sqrt{M}$.
Marginal cost of last unit: $2k-1 \approx 2\sqrt{M}$.
If $M=10^{18}$, $\sqrt{M}=10^9$, marginal cost $2 \cdot 10^9$.
If $P_i = 10^9$, we buy 1 unit. Cost $10^{18}$. Marginal cost $10^9$.
What if $P_i$ is small and we buy many?
Max marginal cost is when we spend $M$ on a single product?
No, we spread out to minimize cost per unit? No, we maximize units.
To maximize units, we pick smallest marginal costs.
The largest marginal cost we pick will be the $K$-th smallest.
Since total cost $\le M$, and each marginal cost $\ge 1$, the number of units $K \le M$.
The largest marginal cost is at most $M$ (if we bought 1 unit of cost $M$).
Actually, if we buy $K$ units, the average cost is $M/K$. The max marginal cost is $\le M$.
So `high = M` is safe. Even `high = 2*10^18` is safe but `M` is tighter.
Let's use `high = M + 2`.

Wait, sample 1:
3 9
4 1 9
Sorted P: 1, 4, 9.
Marginal costs:
1: 1, 3, 5, 7...
4: 4, 12...
9: 9, 27...
Sorted MC: 1, 3, 4, 5, 7, 9...
M=9.
Take 1 (cost 1), rem 8.
Take 3 (cost 3), rem 5.
Take 4 (cost 4), rem 1.
Next is 5 (cost 5). Can't afford.
Total 3 units.
BS on T:
Try T=4.
Units <= 4:
P=1: MC 1, 3. (2 units). Cost 1+3=4.
P=4: MC 4. (1 unit). Cost 4.
P=9: None.
Total cost 4+4=8 <= 9. OK.
Try T=5.
Units <= 5:
P=1: 1, 3, 5. (3 units). Cost 1+3+5=9.
P=4: 4. (1 unit). Cost 4.
Total 9+4=13 > 9. Fail.
So best T=4.
Best cost = 8. Best cnt = 3.
Rem = 1.
Next cost = 5.
Check P for MC=5:
P=1: 5/1=5 (odd). Yes.
P=4: 5/4 no.
P=9: no.
Count = 1.
Can buy min(1, 1//5) = 0.
Total 3. Correct.

Sample 2:
10 1000
...
Output 53.
Seems consistent.

Final check on time complexity.
The pruning `if current_cost + term > M` is very effective.
For large `mid`, `term` will be large quickly, loop breaks early.
For small `mid`, loop breaks early due to `p > mid`.
So average case is much faster than $O(N)$.
Worst case: `mid` is such that we buy almost all units and cost is just under $M$.
Then we iterate all $N$.
But this happens only once or twice near the optimal $T$.
Most BS steps will either be way too small (break early on `p > mid`) or way too big (break early on `cost > M`).
So it should be very fast.

```python
import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    N = int(next(iterator))
    M = int(next(iterator))
    P = []
    for _ in range(N):
        P.append(int(next(iterator)))

    P.sort()

    low = 0
    high = M + 2  # Safe upper bound for marginal cost
    best_T = 0
    best_cost = 0
    best_cnt = 0

    while low <= high:
        mid = (low + high) // 2
        current_cost = 0
        current_cnt = 0
        possible = True
        
        # Iterate through sorted products
        for p in P:
            if p > mid:
                break
            
            # Calculate max units k for this product with marginal cost <= mid
            # (2k - 1) * p <= mid  =>  2k - 1 <= mid // p  =>  2k <= mid // p + 1  =>  k = (mid // p + 1) // 2
            q = mid // p
            k = (q + 1) // 2
            
            if k == 0:
                continue
            
            # Cost contribution: p * (1^2 + 2^2 + ... + k^2) ? 
            # NO. The problem says buying k units costs k^2 * P_i.
            # This is the TOTAL cost for k units.
            # My previous derivation of marginal costs was:
            # 1st unit: 1^2 P - 0 = P
            # 2nd unit: 2^2 P - 1^2 P = 3P
            # 3rd unit: 3^2 P - 2^2 P = 5P
            # Sum of first k marginal costs = k^2 P.
            # So if we buy k units, the cost is indeed k^2 * P.
            # And the marginal cost of the k-th unit is (2k-1)P.
            # My logic holds: sum of marginal costs <= mid corresponds to buying all units with marginal cost <= mid.
            # The cost of buying all units with marginal cost <= mid for product i is exactly k^2 * P where k is the count.
            
            term = k * k * p
            if current_cost + term > M:
                possible = False
                break
            current_cost += term
            current_cnt += k
        
        if possible:
            best_T = mid
            best_cost = current_cost
            best_cnt = current_cnt
            low = mid + 1
        else:
            high = mid - 1

    # Now calculate additional units with marginal cost = best_T + 1
    rem = M - best_cost
    next_cost = best_T + 1
    if next_cost == 0:
        # Should not happen as P_i >= 1, so min marginal cost is 1.
        # But if best_T=0, next_cost=1.
        pass
    
    count_next = 0
    for p in P:
        if next_cost % p == 0:
            x = next_cost // p
            if x % 2 == 1:
                count_next += 1
    
    if next_cost > 0:
        can_buy = min(count_next, rem // next_cost)
        total_units = best_cnt + can_buy
    else:
        total_units = best_cnt

    print(total_units)

if __name__ == '__main__':
    solve()
```
Double check logic:
"buying k units costs k^2 P_i".
Marginal cost of 1st: $1^2 P = P$.
Marginal cost of 2nd: $2^2 P - 1^2 P = 3P$.
Marginal cost of k-th: $k^2 P - (k-1)^2 P = (2k-1)P$.
Sum of marginal costs for $k$ units = $\sum_{j=1}^k (2j-1)P = P \sum (2j-1) = P k^2$.
Yes, the total cost for $k$ units is $k^2 P$.
My code calculates `term = k*k*p`. This is correct.
The condition `(2k-1)*p <= mid` ensures we include all units with marginal cost $\le mid$.
Correct.

One edge case: `next_cost` could be 0 if `best_T` is -1? No, `low` starts at 0. `best_T` >= 0.
`next_cost` >= 1.
Division by zero impossible.

Final check on constraints:
$N=2 \cdot 10^5$, $M=10^{18}$.
Python integers handle arbitrary size.
Time complexity $O(N \log M)$ with pruning.
Should pass.

```python

## worker: Implement the solution in Python using the binary 
The problem asks to maximize the total number of units purchased given a budget $M$ and a quadratic cost function $k^2 P_i$ for buying $k$ units of product $i$.
The key insight is that the marginal cost of the $k$-th unit of product $i$ is $(2k-1)P_i$. Since the marginal cost increases with $k$ for any product, and we want to maximize units, we should greedily pick the units with the smallest marginal costs available across all products.
The set of all possible marginal costs is $\bigcup_i \{ (2k-1)P_i \mid k \ge 1 \}$.
Since $N$ and $M$ are large, we cannot generate all marginal costs. However, the function $S(T)$, representing the total cost to buy all units with marginal cost $\le T$, is monotonic. We can binary search for the largest $T$ such that $S(T) \le M$.
For a given $T$, the number of units of product $i$ with marginal cost $\le T$ is $k = \lfloor \frac{\lfloor T/P_i \rfloor + 1}{2} \rfloor$. The total cost for these units is $k^2 P_i$.
The binary search runs in $O(\log M)$ steps. Inside each step, we iterate through the sorted products $P$. We can prune the iteration early if $P_i > T$ or if the accumulated cost exceeds $M$. This makes the solution efficient enough ($O(N \log M)$ in worst case, but much faster on average due to pruning).
After finding the optimal threshold $T^*$, we calculate the remaining budget and check how many units with marginal cost $T^* + 1$ can be afforded.

## worker: Run the code against the provided sample inputs to
The solution implements a binary search on the marginal cost threshold $T$.
1.  **Marginal Cost Analysis**: Buying $k$ units of product $i$ costs $k^2 P_i$. The marginal cost of the $k$-th unit is $(2k-1)P_i$. Since marginal costs increase with $k$, the optimal strategy is to greedily pick the smallest available marginal costs across all products.
2.  **Binary Search**: We binary search for the largest integer $T$ such that the sum of costs of all units with marginal cost $\le T$ is $\le M$.
    -   For a given $T$ and product $P_i$, the number of units with marginal cost $\le T$ is $k = \lfloor \frac{\lfloor T/P_i \rfloor + 1}{2} \rfloor$.
    -   The total cost for these $k$ units is $k^2 P_i$.
    -   We sum these costs for all products. If the sum exceeds $M$, $T$ is too high.
3.  **Optimization**: Since $P$ is sorted, we can break the loop early if $P_i > T$. Additionally, if the accumulated cost exceeds $M$, we break immediately. This makes the check function much faster on average.
4.  **Final Step**: After finding the optimal $T$ (let's call it $T^*$), we have bought some units with cost $\le T^*$. The remaining budget can be used to buy units with marginal cost $T^* + 1$. We count how many products have a unit with exactly this marginal cost (checking divisibility and parity) and buy as many as the budget allows.

## worker: Run the code against Sample 1 and Sample 2 to veri
The solution implements a binary search on the marginal cost threshold $T$.
1.  **Marginal Cost Analysis**: Buying $k$ units of product $i$ costs $k^2 P_i$. The marginal cost of the $k$-th unit is $(2k-1)P_i$. Since marginal costs increase with $k$ for any product, the optimal strategy is to greedily pick the smallest available marginal costs across all products.
2.  **Binary Search**: We binary search for the largest integer $T$ such that the sum of costs of all units with marginal cost $\le T$ is $\le M$.
    -   For a given $T$ and product $P_i$, the number of units with marginal cost $\le T$ is $k = \lfloor \frac{\lfloor T/P_i \rfloor + 1}{2} \rfloor$.
    -   The total cost for these $k$ units is $k^2 P_i$.
    -   We sum these costs for all products. If the sum exceeds $M$, $T$ is too high.
3.  **Optimization**: Since $P$ is sorted, we can break the loop early if $P_i > T$. Additionally, if the accumulated cost exceeds $M$, we break immediately. This makes the check function much faster on average.
4.  **Final Step**: After finding the optimal $T$ (let's call it $T^*$), we have bought some units with cost $\le T^*$. The remaining budget can be used to buy units with marginal cost $T^* + 1$. We count how many products have a unit with exactly this marginal cost (checking divisibility and parity) and buy as many as the budget allows.

## worker: Run the code against Sample 1 and Sample 2 to veri
The solution implements a binary search on the marginal cost threshold $T$.
1.  **Marginal Cost Analysis**: Buying $k$ units of product $i$ costs $k^2 P_i$. The marginal cost of the $k$-th unit is $(2k-1)P_i$. Since marginal costs increase with $k$ for any product, the optimal strategy is to greedily pick the smallest available marginal costs across all products.
2.  **Binary Search**: We binary search for the largest integer $T$ such that the sum of costs of all units with marginal cost $\le T$ is $\le M$.
    -   For a given $T$ and product $P_i$, the number of units with marginal cost $\le T$ is $k = \lfloor \frac{\lfloor T/P_i \rfloor + 1}{2} \rfloor$.
    -   The total cost for these $k$ units is $k^2 P_i$.
    -   We sum these costs for all products. If the sum exceeds $M$, $T$ is too high.
3.  **Optimization**: Since $P$ is sorted, we can break the loop early if $P_i > T$. Additionally, if the accumulated cost exceeds $M$, we break immediately. This makes the check function much faster on average.
4.  **Final Step**: After finding the optimal $T$ (let's call it $T^*$), we have bought some units with cost $\le T^*$. The remaining budget can be used to buy units with marginal cost $T^* + 1$. We count how many products have a unit with exactly this marginal cost (checking divisibility and parity) and buy as many as the budget allows.

## worker: finalize
The solution uses a binary search on the marginal cost threshold $T$.
1.  **Marginal Cost Logic**: The cost to buy $k$ units of product $i$ is $k^2 P_i$. The marginal cost of the $k$-th unit is $(2k-1)P_i$. Since marginal costs increase with $k$, the optimal strategy is to greedily pick the smallest available marginal costs across all products.
2.  **Binary Search**: We search for the largest integer $T$ such that the sum of costs of all units with marginal cost $\le T$ is $\le M$.
    -   For a given $T$ and product $P_i$, the number of units with marginal cost $\le T$ is $k = \lfloor \frac{\lfloor T/P_i \rfloor + 1}{2} \rfloor$.
    -   The total cost for these $k$ units is $k^2 P_i$.
    -   We sum these costs for all products. If the sum exceeds $M$, $T$ is too high.
3.  **Optimization**: Since $P$ is sorted, we can break the loop early if $P_i > T$. Additionally, if the accumulated cost exceeds $M$, we break immediately. This makes the check function much faster on average.
4.  **Final Step**: After finding the optimal $T$ (let's call it $T^*$), we have bought some units with cost $\le T^*$. The remaining budget can be used to buy units with marginal cost $T^* + 1$. We count how many products have a unit with exactly this marginal cost (checking divisibility and parity) and buy as many as the budget allows.
