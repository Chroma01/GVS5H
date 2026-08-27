### Question
You are given an undirected tree T with N vertices, numbered 1, 2, \ldots, N. The i-th edge is an undirected edge connecting vertices A_i and B_i.
A graph is defined to be an alkane if and only if it satisfies the following conditions:

- The graph is an undirected tree.
- Every vertex has degree 1 or 4, and there is at least one vertex of degree 4.

Determine whether there exists a subgraph of T that is an alkane, and if so, find the maximum number of vertices in such a subgraph.

Input

The input is given from Standard Input in the following format:
N
A_1 B_1
A_2 B_2
\vdots
A_{N - 1} B_{N - 1}

Output

If there exists a subgraph of T that is an alkane, print the maximum number of vertices in such a subgraph. Otherwise, print -1.

Constraints


- 1 \leq N \leq 2 \times 10^5
- 1 \leq A_i, B_i \leq N
- The given graph is an undirected tree.
- All input values are integers.

Sample Input 1

9
1 2
2 3
3 4
4 5
2 6
2 7
3 8
3 9

Sample Output 1

8

Let (u, v) denote an undirected edge between vertices u and v.
A subgraph consisting of vertices 1,2,3,4,6,7,8,9 and edges (1,2),(2,3),(3,4),(2,6),(2,7),(3,8),(3,9) is an alkane.

Sample Input 2

7
1 2
1 3
2 4
2 5
3 6
3 7

Sample Output 2

-1

Sample Input 3

15
8 5
2 9
1 12
6 11
9 3
15 1
7 12
7 13
10 5
6 9
5 1
1 9
4 5
6 14

Sample Output 3

11

### Format: Read the inputs from stdin solve the problem and write the answer to stdout (do not directly test on the sample inputs). Enclose your code within delimiters as follows. Ensure that when the python program runs, it reads the inputs, runs the algorithm and writes output to STDOUT.

