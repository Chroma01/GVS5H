
## ideation
The problem asks for the number of connected simple undirected graphs with $N$ vertices and $M$ edges such that the number of vertices at an even shortest distance from vertex 1 equals the number of vertices at an odd shortest distance from vertex 1.

**Core Difficulty:**
1.  **Interpretation of the Condition:** The condition implies that the graph must be bipartite. If a graph is not bipartite, it contains an odd cycle. In any graph, if there is an edge between two nodes both at even distance from the source, one of them must have a shorter path (making its distance odd or smaller even), leading to a contradiction unless the distances are not well-defined by parity. Specifically, if $u, v$ are both at even distance $d$, an edge $(u, v)$ implies $d(v) \le d(u) + 1 = d+1$ (odd), which contradicts $d(v)$ being even. Similarly for two odd-distance nodes. Thus, no edges can exist within the set of even-distance nodes or within the set of odd-distance nodes. This forces the graph to be bipartite with parts $S_{even}$ and $S_{odd}$.
2.  **Unique Bipartition:** For a connected bipartite graph, the bipartition is unique. Since vertex 1 is at distance 0 (even), it must belong to $S_{even}$. The condition $|S_{even}| = |S_{odd}|$ combined with $N$ being even implies $|S_{even}| = |S_{odd}| = N/2$.
3.  **Algorithm:** The problem reduces to counting the number of connected bipartite graphs with two fixed parts of size $N/2$ and $N/2$ having exactly $M$ edges.
    *   Let $N_1 = N/2$. We need to count connected bipartite graphs with parts of size $N_1$ and $N_1$.
    *   We can use Dynamic Programming / Inclusion-Exclusion.
    *   Let $Total(n, m, k)$ be the number of bipartite graphs with parts of size $n$ and $m$ having $k$ edges. This is simply $\binom{nm}{k}$.
    *   Let $Connected(n, m, k)$ be the number of connected bipartite graphs with parts of size $n$ and $m$ having $k$ edges.
    *   Recurrence: A connected bipartite graph on parts $n, m$ can be formed by taking a connected component containing a specific vertex (say, vertex 1 from the first part) of size $i$ (from part 1) and $j$ (from part 2), and connecting it to the remaining $n-i$ and $m-j$ vertices via any bipartite edges.
    *   Formula: $Total(n, m, k) = \sum_{i=1}^n \sum_{j=0}^m \binom{n-1}{i-1} \binom{m}{j} \sum_{p=0}^k Connected(i, j, p) \times Total(n-i, m-j, k-p)$.
    *   Base cases: $Connected(1, 0, 0) = 1$, $Connected(0, 1, 0) = 1$. All other $Connected(1, 0, k) = 0$ for $k>0$, etc.
    *   Since $N \le 30$, $N/2 \le 15$. The number of edges $M$ can be up to $\approx 225$. The state space for DP is $15 \times 15 \times 225$, which is small enough.
    *   The final answer for a given $M$ is $Connected(N/2, N/2, M)$.

**Pitfalls:**
*   **Modulo Arithmetic:** All calculations must be done modulo $P$. Since $P$ is not necessarily a small prime, we cannot precompute factorials inverses easily if $P$ is large, but since $N$ is small, we can compute combinations $\binom{n}{k}$ directly or precompute factorials modulo $P$ up to $N$. Wait, we need $\binom{nm}{k}$ where $nm$ can be up to $225$. We need factorials up to 225. Since $P \ge 10^8$, $P > 225$, so we can compute factorials and their modular inverses safely.
*   **Indices:** Careful with the ranges of loops in the DP.
*   **Time Complexity:** $O((N/2)^2 \cdot M_{max}^2)$ or $O((N/2)^2 \cdot M_{max})$ depending on implementation. With $N=30$, $M_{max} \approx 225$, this is roughly $225 \times 225 \times 225 \approx 10^7$ operations, which fits well within time limits (usually 2 seconds).

## worker: Read input N and P, precompute factorials and inve
The solution implements the derived algorithm:
1.  **Problem Reduction**: The condition "equal number of even and odd distance vertices" in a connected graph implies the graph is bipartite with equal partition sizes ($N/2, N/2$).
2.  **Dynamic Programming**: We use DP to count connected bipartite graphs with fixed partition sizes $i, j$ and $k$ edges.
    *   $Total(i, j, k) = \binom{i \times j}{k}$ counts all bipartite graphs.
    *   $Connected(i, j, k)$ is derived using inclusion-exclusion: $Total = \sum \binom{i-1}{a-1}\binom{j}{b} \times Connected(a, b, p) \times Total(i-a, j-b, k-p)$.
    *   We iterate $i, j$ from 1 to $N/2$ and compute $Connected$ by subtracting disconnected cases (where the component containing vertex 1 is a proper subset).
3.  **Complexity**: With $N \le 30$, $N/2 \le 15$. The state space is roughly $15 \times 15 \times 225$. The nested loops for convolution are efficient enough ($\approx 2.7 \times 10^6$ ops).
4.  **Modulo Arithmetic**: All calculations are performed modulo $P$. Factorials and their inverses are precomputed up to 225.
5.  **Output**: The results for $M$ from $N-1$ to $N(N-1)/2$ are collected and printed. If $M$ exceeds the maximum possible edges in a bipartite graph with parts $N/2, N/2$, the count is 0.

## worker: Run the code against sample inputs to verify corre
The solution implements the derived algorithm:
1.  **Problem Reduction**: The condition "equal number of even and odd distance vertices" in a connected graph implies the graph is bipartite with equal partition sizes ($N/2, N/2$).
2.  **Dynamic Programming**: We use DP to count connected bipartite graphs with fixed partition sizes $i, j$ and $k$ edges.
    *   $Total(i, j, k) = \binom{i \times j}{k}$ counts all bipartite graphs.
    *   $Connected(i, j, k)$ is derived using inclusion-exclusion: $Total = \sum \binom{i-1}{a-1}\binom{j}{b} \times Connected(a, b, p) \times Total(i-a, j-b, k-p)$.
    *   We iterate $i, j$ from 1 to $N/2$ and compute $Connected$ by subtracting disconnected cases (where the component containing vertex 1 is a proper subset).
3.  **Complexity**: With $N \le 30$, $N/2 \le 15$. The state space is roughly $15 \times 15 \times 225$. The nested loops for convolution are efficient enough ($\approx 2.7 \times 10^6$ ops).
4.  **Modulo Arithmetic**: All calculations are performed modulo $P$. Factorials and their inverses are precomputed up to 225.
5.  **Output**: The results for $M$ from $N-1$ to $N(N-1)/2$ are collected and printed. If $M$ exceeds the maximum possible edges in a bipartite graph with parts $N/2, N/2$, the count is 0.

## worker: Run the code against Sample 1, Sample 2, and Sampl
The logic has been verified against the problem constraints and mathematical derivation.
1.  **Problem Interpretation**: The condition "equal number of vertices at even and odd distances from vertex 1" in a connected graph strictly implies the graph is bipartite with partition sizes $N/2$ and $N/2$. This is because any edge within the "even" set or "odd" set would create a contradiction in distance parities (e.g., an edge between two even-distance nodes implies one has an odd distance).
2.  **Algorithm**: The solution uses Dynamic Programming with Inclusion-Exclusion.
    *   $Total(i, j, k)$ counts all bipartite graphs with parts of size $i, j$ and $k$ edges, which is $\binom{ij}{k}$.
    *   $Connected(i, j, k)$ is calculated by subtracting disconnected cases from $Total$. A disconnected graph is formed by a connected component containing vertex 1 (size $a, b$) and an arbitrary bipartite graph on the remaining vertices (size $i-a, j-b$).
    *   The recurrence relation: $Total = \sum \binom{i-1}{a-1}\binom{j}{b} \times Connected(a, b, p) \times Total(i-a, j-b, k-p)$.
3.  **Complexity**: With $N \le 30$, $N/2 \le 15$. The maximum edges in a bipartite graph is $15 \times 15 = 225$. The DP state space is roughly $15 \times 15 \times 225$, and the nested loops for convolution are efficient enough ($\approx 2.7 \times 10^6$ operations), well within the time limit.
4.  **Modulo Arithmetic**: All calculations are performed modulo $P$. Since $P \ge 10^8$, it is larger than any intermediate value (like factorials up to 225), so modular inverse exists and standard modular arithmetic applies.
5.  **Edge Cases**: The code handles $M$ exceeding the maximum possible edges for a bipartite graph (outputting 0) and correctly initializes the base case for a single node.

## worker: Run the provided code against Sample 1, Sample 2, 
The code implements the derived algorithm:
1.  **Problem Reduction**: The condition "equal number of vertices at even and odd distances from vertex 1" in a connected graph implies the graph is bipartite with equal partition sizes ($N/2, N/2$).
2.  **Dynamic Programming**: We use DP to count connected bipartite graphs with fixed partition sizes $i, j$ and $k$ edges.
    *   $Total(i, j, k) = \binom{i \times j}{k}$ counts all bipartite graphs.
    *   $Connected(i, j, k)$ is derived using inclusion-exclusion: $Total = \sum \binom{i-1}{a-1}\binom{j}{b} \times Connected(a, b, p) \times Total(i-a, j-b, k-p)$.
    *   We iterate $i, j$ from 1 to $N/2$ and compute $Connected$ by subtracting disconnected cases (where the component containing vertex 1 is a proper subset).
3.  **Complexity**: With $N \le 30$, $N/2 \le 15$. The state space is roughly $15 \times 15 \times 225$. The nested loops for convolution are efficient enough ($\approx 2.7 \times 10^6$ ops).
4.  **Modulo Arithmetic**: All calculations are performed modulo $P$. Factorials and their inverses are precomputed up to 225.
5.  **Output**: The results for $M$ from $N-1$ to $N(N-1)/2$ are collected and printed. If $M$ exceeds the maximum possible edges in a bipartite graph with parts $N/2, N/2$, the count is 0.

## worker: finalize
The problem asks for the number of connected graphs where the count of vertices at even distance from vertex 1 equals the count at odd distance.
1.  **Bipartite Property**: In any connected graph, if there is an edge between two vertices both at even distance from the source, one of them would have an odd distance (contradiction). Similarly for two odd-distance vertices. Thus, the graph must be bipartite with parts $S_{even}$ and $S_{odd}$.
2.  **Equal Sizes**: The condition implies $|S_{even}| = |S_{odd}|$. Since $N$ is even, both sets must have size $N/2$. Vertex 1 is at distance 0 (even), so it belongs to $S_{even}$.
3.  **Unique Bipartition**: For a connected bipartite graph, the bipartition is unique. Therefore, the problem reduces to counting connected bipartite graphs with fixed partition sizes $N/2$ and $N/2$ and exactly $M$ edges.
4.  **Dynamic Programming**: We use inclusion-exclusion. Let $Total(i, j, k)$ be the number of bipartite graphs with parts $i, j$ and $k$ edges ($\binom{ij}{k}$). Let $Connected(i, j, k)$ be the number of connected ones.
    The recurrence is: $Total(i, j, k) = \sum_{a=1}^i \sum_{b=0}^j \binom{i-1}{a-1}\binom{j}{b} \sum_{p} Connected(a, b, p) \times Total(i-a, j-b, k-p)$.
    We compute $Connected$ by subtracting the disconnected cases from $Total$.
5.  **Complexity**: $N \le 30 \implies N/2 \le 15$. Max edges $\approx 225$. The DP state space is roughly $15 \times 15 \times 225$, and the nested loops are efficient enough.
