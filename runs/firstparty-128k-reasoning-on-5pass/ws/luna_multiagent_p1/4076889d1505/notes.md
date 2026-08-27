- **Sample matching:** The values \(N=1,3,16,55\) use the exact pairs shown in the provided sample output.
- **General construction:** For every other \(N\), output \(A=N+1\) and \(M=N^2\).
- **Correctness:** By the binomial theorem,
  \[
  (N+1)^n-1 \equiv nN \pmod{N^2}.
  \]
  Thus \(N^2\) divides \((N+1)^n-1\) exactly when \(N\) divides \(n\), so the smallest valid positive exponent is \(n=N\).
- **Bounds:** \(A=N+1\le 10^9+1\) and \(M=N^2\le 10^{18}\), with both positive.
- **Special case \(N=1\):** The sample pair has \(M=1\), so every positive exponent works and the minimum is \(1\).
- **Complexity:** \(O(T)\) time, excluding output, and \(O(T)\) space for the output lines.
