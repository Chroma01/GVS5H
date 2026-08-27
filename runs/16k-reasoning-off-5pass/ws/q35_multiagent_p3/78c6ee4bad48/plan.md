1.  **Analyze the Operation**: The operation involves choosing four consecutive pieces in sorted order (indices $i, i+1, i+2, i+3$). Let their positions be $x_i < x_{i+1} < x_{i+2} < x_{i+3}$. The midpoint $M$ is $(x_i + x_{i+3})/2$. The inner pieces $x_{i+1}$ and $x_{i+2}$ are reflected across $M$. The new positions become $x'_{i+1} = M + (M - x_{i+1}) = x_i + x_{i+3} - x_{i+1}$ and $x'_{i+2} = M - (x_{i+2} - M) = x_i + x_{i+3} - x_{i+2}$.
2.  **Effect on Sum**: The sum of the four pieces before the operation is $S = x_i + x_{i+1} + x_{i+2} + x_{i+3}$. After the operation, the new sum is $x_i + (x_i + x_{i+3} - x_{i+1}) + (x_i + x_{i+3} - x_{i+2}) + x_{i+3} = 3x_i + 3x_{i+3} + x_{i+1} + x_{i+2} - x_{i+1} - x_{i+2} + x_{i+1} + x_{i+2}$ ... wait, let's re-calculate.
    New sum = $x_i + x'_{i+1} + x'_{i+2} + x_{i+3} = x_i + (x_i + x_{i+3} - x_{i+1}) + (x_i + x_{i+3} - x_{i+2}) + x_{i+3} = 3x_i + 3x_{i+3} + x_{i+1} + x_{i+2} - x_{i+1} - x_{i+2}$? No.
    $x'_{i+1} + x'_{i+2} = (x_i + x_{i+3} - x_{i+1}) + (x_i + x_{i+3} - x_{i+2}) = 2x_i + 2x_{i+3} - (x_{i+1} + x_{i+2})$.
    The total sum becomes $x_i + x_{i+3} + 2x_i + 2x_{i+3} - (x_{i+1} + x_{i+2}) = 3x_i + 3x_{i+3} - (x_{i+1} + x_{i+2})$.
    The change in sum is $\Delta = (3x_i + 3x_{i+3} - x_{i+1} - x_{i+2}) - (x_i + x_{i+1} + x_{i+2} + x_{i+3}) = 2x_i + 2x_{i+3} - 2x_{i+1} - 2x_{i+2} = 2(x_i + x_{i+3} - x_{i+1} - x_{i+2})$.
    Since $x_i < x_{i+1} < x_{i+2} < x_{i+3}$, it's not immediately obvious if this is negative. However, note that the operation preserves the set of values $\{x_i, x_{i+3}\}$ and transforms $\{x_{i+1}, x_{i+2}\}$ to $\{x_i+x_{i+3}-x_{i+2}, x_i+x_{i+3}-x_{i+1}\}$. The sum of the inner two changes from $x_{i+1}+x_{i+2}$ to $2x_i+2x_{i+3}-(x_{i+1}+x_{i+2})$. The total sum changes by $2(x_i+x_{i+3} - x_{i+1}-x_{i+2})$.
3.  **Invariant and Reachable States**: The key insight is that the operation allows us to permute the "inner" pieces relative to the "outer" ones in a specific way. Actually, a more powerful observation is that the operation is reversible and generates a group of transformations. It turns out that the set of reachable configurations corresponds to all permutations of the pieces that preserve the relative order of the first and last elements of any window of 4? No.
    Let's look at the sample. $1, 5, 7, 10 \rightarrow 1, 4, 6, 10$. Sum $21$. Original sum $23$.
    Notice that the outer pieces $1$ and $10$ stayed in place. The inner pieces $5, 7$ became $4, 6$.
    The operation essentially allows swapping the "inner" pair with a reflected version.
    A known result for this specific problem (AtCoder ABC 277 F or similar) is that the minimum sum is achieved when the pieces are as "left-heavy" as possible.
    Actually, the operation preserves the sum of coordinates modulo some value? No.
    Let's consider the effect on the sum again. We want to minimize the sum. This means we want $x_i + x_{i+3} < x_{i+1} + x_{i+2}$ for the operation to reduce the sum.
    However, we can perform operations repeatedly.
    The crucial observation is that the operation allows us to effectively swap adjacent elements in a way that reduces the sum if the "convexity" condition is met.
    In fact, it can be proven that the minimum sum is obtained when the sequence is "as convex as possible" to the left.
    Specifically, the problem is equivalent to finding the minimum sum of a sequence reachable from $X$ under these reflections.
    It turns out that the set of reachable configurations is such that the first and last elements are fixed? No, the operation on $i$ affects $i+1, i+2$. The first element $X_1$ is only affected if it is an inner element, i.e., in a window starting at $i=-1$? No, $i \ge 1$. So $X_1$ is never an inner element for $i=1$ (it's outer). For $i=2$, $X_1$ is not involved. So $X_1$ and $X_N$ are never moved?
    Wait, for $i=1$, pieces $2,3$ move. $1,4$ are fixed.
    For $i=2$, pieces $3,4$ move. $2,5$ are fixed.
    So $X_1$ is never moved. $X_N$ is never moved.
    What about $X_2$? It can be moved by $i=1$. Can it be moved again? Yes.
    It turns out that the minimum sum is simply the sum of the original coordinates if no operation reduces it? No, Sample 1 reduces it.
    
    Correct Insight: The operation preserves the sum of the coordinates if and only if $x_i + x_{i+3} = x_{i+1} + x_{i+2}$. Otherwise, it changes the sum.
    The problem is equivalent to: We can apply the transformation $x_{i+1}, x_{i+2} \to x_i+x_{i+3}-x_{i+2}, x_i+x_{i+3}-x_{i+1}$ (sorted).
    This looks like we can "push" mass to the left.
    Actually, there is a simpler invariant. The sum of the coordinates is minimized when the sequence is "sorted" in a specific way?
    
    Let's look at the constraints and similar problems. This is likely related to the fact that the operation allows us to reorder the inner elements arbitrarily while keeping the outer ones fixed, but with a cost.
    However, a key property is that the operation is an involution on the pair $(x_{i+1}, x_{i+2})$ relative to the midpoint.
    
    Alternative approach:
    The minimum sum is achieved when the configuration is "stable", meaning no operation can reduce the sum further.
    An operation reduces the sum if $x_i + x_{i+3} < x_{i+1} + x_{i+2}$.
    We can greedily apply operations that reduce the sum.
    Since $N$ is up to $2 \times 10^5$, we need an efficient solution.
    
    Actually, it can be shown that the minimum sum is $\sum X_j - 2 \times (\text{something})$.
    
    Let's reconsider the sample.
    $1, 5, 7, 10$. Sum 23.
    Op $i=1$: $M=5.5$. $5 \to 6, 7 \to 4$. New: $1, 4, 6, 10$. Sum 21.
    Can we do better?
    Try op on $1, 4, 6, 10$ with $i=1$: $M=5.5$. $4 \to 7, 6 \to 5$. Back to $1, 5, 7, 10$.
    
    What if we have 5 elements? $0, 1, 6, 10, 14, 16$.
    Sample 2: $N=6$. Output 41.
    Original sum: $0+1+6+10+14+16 = 47$.
    
    The problem is known to be solvable by noting that the operation allows us to swap the "inner" pair with their reflection. The minimum sum is achieved when the sequence is "convex".
    
    Actually, the correct solution involves dynamic programming or a greedy strategy based on the fact that the relative order of the pieces can be changed.
    
    However, there is a known result: The minimum sum is $\sum_{i=1}^N X_i - 2 \sum_{k} \max(0, \text{something})$.
    
    Let's use the property that the operation preserves the sum of the squares? No.
    
    Let's try a different perspective. The operation is linear.
    
    After research, this problem is from AtCoder. The solution is that the minimum sum is obtained by sorting the array and then the answer is just the sum? No.
    
    The correct insight is that the operation allows us to effectively "bubble" smaller values to the left.
    The minimum sum is $\sum_{i=1}^N X_i$ if the array is already "convex" in a specific sense?
    
    Let's implement a simulation with a priority queue of operations that reduce the sum?
    Since $N$ is large, simulation might be slow if many operations are needed.
    
    However, note that each operation that reduces the sum strictly decreases the sum. The values are bounded.
    
    Actually, the minimum sum is simply the sum of the coordinates after sorting the array such that it is "as left-skewed as possible".
    
    Let's write a solution that uses the fact that we can independently optimize pairs? No.
    
    Final Plan:
    1. Read input.
    2. The problem is equivalent to finding the minimum sum of a sequence reachable by these reflections.
    3. It turns out the minimum sum is $\sum X_i - 2 \times \sum_{i=1}^{N-3} \max(0, X_{i+1} + X_{i+2} - X_i - X_{i+3})$? No, this is greedy.
    
    Let's use the provided solution structure.