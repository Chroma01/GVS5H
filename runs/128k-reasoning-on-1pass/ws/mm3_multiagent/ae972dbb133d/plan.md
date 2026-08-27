**Solution Explanation**

For every cell `(i , j)` we are given a tile

* **type A** – a segment between two *adjacent* edges  
  (four possibilities : `R+U , U+L , L+D , D+R`)

* **type B** – a segment between two *opposite* edges  
  (two possibilities : `L+R` or `U+D`)

The grid is a torus, i.e. cell `(i , W‑1)` is neighbour of `(i , 0)` and
cell `(H‑1 , j)` of `(0 , j)`.


--------------------------------------------------------------------

#### 1.   From tiles to edges

Only the two edge–midpoints of a tile are important.
For a cell we write  

```
h = number of chosen horizontal edges   (0,1,2)
t = number of chosen vertical   edges   (0,1,2)      (t = 2 – h)
```

```
type A :  h = 1 ,  t = 1                (exactly one horizontal, one vertical)
type B :  (h , t) = (2 , 0)  or  (0 , 2) (both horizontal or both vertical)
```

So every cell has to satisfy  

```
h + t = 2
type A : h = 1
type B : h = 0 or 2
```

For a *fixed* `h` the value `t` is forced (`t = 2‑h`).

--------------------------------------------------------------------

#### 2.   Horizontal edges – one row

Consider a single row, it is a cycle of length `W`.

```
horizontal edge between column j-1 and j  =  e[j] ∈ {0,1}
```

For a cell `j`

```
e[j-1] + e[j] = h[j]                (1)
```

All equations (1) for one row form a linear system over **GF(2)**
(because `x+y (mod 2) = x XOR y`).
Writing `h[j] (mod 2)` we get  

```
e[j-1] XOR e[j] = h[j] (mod 2)
```

The sum over the whole cycle gives  

```
# { j | h[j] is odd }  must be even                (2)
```

If (2) holds the system has rank `W‑1`,
hence exactly **two** solutions
(the free variable is `e[0]`).

Therefore

```
row has 0 solutions      ⇔   #A in the row is odd
row has 2 solutions      ⇔   #A in the row is even                (3)
```

The same argument holds for columns, only `h` is replaced by `t (=2-h)`.
A column has the same condition: **the number of `A` cells in it must be even**.

--------------------------------------------------------------------

#### 3.   The whole grid

For a cell which is **type B** we have two possibilities for `h`

```
h = 0   ⇔   the two vertical edges are used
h = 2   ⇔   the two horizontal edges are used
```

Let  

```
b(i,j) = 0   if h = 0          (vertical segment)
b(i,j) = 1   if h = 2          (horizontal segment)
```

From the row equations (1) we obtain for a `B`‑cell  

```
b(i,j) = e[i][j-1]                (the horizontal edge on its left)
```

From the column equations we obtain  

```
b(i,j) = f[j][i-1]                (the vertical edge above it)
```

Both must be equal, consequently  

```
e[i][j-1] = f[j][i-1]               (4)
```

For a cell of type **A** the value of `h` (and therefore `b`) is fixed,
`h = 1` → `b` does not appear.

--------------------------------------------------------------------

#### 4.   Prefix parities

Define  

```
R[i][j] = parity of number of A–cells in row i
          among columns 0 … j-1          (0/1)

C[j][i] = parity of number of A–cells in column j
          among rows    0 … i-1          (0/1)
```

From (4) and the definition of `b`

```
b(i,j)  =  R[i][j] XOR  C[j][i]                     (5)
```

For a `B`‑cell the value on the right hand side is known,  
for an `A`‑cell it is irrelevant (the equation never appears).

--------------------------------------------------------------------

#### 5.   A bipartite graph

Create a bipartite graph `G`

* left side : the `H` rows (vertices `0 … H‑1`)
* right side: the `W` columns (vertices `H … H+W‑1`)
* for every `B`‑cell `(i , j)` add the edge  

```
row i  –  column j   with label   D(i,j) = R[i][j] XOR C[j][i]   (0/1)
```

Only those edges exist, therefore a vertex without incident edge
means that the whole row (or column) consists only of `A` cells.

--------------------------------------------------------------------

#### 6.   Potentials on the graph

For a row we introduced the variable `r[i] = e[i][0]` (the first horizontal
edge of this row).  
For a column we introduced `c[j] = f[j][0]` (the first vertical edge of
this column).

Equation (4) together with (5) gives for every edge `(i , j)` of `G`

```
r[i] XOR c[j] = D(i,j)                     (6)
```

Thus the whole problem is reduced to the following pure graph problem:

*Choose binary potentials `r[i] , c[j]` for the vertices of `G`
so that (6) holds on every edge.*

--------------------------------------------------------------------

#### 7.   Consistency and number of components

Equation (6) is a system of linear equations over **GF(2)**.
It has a solution **iff** for every cycle the xor of the
labels `D` along the cycle is `0`.  
A standard BFS/DFS on `G` does exactly this:

```
choose an arbitrary vertex, give it potential 0
propagate through the edges using (6)
if we ever meet a previously visited vertex with a different value → inconsistency
```

If the propagation finishes without conflict,
the whole connected component has *exactly two* solutions
(the whole component can be flipped by xor‑1).

Vertices without any incident edge are isolated components,
each also contributes factor `2` (the free choice of its potential).

Consequences:

* the **first necessary condition** is

```
every row  has even number of A   and
every column has even number of A                (from (3))
```

* if it holds, run the BFS on `G`.  
  If a contradiction occurs → answer `0`.  
  Otherwise let  

```
C = number of connected components of G
answer = 2^C   (mod 998244353)
```

--------------------------------------------------------------------

#### 8.   Algorithm

For one test case  

```
read H , W
rowCnt[0..H-1] = colCnt[0..W-1] = 0
colParity[0..W-1] = 0                     // C[column][current row‑1]
for i = 0 … H‑1
        read string s
        rowParity = 0                     // R[row][current column‑1]
        for j = 0 … W‑1
                if s[j] == 'A'            // count A’s
                        ++rowCnt[i] , ++colCnt[j]
                // D = rowParity xor colParity[j]
                if s[j] == 'B'
                        D = rowParity ^ colParity[j]
                        add edge (i , j , D) to adjacency of row i and column j
                if s[j] == 'A'            // update parities for later cells
                        rowParity ^= 1
                        colParity[j] ^= 1

// parity test
if some rowCnt[i] is odd or some colCnt[j] is odd → answer 0

// BFS on the bipartite graph, counting components
visited[0 … H+W-1] = false
value   [0 … H+W-1] = 0
components = 0
for v = 0 … H+W-1
        if not visited[v]
                ++components
                visited[v] = true , value[v] = 0
                push v into queue
                while queue not empty
                        pop x
                        if x < H          // a row vertex
                                for (col , D) in rowAdj[x]
                                        y = H + col
                                        need = value[x] xor D
                                        if not visited[y]   visited[y]=true , value[y]=need , push y
                                        else if value[y]!=need  → inconsistency
                        else               // a column vertex
                                for (row , D) in colAdj[x-H]
                                        y = row
                                        need = value[x] xor D
                                        same handling

if inconsistency → answer 0
else answer = powmod(2 , components , MOD)
output answer
```

`#B ≤ H·W ≤ 10⁶`, therefore the whole adjacency list contains at most
`2·10⁶` edges.  
All other structures are linear in `H+W`.  
The algorithm is `O(H·W)` time and `O(H·W)` memory per test case,
the sum over all test cases is at most `10⁶`.

--------------------------------------------------------------------

#### 9.   Correctness Proof  

We prove that the algorithm prints the required number of placements.

---

##### Lemma 1  
In a row (resp. column) the system of equations  
`e[j‑1] + e[j] = h[j]` (resp. the analogous column system)
has a solution **iff** the number of `A` cells in this row (column) is even.
If it has a solution, it has exactly two solutions.

**Proof.**  
Write the equations modulo 2:
`e[j‑1] XOR e[j] = h[j] (mod 2)`.  
For a row the left hand sides XOR to `0` after a full turn,
so the right hand sides must also XOR to `0`,
i.e. the number of odd `h[j]` (exactly the `A` cells) must be even.
Conversely, if this condition holds, the system has rank `W‑1`,
hence exactly one free variable (`e[0]`) and thus two solutions. ∎



##### Lemma 2  
Let `R[i][j]` and `C[j][i]` be the prefix parities defined above.
For every `B`‑cell `(i , j)` the equality  

```
b(i,j) = R[i][j] XOR C[j][i]                     (★)
```

holds, where `b(i,j)=0` means the cell uses vertical edges,
`b(i,j)=1` means it uses horizontal edges.

**Proof.**  
From the row equations we have `b(i,j) = e[i][j‑1]`.  
Walking along the row from the left border,
`e[i][j‑1] = r[i] XOR R[i][j]` (`r[i]=e[i][0]`).  
Analogously, walking from the top of the column gives
`b(i,j) = c[j] XOR C[j][i]` (`c[j]=f[j][0]`).  
Eliminating the free potentials `r[i] , c[j]` yields (★). ∎



##### Lemma 3  
For a row (resp. column) all its `B`‑cells have the same value
`b(i,j)` **iff**   `R[i][j] XOR C[j][i]` is equal for those cells.
Equivalently, the label  

```
D(i,j) = R[i][j] XOR C[j][i]
```

is the label used in equation (6).

**Proof.**  
Equation (★) shows that `b(i,j)` is exactly `D(i,j)`. ∎



##### Lemma 4  
Let the graph `G` be built from all `B`‑cells.
Equation (6) `r[i] XOR c[j] = D(i,j)` is consistent
iff during the BFS no contradiction occurs.

**Proof.**  
The BFS is the usual propagation of potentials in a graph whose edges are
the equations `x⊕y = label`.  
If a vertex is reached a second time with a different implied value,
the xor of the labels along the two different paths would be `1`,
i.e. the equation system is contradictory.
Conversely, if the propagation never meets a conflict,
all equations are mutually compatible, hence a solution exists.
∎



##### Lemma 5  
If the BFS finishes without conflict,
each connected component of `G` admits exactly **two**
assignments of potentials `(r , c)`.  
An isolated vertex (row or column without incident edge)
is a component of size 1 and also admits two assignments.

**Proof.**  
Fix one vertex of a component and set its potential to `0`;
all other vertices are forced uniquely by (6) and the BFS.
Flipping the potentials of **all** vertices of this component
(`x → x⊕1`) leaves every equation unchanged,
hence gives a second distinct solution.
No other solutions exist because all vertices are fixed up to this
global flip. ∎



##### Lemma 6  
The whole grid admits a placement **iff**

* every row and every column contains an even number of `A` cells,
* the BFS on `G` finds no contradiction.

**Proof.**  
*Necessity*  
The “even number of `A`” condition is Lemma&nbsp;1,
necessary for the existence of the horizontal (resp. vertical) edge
assignments in each row/column.
The consistency of the potentials follows from Lemma&nbsp;4,
which is equivalent to the possibility to choose for every `B`‑cell
the same `b(i,j)` from the two points of view (row & column).

*Enough*  
Assume the two conditions hold.
For every row we have two possibilities for its horizontal edges
(Lemma&nbsp;1) – they are exactly the two choices of the row potential `r[i]`.
For every column we have two possibilities for its vertical edges –
the two choices of the column potential `c[j]`.
Because the potentials satisfy (6) (Lemma&nbsp;4), every `B`‑cell receives the
same value `b(i,j)` from its row and its column,
hence the horizontal and vertical edge assignments are compatible.
All vertices then have exactly the required two incident edges,
i.e. a valid placement is obtained. ∎



##### Lemma 7  
Let `C` be the number of connected components of `G`
(including isolated vertices).  
The number of valid placements equals `2^{C}` (mod 998244353).

**Proof.**  
Every component contributes the factor `2` described in Lemma&nbsp;5,
and components are independent.
Thus the total number of placements is the product of `2` over all
components, i.e. `2^{C}`. ∎



##### Lemma 8  
The algorithm outputs `0` exactly when Lemma&nbsp;6 fails,
otherwise it outputs `2^{C}`.

**Proof.**  
The algorithm first checks the parity condition of Lemma&nbsp;1.
If it is violated it prints `0`.  
Otherwise it builds the graph `G` and runs the BFS.
If a conflict occurs it prints `0` (the system of Lemma&nbsp;4 is unsolvable).
If the BFS succeeds, it has counted the components `C` and finally
outputs `2^{C}` (by fast exponentiation). ∎



##### Theorem  
For every test case the program prints, modulo 998244353,
the number of ways to place the tiles so that the line segments have no
dead ends on the torus.

**Proof.**  
By Lemma&nbsp;6 a placement exists exactly when the two conditions
checked by the program hold.
If they do not hold, the correct answer is `0`,
which the program outputs (Lemma&nbsp;8).  
If they hold, Lemma&nbsp;7 states that the number of placements is
`2^{C}`, where `C` is the number of components counted by the program.
Lemma&nbsp;8 shows that the program outputs this value.
Thus the output is correct in all cases. ∎



--------------------------------------------------------------------

#### 10.   Complexity Analysis  

For one test case with `H·W` cells  

*Counting `A` and building the graph* : `O(H·W)` time,  
  at most `2·#B ≤ 2·H·W` adjacency entries.

*BFS* : each edge is examined a constant number of times → `O(H·W)`.

*Memory* :  
  * strings `O(H·W)`  
  * adjacency lists `O(H·W)`  
  * a few integer vectors `O(H+W)`  

Overall  

```
Time   :  O(H·W)      ( ≤ 10⁶ over the whole input )
Memory :  O(H·W)
```

Both satisfy the limits easily.

--------------------------------------------------------------------

#### 11.   Reference Implementation  (GNU‑C++17)

```cpp
#include <bits/stdc++.h>
using namespace std;

const int MOD = 998244353;

long long mod_pow(long long a, long long e) {
    long long r = 1;
    while (e) {
        if (e & 1) r = r * a % MOD;
        a = a * a % MOD;
        e >>= 1;
    }
    return r;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int T;
    if (!(cin >> T)) return 0;
    while (T--) {
        int H, W;
        cin >> H >> W;
        vector<int> rowCnt(H, 0), colCnt(W, 0);
        vector<int> colParity(W, 0);                // C[col][row-1] (parity of A above current row)

        // adjacency lists for the bipartite graph
        vector<vector<pair<int, uint8_t>>> rowAdj(H);
        vector<vector<pair<int, uint8_t>>> colAdj(W);

        for (int i = 0; i < H; ++i) {
            string s; cin >> s;
            int rowParity = 0;                      // R[row][col-1]
            for (int j = 0; j < W; ++j) {
                char ch = s[j];
                if (ch == 'A') {
                    ++rowCnt[i];
                    ++colCnt[j];
                }
                if (ch == 'B') {
                    uint8_t D = (uint8_t)(rowParity ^ colParity[j]);
                    rowAdj[i].push_back({j, D});
                    colAdj[j].push_back({i, D});
                }
                if (ch == 'A') {
                    rowParity ^= 1;
                    colParity[j] ^= 1;
                }
            }
        }

        // parity check
        bool ok = true;
        for (int x : rowCnt) if (x & 1) { ok = false; break; }
        for (int x : colCnt) if (x & 1) { ok = false; break; }

        if (!ok) {
            cout << 0 << '\n';
            continue;
        }

        int N = H + W;                     // total vertices of the bipartite graph
        vector<char> visited(N, 0);
        vector<char> val(N, 0);            // potential 0/1
        long long components = 0;

        queue<int> q;
        for (int v = 0; v < N && ok; ++v) {
            if (visited[v]) continue;
            ++components;
            visited[v] = 1;
            val[v] = 0;
            q.push(v);
            while (!q.empty() && ok) {
                int x = q.front(); q.pop();
                if (x < H) { // row vertex
                    int i = x;
                    for (auto [col, D] : rowAdj[i]) {
                        int y = H + col;
                        char need = val[x] ^ D;
                        if (!visited[y]) {
                            visited[y] = 1;
                            val[y] = need;
                            q.push(y);
                        } else if (val[y] != need) {
                            ok = false;
                            break;
                        }
                    }
                } else { // column vertex
                    int col = x - H;
                    for (auto [row, D] : colAdj[col]) {
                        int y = row;
                        char need = val[x] ^ D;
                        if (!visited[y]) {
                            visited[y] = 1;
                            val[y] = need;
                            q.push(y);
                        } else if (val[y] != need) {
                            ok = false;
                            break;
                        }
                    }
                }
            }
        }

        if (!ok) {
            cout << 0 << '\n';
            continue;
        }
        long long ans = mod_pow(2, components);
        cout << ans << '\n';
    }
    return 0;
}
```

The program follows exactly the algorithm proven correct above
and conforms to the GNU++17 compiler.