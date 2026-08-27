Merge adjacent bad intervals into maximal bad blocks, then form the good gaps before, between, and after them.  
Because B≤20, any jump from an earlier gap lands in the first B squares of the target gap, and only the last B squares of a gap can jump out, so boundary bit masks are sufficient.  
Process gaps left to right, accumulating an entry mask for each gap from all earlier gaps that can reach it in one jump.  
Within a good gap, a distance D from an entry square is reachable iff D=0 or there exists k≥1 with kA≤D≤kB, since every integer in [kA,kB] is a sum of k allowed jumps.  
Use this test to propagate an entry mask to the gap's last-B mask, then use single jumps of length A..B to OR possible landings into later gaps' first-B masks.  
If the final gap's last-B mask contains square N, print Yes; otherwise print No.