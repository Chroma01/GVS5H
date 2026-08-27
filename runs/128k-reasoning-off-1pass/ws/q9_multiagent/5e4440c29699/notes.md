
## ideation
The problem asks for the number of paths in a grid where blocks exist in a "frame" shape (the full rectangle $[0, W] \times [0, H]$ minus the inner rectangle $[L, R] \times [D, U]$). Movement is restricted to positive $x$ and positive $y$ directions.
The set of valid blocks forms the union of four disjoint rectangular regions (strips):
1.  **Bottom Strip**: $x \in [0, W], y \in [0, D-1]$ (if $D > 0$)
2.  **Top Strip**: $x \in [0, W], y \in [U+1, H]$ (if $U < H$)
3.  **Left Strip**: $x \in [0, L-1], y \in [D, U]$ (if $L > 0$)
4.  **Right Strip**: $x \in [R+1, W], y \in [D, U]$ (if $R < W$)

Since these four regions are pairwise disjoint (they do not share any lattice points), the total number of valid paths is simply the sum of the number of valid paths within each of these four regions.
For a single rectangular region of width $w$ and height $h$ (covering lattice points from $0$ to $w$ and $0$ to $h$), the number of paths starting at any block $(x_1, y_1)$ and ending at any block $(x_2, y_2)$ within the rectangle (where $x_2 \ge x_1, y_2 \ge y_1$) is given by:
$$ \sum_{x_1=0}^w \sum_{y_1=0}^h \sum_{x_2=x_1}^w \sum_{y_2=y_1}^h \binom{(x_2-x_1) + (y_2-y_1)}{x_2-x_1} $$
This sum can be computed in $O(1)$ time using combinatorial identities involving binomial coefficients, provided we have precomputed factorials for modular inverse calculations. The constraints $W, H \le 10^6$ allow for $O(N)$ precomputation and $O(1)$ query.

Key steps:
1.  Parse input $W, H, L, R, D, U$.
2.  Define a function `count_paths(w, h)` that calculates the number of paths in a grid of size $w \times h$ (vertices $0..w, 0..h$).
    -   The formula involves sums of the form $\sum \binom{n}{k}$.
    -   Specifically, the total paths in a $w \times h$ grid is $\binom{w+h+2}{w+1} \times \binom{w+h+2}{h+1} \times \frac{1}{w+h+2}$? No, let's derive the exact closed form carefully or implement the $O(1)$ summation logic derived in the thought process:
      Total = $(w+1)(h+1) S_0 - (w+1) S_1 - (h+1) S_2 + S_3$ where $S_k$ are specific sums of binomial coefficients.
      Actually, there is a simpler known identity for this specific problem (sum of paths in a grid):
      The number of paths in a grid of size $W \times H$ (points $0..W, 0..H$) is $\binom{W+H+2}{W+1} \times \frac{W+H+2}{W+H+2} \dots$?
      Let's stick to the derived expansion:
      $Total = \sum_{u=0}^W \sum_{v=0}^H (W-u+1)(H-v+1) \binom{u+v}{u}$.
      Using identities:
      $\sum_{v=0}^H \binom{u+v}{u} = \binom{u+H+1}{u+1}$
      $\sum_{v=0}^H v \binom{u+v}{u} = \dots$
      It turns out the closed form is:
      $Ans = \binom{W+H+2}{W+1} \times \binom{W+H+2}{H+1} \times \frac{1}{W+H+2}$? No.
      Let's re-verify with $W=1, H=1 \to 10$.
      Formula $\binom{1+1+2}{1+1} \times \binom{1+1+2}{1+1} \times \frac{1}{4} = \binom{4}{2}^2 / 4 = 36/4 = 9 \neq 10$.
      Okay, let's use the explicit summation logic with helper functions for $O(1)$ calculation.
      $S_0(n, m) = \binom{n+m+2}{n+1}$
      $S_1(n, m) = \sum_{u=0}^n \sum_{v=0}^m v \binom{u+v}{u} = \sum_{u=0}^n \left( \binom{u+m+2}{u+2} \times (u+m+1) - \dots \right)$?
      Actually, $v \binom{u+v}{u} = v \binom{u+v}{v} = (u+v+1) \binom{u+v}{u} - (u+1) \binom{u+v}{u}$? No.
      $v \binom{u+v}{u} = (u+v) \binom{u+v-1}{u} = (u+v) \binom{u+v-1}{v-1}$.
      Better: $\sum_{v=0}^m v \binom{u+v}{u} = \sum_{v=1}^m v \binom{u+v}{v}$.
      Use identity $\sum_{i=0}^n \binom{i+k}{i} = \binom{n+k+1}{n}$.
      Also $\sum_{i=0}^n i \binom{i+k}{i} = (k+1) \binom{n+k+2}{n-1}$?
      Let's just implement the $O(1)$ summation using the precomputed factorials and the specific identities for $\sum \binom{n}{k}$ and $\sum k \binom{n}{k}$.
      Identity: $\sum_{i=0}^n \binom{i+k}{k} = \binom{n+k+1}{k+1}$.
      Identity: $\sum_{i=0}^n i \binom{i+k}{k} = (k+1) \binom{n+k+1}{k+2} \times (n+1)$? No.
      Let's use the property: $i \binom{i+k}{k} = (k+1) \binom{i+k}{k+1} + k \binom{i+k}{k}$? No.
      $i \binom{i+k}{k} = (i+k-k) \binom{i+k}{k} = (i+k) \binom{i+k}{k} - k \binom{i+k}{k} = (k+1) \binom{i+k+1}{k+1} - k \binom{i+k}{k}$.
      Summing this over $i$:
      $\sum_{i=0}^n i \binom{i+k}{k} = (k+1) \sum \binom{i+k+1}{k+1} - k \sum \binom{i+k}{k}$
      $= (k+1) \binom{n+k+2}{k+2} - k \binom{n+k+1}{k+1}$.
      This allows computing the required sums in $O(1)$.

3.  Calculate the dimensions of the 4 strips.
    -   Bottom: $w=W, h=D-1$. If $D=0$, skip.
    -   Top: $w=W, h=H-U-1$. If $U=H$, skip.
    -   Left: $w=L-1, h=U-D$. If $L=0$, skip.
    -   Right: $w=W-R-1, h=U-D$. If $R=W$, skip.
4.  Sum the results modulo 998244353.
