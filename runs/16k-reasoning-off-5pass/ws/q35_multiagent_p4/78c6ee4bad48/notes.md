
## ideation
The core difficulty lies in understanding the invariant properties of the operation and efficiently computing the minimum sum without simulation, which would be too slow for $N \le 2 \times 10^5$.

1.  **Operation Analysis**: The operation on indices $i, i+1, i+2, i+3$ (0-indexed) replaces $X_{i+1}$ and $X_{i+2}$ with $X_i + X_{i+3} - X_{i+2}$ and $X_i + X_{i+3} - X_{i+1}$ respectively. The sum of the four elements changes from $S_{old} = X_i + X_{i+1} + X_{i+2} + X_{i+3}$ to $S_{new} = X_i + (X_i + X_{i+3} - X_{i+2}) + (X_i + X_{i+3} - X_{i+1}) + X_{i+3} = 2(X_i + X_{i+3}) + (X_i + X_{i+3}) - (X_{i+1} + X_{i+2}) = 3(X_i + X_{i+3}) - (X_{i+1} + X_{i+2})$.
    The change in the total sum is $\Delta = S_{new} - S_{old} = 2(X_i + X_{i+3} - X_{i+1} - X_{i+2})$.
    To minimize the total sum, we want to apply operations where $\Delta < 0$, i.e., $X_i + X_{i+3} < X_{i+1} + X_{i+2}$.

2.  **Invariant**: It can be proven that the operation preserves the sum of the coordinates at odd indices and the sum of the coordinates at even indices modulo some value? No, actually, a stronger invariant exists.
    Let's look at the effect on the sum of elements at odd positions ($S_{odd}$) and even positions ($S_{even}$).
    If we apply the operation at index $i$ (0-indexed), the elements at $i+1$ and $i+2$ change.
    - If $i$ is even, $i+1$ is odd, $i+2$ is even.
      $S_{odd}$ changes by $(X_i + X_{i+3} - X_{i+2}) - X_{i+2} = X_i + X_{i+3} - 2X_{i+2}$.
      $S_{even}$ changes by $(X_i + X_{i+3} - X_{i+1}) - X_{i+1} = X_i + X_{i+3} - 2X_{i+1}$.
      This doesn't seem to preserve individual sums.

3.  **Key Insight from Competitive Programming**: This problem is equivalent to finding the minimum sum of a sequence that satisfies the convexity condition $X_i + X_{i+3} \ge X_{i+1} + X_{i+2}$ for all $i$, which is reachable from the initial configuration.
    However, there is a simpler invariant: The sum of the coordinates of the pieces at positions $1, 3, 5, \dots$ and $2, 4, 6, \dots$ are NOT invariant.
    BUT, it is known that the minimum sum is achieved when the sequence is "sorted" in a specific way related to the initial values.
    
    Actually, let's look at the sample cases again.
    Sample 1: `1 5 7 10`. Sum = 23. Output = 21.
    Operation: $i=0$. $M = (1+10)/2 = 5.5$. New $X_1 = 5.5 + (5.5-5) = 6$. New $X_2 = 5.5 - (7-5.5) = 4$.
    New array: `1 6 4 10`. Wait, the problem says "ascending order of coordinate".
    The pieces are identified by their initial positions? No, "i-th and (i+3)-rd pieces in ascending order of coordinate".
    So after the move, we must re-sort.
    Initial: $X_0=1, X_1=5, X_2=7, X_3=10$.
    Op on $i=0$ (indices 0,1,2,3 in sorted order):
    Outer: $X_0=1, X_3=10$. Midpoint $M=5.5$.
    Inner: $X_1=5, X_2=7$.
    New positions: $2M - 5 = 6$, $2M - 7 = 4$.
    The pieces move to 6 and 4.
    The set of coordinates becomes $\{1, 6, 4, 10\}$. Sorted: $1, 4, 6, 10$.
    Sum: $1+4+6+10 = 21$.

    Sample 2: `0 1 6 10 14 16`. Sum = 47. Output = 41.
    
    The critical realization is that the operation allows us to effectively "swap" the relative order of elements in a way that minimizes the sum.
    It turns out that the minimum sum is simply the sum of the initial array if we can't reduce it, but we can.
    
    **Correct Approach**:
    The operation preserves the sum of the coordinates of the pieces at odd indices and even indices? No.
    However, it preserves the sum of the coordinates of the pieces at indices $i$ where $i \equiv 0 \pmod 2$ and $i \equiv 1 \pmod 2$? No.
    
    Let's look at the change in sum again: $\Delta = 2(X_i + X_{i+3} - X_{i+1} - X_{i+2})$.
    We want to minimize the sum. This is equivalent to maximizing the reduction.
    
    There is a known result for this problem (AtCoder ABC 256 F is different, this is likely **AtCoder Grand Contest 043 A** or similar, actually it's **AtCoder Beginner Contest 256 Problem F**? No. It is **AtCoder Regular Contest 130 C**? No.
    
    Actually, this problem is **AtCoder Beginner Contest 256 Problem E**? No.
    
    Let's rely on the property: The minimum sum is the sum of the initial array minus $2 \times$ the maximum possible reduction.
    
    **Final Insight**: The problem is equivalent to finding the minimum sum of a sequence that is "convex" in the sense that $X_i + X_{i+3} \ge X_{i+1} + X_{i+2}$.
    The minimum sum is achieved when the sequence is as "flat" as possible.
    
    However, there is a simpler invariant: The sum of the coordinates of the pieces at odd positions and even positions are NOT invariant, but the sum of the coordinates of the pieces at positions $1, 2, \dots, N$ modulo 2? No.
    
    **Correct Solution**:
    The minimum sum is the sum of the initial array if the array is already convex.
    Otherwise, we can reduce it.
    The reduction is determined by the "non-convexities".
    
    Actually, the answer is simply the sum of the initial array if we can't do better. But we can.
    
    Let's try a different perspective. The operation is linear. The final sum is a linear combination of the initial $X_i$.
