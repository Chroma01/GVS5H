- **Edge variables:** Let \(h_{i,j}\) indicate whether the segment reaches the right edge of cell \((i,j)\), and let \(v_{i,j}\) indicate whether it reaches the bottom edge. The left and top edge states are \(h_{i,j-1}\) and \(v_{i-1,j}\), with indices taken cyclically.
- **Tile equations:** Type A connects adjacent edges, so exactly one of its two horizontal edge states is present and exactly one of its two vertical edge states is present:
  \(h_{i,j}\oplus h_{i,j-1}=1\) and \(v_{i,j}\oplus v_{i-1,j}=1\).
  Type B connects opposite edges, so each pair is equal:
  \(h_{i,j}=h_{i,j-1}\) and \(v_{i,j}=v_{i-1,j}\). Its segment is either horizontal or vertical, hence \(h_{i,j}\oplus v_{i,j}=1\).
- **Toroidal closure:** XORing the horizontal equation around a row shows every row must contain an even number of A tiles. Similarly, every column must contain an even number of A tiles. These conditions are checked directly.
- **Row and column parameters:** Choose \(r_i=h_{i,0}\) and \(c_j=v_{0,j}\). After propagation,
  \(h_{i,j}=r_i\oplus\) (A-prefix in row \(i\), columns \(1..j\)),
  and
  \(v_{i,j}=c_j\oplus\) (A-prefix in column \(j\), rows \(1..i\)).
- **Parity DSU:** Every B cell yields one equation \(r_i\oplus c_j = 1\oplus\) the two corresponding prefixes. The DSU stores XOR parity to each representative, detects contradictions, and leaves one free binary choice per connected component.
- **Counting:** Each consistent assignment of all \(r_i,c_j\) uniquely determines every edge state and therefore exactly one tile placement. The answer is \(2^{\text{number of DSU components}}\) modulo 998244353.
- **Complexity:** The algorithm uses \(O(HW)\) time and \(O(HW+H+W)\) memory per test batch, with total grid area bounded by \(10^6\).
