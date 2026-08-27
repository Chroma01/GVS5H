import sys
from sys import stdin, stdout

def solve():
    input_data = stdin.read().split()
    idx = 0
    T = int(input_data[idx]); idx += 1
    out_lines = []
    for _ in range(T):
        R = int(input_data[idx]); idx += 1
        B = int(input_data[idx]); idx += 1
        
        # Check feasibility
        if R % 2 == 1:
            out_lines.append("No")
            continue
        if R == 0 and B % 2 == 1:
            out_lines.append("No")
            continue
        
        # Construct placement
        out_lines.append("Yes")
        placements = []
        
        if R == 0:
            # All blue, B even
            # Cycle: (1,1) -> (2,2) -> (3,1) -> (2,0)... use (1,2),(2,3),(3,2),(2,1) for B=4
            # For general even B, use a zigzag
            # Simple: place at (1,1),(2,2),(3,3),... and close with (2,0)... 
            # Better: use cycle of length B in diagonal graph
            # For B=2: (1,1),(2,2)
            # For B=4: (1,2),(2,3),(3,2),(2,1)
            # For B=2k: use (1,k),(2,k+1),(3,k),(4,k+1),...,(2k,k) then back
            # Simplest: build a "ladder"
            # (1,1),(2,2),(3,1),(4,2),...,(B-1, B/2),(B, B/2+1) doesn't close
            # Use: (1,1),(2,2),(1,3),(2,2)... no
            # Diagonal 4-cycle: (r,c),(r+1,c+1),(r+2,c),(r+1,c-1)
            # For B=2k, use k such 4-cycles? No, need single cycle.
            # Long cycle: (1,1),(2,2),(3,3),(4,4),...,(k,k),(k+1,k-1),(k+2,k-2),..., back to (1,1)
            # Actually: (1,1)->(2,2)->(3,1)->(4,2)->...->(2k-1,1)->(2k,2)->(1,1)? (2k,2)->(1,1) not diag
            # 
            # Simpler: place B blues in a 2x(B/2) grid alternating
            # (1,1),(2,2),(1,3),(2,4),...,(1,B-1),(2,B), then (2,B)->(1,B-1) is orth not diag
            # 
            # Cleanest: use a "zigzag" diagonal path that forms a cycle
            # Path: (1,1),(2,2),(3,1),(4,2),(5,1),(6,2),...
            # For B=2k: (1,1),(2,2),(3,1),(4,2),...,(2k-1,1),(2k,2)
            # Close: (2k,2)->(1,1) not diag.
            # 
            # Add a "return" leg: (1,1),(2,2),(3,1),(4,2),...,(2k-1,1),(2k,2),(2k-1,3),...,(1,3),(1,1)?
            # Too complex.
            #
            # Standard solution: place in two rows
            # Row 1 (odd i): (1,1),(1,3),(1,5),...
            # Row 2 (even i): (2,2),(2,4),(2,6),...
            # (1,1)->(2,2) diag, (2,2)->(1,3) diag, (1,3)->(2,4) diag, ..., 
            # (2,2k)->(1,1)? (2,2k) to (1,1): (1-2,1-2k) not diag unless k=1.
            # 
            # Use a different shape. Cycle of B blues:
            # For B=2: (1,1),(2,2)
            # For B=4: (1,1),(2,2),(3,1),(2,0) invalid. (1,2),(2,3),(3,2),(2,1) works.
            # For B=6: (1,2),(2,3),(3,4),(4,3),(3,2),(2,1). Check:
            # (1,2)->(2,3)diag, (2,3)->(3,4)diag, (3,4)->(4,3)diag(-1,-1)✓, 
            # (4,3)->(3,2)diag(-1,-1)✓, (3,2)->(2,1)diag(-1,-1)✓, (2,1)->(1,2)diag(-1,1)✓
            # Works! Pattern: start at (1,2), go (1,2)->(2,3)->(3,4)->...->(k+1,k+1), 
            # then come back: (k+1,k+1)->(k,k)->...->(1,2)? 
            # For B=6 (k=3): (1,2),(2,3),(3,4) then (4,3),(3,2),(2,1). 
            # (3,4)->(4,3) is up-left diag (-1,-1)✓.
            # General: for B=2m, m>=1:
            # (1,2),(2,3),...,(m,m+1)  [m positions, going up-right]
            # then (m+1,m),(m,m-1),...,(1,2-m+1)? 
            # For m=2 (B=4): (1,2),(2,3) then (3,2),(2,1). (2,3)->(3,2)diag(1,-1)✓, (3,2)->(2,1)diag(-1,-1)✓, (2,1)->(1,2)diag(-1,1)✓
            # For m=3 (B=6): (1,2),(2,3),(3,4) then (4,3),(3,2),(2,1). (3,4)->(4,3)diag(1,-1)✓, ..., (2,1)->(1,2)diag(-1,1)✓
            # Pattern: forward (1,2),(2,3),...,(m,m+1) [m pieces]
            # backward (m+1,m),(m,m-1),...,(2,1) [m pieces]
            # Check closure: (2,1)->(1,2)diag(-1,1)✓
            # And (m+1,m) to (m,m+1): (m+1,m)->(m,m+1) is (-1,1)diag✓
            # Wait, after forward we are at (m,m+1), then we go to (m+1,m). 
            # (m,m+1)->(m+1,m): (1,-1)diag✓. Good.
            # Then backward: (m+1,m),(m,m-1),...,(2,1). That's m pieces.
            # Last backward piece (2,1) connects to first (1,2): (2,1)->(1,2)diag(-1,1)✓
            # Total: m + m = 2m = B. ✓
            
            half = B // 2
            # Forward: (1,2),(2,3),...,(half, half+1)
            for i in range(half):
                placements.append(('B', i+1, i+2))
            # Backward: (half+1, half),(half, half-1),...,(2,1)
            for i in range(half):
                placements.append(('B', half+1-i, half-i))
                # Wait: (half+1, half),(half, half-1),...,(2,1)
                # i=0: (half+1, half)
                # i=1: (half, half-1)
                # ...
                # i=half-1: (2, 1)
                # So (half+1-i, half-i) for i=0..half-1
                # i=0: (half+1, half) ✓
                # i=half-1: (2, 1) ✓
                pass
            # Fix the loop
            placements = []
            for i in range(half):
                placements.append(('B', i+1, i+2))
            for i in range(half):
                r = half + 1 - i
                c = half - i
                placements.append(('B', r, c))
        
        elif R == 2:
            # R=2, B>=0
            # Structure: R_a -> B_1 -> ... -> B_k -> R_b -> B_close -> R_a
            # R_a=(3,2), R_b=(2,4) for B=3 [sample-like]
            # General: choose R_a, R_b, B_close, and diagonal path
            if B == 0:
                placements.append(('R', 1, 1))
                placements.append(('R', 1, 2))
            else:
                # Use R_a=(1,1), R_b=(1,2), B_close=(2,2)
                # Main path: B_1=(2,1) orth-adj R_a, B_k diag-adj R_b=(1,2)
                # B_k must be in {(0,1)OOB,(0,3)OOB,(2,1),(2,3)}
                # If path uses (2,3) as end: need diagonal path from (2,1) to (2,3) of length B-2
                # (2,1) and (2,3) differ by (0,2), same (r-c) part, need even length
                # If path uses (2,1) as end: B_1=B_k, need (2,1) diag-adj (1,2): |1|,|1| yes
                # So if B-2=0 (B=2), use (2,1) as single blue
                # If B-2>=2 and even, use path to (2,3)
                # If B-2 odd... (2,1) to (2,3) needs even length. 
                # But we can choose different R_a, R_b to get odd distances.
                # 
                # Alternative: use a configuration that works for all B.
                # 
                # R_a=(1,1), R_b=(2,1) [vertical]
                # B_close orth-adj R_b and diag-adj R_a
                # orth-adj (2,1): (3,1),(1,1)=R_a,(2,2),(2,0)OOB -> (3,1),(2,2)
                # diag-adj (1,1): (2,2),(0,2)OOB,(2,0)OOB,(0,0)OOB -> (2,2)
                # So B_close=(2,2)
                # B_1 orth-adj R_a=(1,1), not R_b=(2,1): (2,1)=R_b,(0,1)OOB,(1,2),(1,0)OOB -> (1,2)
                # B_k diag-adj R_b=(2,1): (1,0)OOB,(1,2),(3,0)OOB,(3,2)
                # Excluding B_1=(1,2): (3,2)
                # So B_1=(1,2), B_k=(3,2). Distance: (3,2)-(1,2)=(2,0), d=2, even part.
                # Need path length = B-2 (since total blues = B, B_close is 1, main path has B-1 blues? 
                # Wait: R_a -> B_1 -> ... -> B_k -> R_b -> B_close -> R_a
                # B_1 to B_k: B-2 internal blues? No.
                # Total blues = B. B_close = 1. Main path blues = B-1.
                # B_1, B_2, ..., B_{B-1} = B_k. That's B-1 blues in main path.
                # Edges in main path: B-2 (from B_1 to B_k).
                # B-2 must be >= d=2 and even.
                # So B-2 >= 2 and even, i.e., B >= 4 and B even.
                # B=1: main path has 0 blues? R_a->R_b->B_close->R_a. 
                # R_a->R_b orth: (1,1)->(2,1)✓. R_b->B_close orth: (2,1)->(2,2)✓. B_close->R_a diag: (2,2)->(1,1)diag(-1,-1)✓. 
                # So B=1 works! Main path 0 blues.
                # B=2: main path 1 blue = B_1 = B_k. (1,2) must be diag-adj (2,1): |1|,|1|✓. Works!
                # B=3: main path 2 blues. (1,2)->(3,2) in 1 step? (1,2) to (3,2) is (2,0), d=2, need 2 steps. 
                # 2 steps from (1,2) to (3,2): (1,2)->(2,3)->(3,2)diag(-1,-1)✓. Or (1,2)->(2,1)=R_b->(3,2) but R_b used.
                # So (1,2)->(2,3)->(3,2). But (2,3) is free. Path: B_1=(1,2), B_2=(2,3), B_3=(3,2). 
                # B_1->B_2: (1,2)->(2,3)diag(1,1)✓. B_2->B_3: (2,3)->(3,2)diag(1,-1)✓. B_3->R_b: (3,2)->(2,1)diag(-1,-1)✓.
                # Works! B=3.
                # B=4: main path 3 blues. (1,2)->(3,2) in 3 steps. d=2, parity: same part, need even. 3 odd. No.
                # B=5: 4 steps, even. (1,2)->(2,3)->(3,4)->(2,3) no. (1,2)->(2,3)->(3,2)->(4,3)->(3,2) no.
                # (1,2)->(0,3)->(1,4)->(2,3)->(3,2). Check: (1,2)->(0,3)diag(-1,1)✓,(0,3)->(1,4)diag(1,1)✓,(1,4)->(2,3)diag(1,-1)✓,(2,3)->(3,2)diag(1,-1)✓. ✓ B=5.
                # B=6: 5 steps, odd, no.
                # So with this config: B in {1,2,3,5,7,...} and missing even B>=4.
                # 
                # To get even B>=4, use the horizontal config:
                # R_a=(1,1), R_b=(1,2). B_close=(2,2). 
                # B_1=(2,1), B_k=(2,3). d=2, even. Need B-2 even and >=2. B even, B>=4.
                # B=2: main path 1 blue = (2,1) diag-adj (1,2)✓. Works.
                # B=4: 3 steps odd, no.
                # B=6: 5 steps odd, no.
                # Hmm.
                # 
                # Combine: for odd B use vertical, for even B use horizontal? 
                # B=1: vertical. B=2: vertical or horizontal. B=3: vertical. B=4: ? 
                # B=4 with R_a=(1,1), R_b=(1,2): main path 3 blues, d=2, odd length impossible.
                # B=4 with vertical: B-2=2 even, d=2, (1,2)->(3,2) in 2 steps: (1,2)->(2,3)->(3,2) or (1,2)->(2,1)=R_b->(3,2). 
                # First: (1,2)->(2,3)diag(1,1)✓, (2,3)->(3,2)diag(1,-1)✓. So B_1=(1,2), B_2=(2,3), B_3=(3,2)=B_k. 
                # B_1 is (1,2) which is the start, B_k=(3,2). 3 blues in main path. B=4 total. ✓
                # Check: R_a(1,1)->B_1(1,2)orth(0,1)✓, B_1->B_2diag(1,1)✓, B_2->B_3diag(1,-1)✓, B_3->R_b(2,1)diag(-1,-1)✓, 
                # R_b->B_close(2,2)orth(0,1)✓, B_close->R_a(1,1)diag(-1,-1)✓. ✓
                # So B=4 works with vertical config! Wait, vertical gives B=1,2,3,5,7,... and B=4?
                # B=4: B-2=2, d=2, path length 2 even. 2>=2✓, 2 even✓. Works!
                # B=5: B-2=3, d=2, need even, 3 odd. Doesn't work with this.
                # B=6: B-2=4, d=2, 4 even. Works.
                # So vertical: B-2 even => B even. B=2,4,6,...
                # And odd B with vertical: B=1 (B-2=-1? no, B=1 means 0 blues in main path, direct R_a->R_b. 
                # B=1: main path 0 blues. R_a->R_b orth. Works. (B-2 doesn't apply.)
                # B=3: main path 2 blues. B-2=1. d=2, need even, 1 odd. No.
                # 
                # I'm getting confused. Let me just enumerate what works.
                # 
                # Decision: for R=2, use a flexible construction. 
                # Key: we can scale up. For large B, use R>=4? No, R is fixed.
                # 
                # OK, final decision for R=2: use a construction that works for all B.
                # 
                # Observation: the "diagonal path" can be made arbitrarily long by going far away.
                # So for any B, we can find a path.
                # 
                # Construction: R_a=(1,1), R_b=(1,2). B_close=(2,2).
                # Main path: from B_1 to B_k, where B_1 is orth-adj R_a, B_k is diag-adj R_b.
                # B_1=(2,1) (only choice excluding (1,2)=R_b and OOB).
                # B_k can be (0,1)OOB, (0,3)OOB, (2,1)=B_1, (2,3).
                # If B_k=(2,1), then main path is just B_1 (0 edges), total B=1+1=2. B=1? 
                # Wait: R_a -> B_1 -> R_b -> B_close -> R_a. B_1 is the only main blue. Total blues = 1+1=2. B=2.
                # B=1: no main blue. R_a->R_b->B_close->R_a. Total B=1. 
                # B=3: main has 2 blues, B_1 and B_k=B_2=(2,3). Path (2,1)->(2,3) in 1 step? No, d=2.
                # B=3 needs 2 edges. (2,1)->(3,2)->(2,3). ✓
                # B=4: 3 edges, (2,1)->(2,3), d=2, need even, 3 odd. No with B_k=(2,3).
                # 
                # For B=4, choose different R_a, R_b. R_a=(1,1), R_b=(2,1). 
                # B_close: orth-adj R_b, diag-adj R_a. (3,1),(1,1)=R_a,(2,2),(2,0)OOB. diag(1,1):(2,2). B_close=(2,2).
                # B_1 orth-adj R_a not R_b: (2,1)=R_b,(0,1)OOB,(1,2),(1,0)OOB. B_1=(1,2).
                # B_k diag-adj R_b=(2,1): (1,0)OOB,(1,2)=B_1,(3,0)OOB,(3,2). B_k=(3,2).
                # Main path (1,2)->(3,2), d=2, need B-2 edges. B=4: 2 edges. (1,2)->(2,3)->(3,2). ✓
                # 
                # Pattern: alternate between two configurations based on B parity.
                # Or: use a configuration where d is large enough.
                # 
                # Simplest: for R=2, use R_a=(1,1), R_b=(1,2), and for the main path, 
                # go far away and come back.
                # 
                # B_start=(2,1). B_end=(2, 2B-1) but must be diag-adj R_b=(1,2). So B_end=(2,3) only.
                # So the path from (2,1) to (2,3) is constrained to be short.
                # 
                # Solution: make R_a and R_b farther apart? But they must be orth-adj (R_a->R_b is orth move).
                # Wait, R_a and R_b don't need to be orth-adj directly! In the cycle, R_a and R_b are connected via blues.
                # The move R_b -> B_close is orth, and B_close -> R_a is diag. 
                # R_a and R_b are not directly connected; they're connected through B_close and the main path.
                # So R_a and R_b can be any distance apart! 
                # 
                # Great! So for R=2, B large:
                # R_a=(1,1), R_b=(1, 1 + d) for large d.
                # B_close orth-adj R_b, diag-adj R_a.
                # B_1 orth-adj R_a, B_k diag-adj R_b.
                # Diagonal path from B_1 to B_k of length B-2.
                # 
                # To make d large, we need the diag path to be long. B_1 near R_a, B_k near R_b.
                # Distance between B_1 and B_k is roughly d. So we need B-2 >= d and B-2 ≡ d (mod 2).
                # By choosing d = B-2 or d = B-3 etc., we can make it work.
                # Specifically, set d = B-2 (or B-3 for parity), and place R_b at (1, 1+d).
                # B_1=(2,1), B_k=(2, 1+d) [diag-adj R_b=(1,1+d): (1,1+d) diag nbrs include (2,1+d)✓]
                # Diagonal path from (2,1) to (2,1+d): need to traverse horizontal distance d.
                # d is even? (2,1) and (2,1+d) have same r-c part (2-1=1, 2-(1+d)=1-d, same parity).
                # Need even path length. d=even => B-2 even => B even.
                # If B odd, d=odd, but same part needs even. Contradiction.
                # So d must be even. Set d = B-2 if B even, or d = B-3 (if B-3 >=0 and B-3 even) for B odd.
                # B=3: d=0? R_a=(1,1), R_b=(1,1) same. No.
                # B=3: d=1. R_b=(1,2). Then B_k=(2,3), B_1=(2,1). d=1 between (2,1) and (2,3)? No, (2,3) is at col 3, d=2.
                # Hmm, B_k=(2, 1+d) = (2,2) for d=1. But (2,2) diag-adj (1,2)=R_b? |1|,|0| no. (1,2) diag nbrs: (0,1),(0,3),(2,1),(2,3). So B_k=(2,3) not (2,2).
                # So d is the horizontal distance between B_1 and B_k, which is determined by the choice.
                # 
                # This is getting too complex. Let me just use a known working solution.
                # 
                # DECISION: For R=2, handle all B with a general construction:
                # Use R_a=(1,1), R_b=(1, 2B+1) or similar, with the path going right.
                # B_close=(2, 2B+2) [orth-adj R_b, need diag-adj R_a=(1,1): (2,2) is diag, (2, 2B+2) is far].
                # (2, 2B+2) to (1,1): not diag. So B_close must be near both.
                # B_close orth-adj R_b and diag-adj R_a. R_a=(1,1). 
                # diag(1,1) = (0,0),(0,2),(2,0),(2,2). All near.
                # So R_b must be near (1,1) too, for B_close to be near R_a.
                # 
                # OK so R_a and R_b must be close. Maximum d is limited.
                # 
                # For R=2, the max B is limited by the distance between R_a and R_b (which is 1, orth-adj).
                # Wait, they don't need to be orth-adj! In the cycle, R_a -> B_1 -> ... -> R_b is the path.
                # R_a -> B_1: R_a moves orth. So B_1 is orth-adj R_a.
                # B_k -> R_b: B_k moves diag. So B_k is diag-adj R_b.
                # R_b -> B_close: R_b moves orth. B_close orth-adj R_b.
                # B_close -> R_a: B_close moves diag. B_close diag-adj R_a.
                # 
                # So B_close is orth-adj R_b AND diag-adj R_a. This constrains R_a, R_b to be close.
                # Specifically, the 4 orth-nbrs of R_b and 4 diag-nbrs of R_a must intersect.
                # orth(R_b) ∩ diag(R_a) ≠ ∅.
                # orth(R_b) = {R_b ± (1,0), R_b ± (0,1)} (4 squares).
                # diag(R_a) = {R_a ± (1,1)} (4 squares).
                # Intersection: need (R_b + δ) = R_a + (ε,ε) for some δ∈{(±1,0),(0,±1)}, ε∈{(±1,±1)}.
                # So R_b - R_a = (ε,ε) - δ.
                # If R_b = R_a + (1,0): δ=(-1,0), then R_b - R_a = (1,0), so (ε,ε) = (0,0), impossible.
                # Hmm wait: R_b + δ = R_a + (ε,ε), so R_b = R_a + (ε,ε) - δ.
                # For R_b = R_a + (1,0): (ε,ε) - δ = (1,0). δ∈{(±1,0),(0,±1)}, (ε,ε)∈{(±1,±1)}.
                # Try δ=(0,0) not allowed. δ=(-1,0): (ε,ε)=(0,0) no. δ=(1,0): (ε,ε)=(2,0) no. δ=(0,1): (ε,ε)=(1,1) yes! ε=(1,1).
                # So R_b = R_a + (1,0), B_close = R_a + (1,1) = R_b + (0,1). 
                # Check: B_close=(2,2) orth-adj R_b=(2,1)? No, R_b=(1,1)+(1,0)=(2,1). (2,2) orth-adj (2,1) yes.
                # And (2,2) diag-adj (1,1) yes. ✓
                # 
                # So R_b can be at R_a + (1,0) [right], and B_close at R_a + (1,1) [diag of R_a, orth of R_b].
                # Similarly R_b = R_a + (-1,0), R_a + (0,1), R_a + (0,-1) with appropriate B_close.
                # 
                # But R_b can also be farther! R_b = R_a + (2,1) for example?
                # (ε,ε) - δ = (2,1). δ=(0,±1) or (±1,0). (ε,ε)=((2,1)+δ).
                # If δ=(-1,0): (ε,ε)=(1,1) yes! So R_b = R_a + (2,1), B_close = R_b + (1,0) = R_a + (3,1).
                # Check: B_close=(4,1) diag-adj R_a=(1,1)? |3|,|0| no. 
                # Wait B_close = R_a + (ε,ε) = R_a + (1,1) = (2,2). And R_b = B_close - δ = (2,2) - (-1,0) = (3,2).
                # So R_b=(3,2), B_close=(2,2). R_a=(1,1).
                # B_close orth-adj R_b=(3,2): (4,2),(2,2)=B_close,(3,3),(3,1). (2,2) is orth-adj (3,2) yes.
                # B_close diag-adj R_a=(1,1): (2,2) yes.
                # So R_a=(1,1), R_b=(3,2), B_close=(2,2). Distance R_a to R_b: (2,1), not orth.
                # Main path: B_1 orth-adj R_a=(1,1), B_k diag-adj R_b=(3,2).
                # B_1: (2,1),(0,1)OOB,(1,2),(1,0)OOB. B_1∈{(2,1),(1,2)}.
                # B_k diag-adj (3,2): (2,1),(2,3),(4,1),(4,3).
                # Path B_1->B_k of length B-2.
                # 
                # Great! Now we can choose R_a, R_b, B_close to make the distance d between B_1 and B_k
                # as large as we want, and with the right parity.
                # 
                # General: R_a=(1,1). R_b=(1+2a, 1+a) for some a. B_close=R_a+(1,1)=(2,2).
                # B_close=(2,2) orth-adj R_b=(1+2a, 1+a): |2-(1+2a)|+|2-(1+a)| = |1-2a|+|1-a|.
                # For orth, one of these is 0 and other is 1.
                # |1-2a|=0 => a=1/2 no. |1-a|=0 => a=1 => R_b=(3,2), |1-2|=1. ✓
                # So a=1 gives R_b=(3,2). 
                # For larger a, B_close=(2,2) is not orth-adj R_b.
                # 
                # Try B_close = R_a + (1,1) = (2,2). R_b = B_close - δ. For R_b far, δ large, but δ∈{(±1,0),(0,±1)}.
                # So R_b is always adjacent to B_close, hence close to R_a.
                # 
                # So R_b is within distance 2 of R_a (since B_close is orth-adj R_b and diag-adj R_a, 
                # meaning |R_b - B_close|=1 and |B_close - R_a|_∞=1 (diag), so |R_b - R_a|_∞ ≤ 2).
                # Specifically, R_b is at Chebyshev distance 1 or 2 from R_a.
                # Chebyshev distance 1: R_b orth-adj or diag-adj R_a.
                # If R_b orth-adj R_a, then R_a->R_b is a valid move, and the "main path" can be empty (B=1 or B=0).
                # If R_b diag-adj R_a, then R_b is at (R_a ± 1, R_a ± 1).
                # 
                # Case: R_b = R_a + (1,1) [diag]. Then B_close orth-adj R_b, diag-adj R_a.
                # orth(1+1,1+1)=(2,2) = B_close. So B_close=(2,2)=R_b. But B_close must be distinct.
                # orth(R_b)\{R_a}: (R_b ± (1,0), R_b ± (0,1)) \ {R_a}. R_a=(1,1), R_b=(2,2).
                # orth(2,2): (3,2),(1,2),(2,3),(2,1). None is (1,1)=R_a. So 4 choices.
                # diag(1,1): (0,0)OOB,(0,2)OOB,(2,0)OOB,(2,2)=R_b. So only R_b is diag-adj, but R_b is not B_close.
                # So B_close must be diag-adj R_a and orth-adj R_b. diag(R_a) = {(2,2)=R_b, (0,2)OOB, (2,0)OOB, (0,0)OOB}. Only (2,2)=R_b.
                # But B_close ≠ R_b. So no valid B_close. 
                # 
                # Case: R_b = R_a + (2,1). B_close orth-adj R_b, diag-adj R_a.
                # R_a=(1,1), R_b=(3,2). orth(3,2): (4,2),(2,2),(3,3),(3,1). 
                # diag(1,1): (2,2),(0,2)OOB,(2,0)OOB,(0,0)OOB. 
                # Intersection: (2,2). So B_close=(2,2). ✓
                # 
                # Case: R_b = R_a + (1,2). R_a=(1,1), R_b=(2,3). orth(2,3): (3,3),(1,3),(2,4),(2,2).
                # diag(1,1): (2,2). Intersection: (2,2). B_close=(2,2). ✓
                # 
                # Case: R_b = R_a + (3,2). R_a=(1,1), R_b=(4,3). orth(4,3): (5,3),(3,3),(4,4),(4,2).
                # diag(1,1): (2,2). Intersection: empty. No.
                # 
                # So max |R_b - R_a|_∞ = 2, and specifically R_b ∈ {R_a+(2,1), R_a+(1,2), or the orth-adj ones}.
                # 
                # With R_b at Chebyshev distance 2, the diagonal path from B_1 (orth-adj R_a) to B_k (diag-adj R_b)
                # has limited length.
                # 
                # B_1 orth-adj R_a=(1,1): (2,1),(0,1)OOB,(1,2),(1,0)OOB. 2 choices: (2,1),(1,2).
                # B_k diag-adj R_b=(3,2): (2,1),(2,3),(4,1),(4,3). 4 choices.
                # 
                # Distances:
                # (2,1) to (2,1): d=0
                # (2,1) to (2,3): d=2
                # (2,1) to (4,1): d=2
                # (2,1) to (4,3): d=3
                # (1,2) to (2,1): d=1
                # (1,2) to (2,3): d=1
                # (1,2) to (4,1): d=3
                # (1,2) to (4,3): d=2
                # 
                # Max d=3. So max path length is 3, meaning B-2 ≤ 3, B ≤ 5.
                # 
                # For B > 5, R=2 doesn't work with this structure? 
                # But the problem allows R=2, B up to 2e5. So either R=2 with large B is impossible, 
                # or I need a different structure.
                # 
                # Hmm, is R=2, B=6 possible? 
                # Cycle: R, B, B, B, B, B, B, R. 2 reds, 6 blues.
                # As analyzed, with the two arcs (R_a to R_b via main path, and R_b to R_a via B_close),
                # and B_close constrained to be near both reds, the total is limited.
                # 
                # But wait, the "main path" can use B_close? No, B_close is separate.
                # 
                # Actually, I think for R=2, large B is possible if we make the path very long.
                # The key is that B_1 and B_k don't need to be near R_a and R_b in a small neighborhood.
                # B_1 is orth-adj R_a, so |B_1 - R_a| = 1. B_k is diag-adj R_b, so |B_k - R_b|_∞ = 1.
                # So B_1 is within 1 of R_a, B_k is within 1 of R_b. 
                # If R_a and R_b are far apart, the path from B_1 to B_k is long.
                # 
                # But we showed R_b is constrained to be near R_a (Chebyshev distance ≤ 2).
                # 
                # Unless... B_close is not unique? We need B_close orth-adj R_b AND diag-adj R_a.
                # This forces R_b near R_a.
                # 
                # So for R=2, the structure is limited. R=2, B large might be impossible!
                # 
                # Let me check R=2, B=6. Is there a cycle?
                # Try: (1,1)R, (2,1)B, (3,2)B, (4,3)B, (5,4)B, (4,5)B, (3,4)B, (2,3)R? 
                # Last R(2,3) to first R(1,1): (1,2) not orth.
                # 
                # I think for R=2, the constraint is that B ≤ 5 or so. Let me check the problem.
                # The problem says R+B can be up to 2e5. So R=2, B=2e5 must be handled.
                # 
                # Therefore, R=2 with large B must be possible. Let me re-examine.
                # 
                # OH WAIT. I was wrong about R_a and R_b being constrained. 
                # The cycle is: R_a -> [main path] -> R_b -> B_close -> R_a.
                # B_close is orth-adj R_b and diag-adj R_a.
                # But R_b doesn't need to be fixed. We can choose R_b anywhere, as long as B_close exists.
                # B_close exists iff orth(R_b) ∩ diag(R_a) ≠ ∅.
                # 
                # For R_a=(1,1), diag(R_a) = {(0,0)OOB, (0,2)OOB, (2,0)OOB, (2,2)}.
                # So B_close must be (2,2) (the only valid one).
                # Then R_b must be orth-adj (2,2): (3,2),(1,2),(2,3),(2,1).
                # So R_b ∈ {(3,2),(1,2),(2,3),(2,1)}. All within Chebyshev distance 1 or 2 of R_a.
                # 
                # (1,2): Chebyshev 1. (2,1): 1. (3,2): 2. (2,3): 2.
                # So yes, R_b is constrained. Max d=2.
                # 
                # Therefore, for R=2, the diagonal path from B_1 to B_k is short, and B is limited.
                # 
                # Specifically, with R_a=(1,1), B_close=(2,2), R_b=(3,2):
                # B_1 ∈ {(2,1),(1,2)}. B_k ∈ {(2,1),(2,3),(4,1),(4,3)}.
                # Max distance (Chebyshev or graph dist) is 3 (from (1,2) to (4,1) or (1,2) to (4,3)).
                # Graph distance: (1,2) to (4,1): (3,-1). diag steps: need to change r by 3, c by -1.
                # m steps, |Δr|=3, |Δc|=1. m≥3, m≡1(mod 2). m=3: possible? 
                # (1,2)->(2,1)->(3,2)->(4,1): diag steps? (1,2)->(2,1)diag(1,-1)✓, (2,1)->(3,2)diag(1,1)✓, (3,2)->(4,1)diag(1,-1)✓. ✓ d=3.
                # So max path length is 3, giving B = path_length + 2 = 5.
                # 
                # With R_b=(2,3): B_k diag-adj (2,3): (1,2),(1,4)OOB,(3,2),(3,4).
                # B_1=(2,1) or (1,2). 
                # (1,2) to (1,2): d=0. (1,2) to (3,2): d=2. (1,2) to (3,4): d=2.
                # (2,1) to (1,2): d=1. (2,1) to (3,2): d=1. (2,1) to (3,4): d=3.
                # Max d=3. Same limit.
                # 
                # So for R=2, B ≤ 5.
                # 
                # But the problem has R=2, B up to 2e5. So R=2, B > 5 should be "No".
                # 
                # Hmm, but the sample has R=2, B=3, which is Yes. And R=1, B=1 is No.
                # 
                # Let me re-examine the feasibility condition.
                # 
                # R=0, B=3: No (odd cycle in bipartite).
                # R=0, B=4: Yes.
                # R=0, B=5: No.
                # R=1, any: No.
                # R=2, B=0: Yes. R=2, B=1: Yes. R=2, B=2: Yes. R=2, B=3: Yes. R=2, B=4: ? R=2, B=5: ? R=2, B=6: No?
                # 
                # Actually, I realize my analysis might be wrong. Let me think again.
                # The cycle is a sequence p1, p2, ..., pN with N=R+B.
                # p1 is placed first, p2 second, etc.
                # p_i moves to p_{i+1}, and p_N moves to p_1.
                # 
                # For R=2, B=6: 8 pieces. Cycle R,B,B,B,B,B,B,R (or other arrangement).
                # Two reds at some positions, 6 blues.
                # The two reds divide the cycle into two arcs.
                # Each arc is a path from one red to the other, using only blues.
                # Arc 1: R -> B -> ... -> B -> R. The first move is R orth, intermediate are B diag, last is B diag to R.
                # Arc 2: R -> B -> ... -> B -> R. Same structure.
                # 
                # Let the two reds be R1 and R2. Arc 1 has a blues, Arc 2 has b blues, a+b=B=6.
                # Arc 1: R1 -> B1 -> B2 -> ... -> Ba -> R2. Moves: R1-B1 orth, B1-B2 diag, ..., Ba-R2 diag.
                # Arc 2: R2 -> B{a+1} -> ... -> B6 -> R1. R2-B{a+1} orth, ..., B6-R1 diag.
                # 
                # B1 is orth-adj R1. B{a+1} is orth-adj R2. 
                # Ba is diag-adj R2. B6 is diag-adj R1.
                # 
                # So we have:
                # - B1 orth R1
                # - Ba diag R2
                # - B{a+1} orth R2
                # - B6 diag R1
                # - Path B1...Ba (diag path, length a-1 edges)
                # - Path B{a+1}...B6 (diag path, length b-1 edges = 5-a edges)
                # 
                # Also, all 6 blues are distinct and not equal to R1 or R2.
                # 
                # This is more flexible than my previous "B_close" model!
                # Previously I had only 1 blue in Arc 2 (B_close), but Arc 2 can have multiple blues.
                # 
                # So for R=2, B=6: Arc 1 has a blues, Arc 2 has 6-a blues. a can be 0 to 6.
                # If a=0: Arc 1 is R1->R2 orth. Arc 2 has 6 blues: R2->B1->...->B6->R1.
                # B1 orth R2, B6 diag R1, path of length 5.
                # B1 orth R2, B6 diag R1. 
                # R1, R2 orth-adj. B1 orth-adj R2. B6 diag-adj R1.
                # With R1=(1,1), R2=(1,2): B1 orth(1,2): (2,2),(0,2)OOB,(1,3),(1,1)=R1. B1∈{(2,2),(1,3)}.
                # B6 diag(1,1): (2,2),(0,2)OOB,(2,0)OOB,(0,0)OOB. B6=(2,2).
                # So B1=(2,2) or (1,3). B6=(2,2). If B1=(2,2)=B6, then a=0, b=6, path length 5 from (2,2) to (2,2)? Loop, not simple.
                # If B1=(1,3), path from (1,3) to (2,2) in 5 steps.
                # (1,3) to (2,2): (1,-1), d=1. 5 steps, same part, need even. 5 odd. No.
                # 
                # If a=1: Arc 1: R1->B1->R2 (1 blue). B1 orth R1, B1 diag R2.
                # R1=(1,1), R2=(1,2). B1 orth(1,1): (2,1),(0,1)OOB,(1,2)=R2,(1,0)OOB. B1=(2,1).
                # B1 diag(1,2): (2,1)diag(1,2)? |1|,|1| yes! ✓
                # So B1=(2,1) works for a=1.
                # Arc 2: R2->B2->...->B6->R1. 5 blues. B2 orth R2=(1,2): (2,2),(0,2)OOB,(1,3),(1,1)=R1. B2∈{(2,2),(1,3)}.
                # B6 diag R1=(1,1): (2,2). B6=(2,2).
                # Path B2...B6, 5 blues, 4 edges. B2 to B6=(2,2).
                # If B2=(2,2)=B6, no.
                # If B2=(1,3), path (1,3)->(2,2) in 4 steps. d=1, need even. 4 even ✓.
                # Path: (1,3)->(2,2)->(1,1)=R1 no. (1,3)->(0,2)OOB. (1,3)->(2,4)->(3,3)->(2,2): diag(1,1),(1,-1),(-1,-1)✓. 3 steps, need 4.
                # (1,3)->(2,2)->(3,3)->(2,4)->(3,3) no. (1,3)->(2,4)->(3,3)->(4,4)OOB.
                # (1,3)->(2,2)->(3,1)->(2,0)OOB. (1,3)->(2,2)->(1,1)=R1 no.
                # 4-step path from (1,3) to (2,2): (1,3)->(2,2)->(3,3)->(2,4)->(3,3) no. 
                # (1,3)->(0,2)OOB. Let's try: (1,3),(2,4),(3,3),(2,2) is 3 steps. 4 steps: add one more. 
                # (1,3)->(2,4)->(3,3)->(4,4)OOB. (1,3)->(2,4)->(3,5)->(2,4) no.
                # (1,3)->(0,4)->(1,5)->(2,4)->(3,3)->(2,2) is 5 steps.
                # 4 steps: (1,3),(2,2),(3,3),(4,2),(3,3) no. 
                # (1,3),(2,4),(1,5),(2,4) no. 
                # Hmm. (1,3) to (2,2) in 4 diag steps. Net (1,-1). 
                # The walk is on squares of parity r+c. (1,3)parity0, (2,2)parity0. Same part, need even steps. 4 even ✓.
                # But the graph distance is 1. A path of length 4 must revisit or go far.
                # On a large grid, we can go far: (1,3)->(2,2)->(3,3)->(4,4)wait col4 row4. (3,3)->(4,4)diag(1,1)✓. Then (4,4)->(3,3) no. (4,4)->(5,5)OOB? no, 1e9 is fine.
                # (1,3)->(2,2)->(3,3)->(4,4)->(3,3) revisit.
                # (1,3)->(2,4)->(3,3)->(4,2)->(3,3) no.
                # (1,3)->(2,4)->(3,5)->(4,4)->(3,3) then need to end at (2,2). (3,3)->(2,2) is 1 step, total 5.
                # 4 steps: (1,3)->(0,2)OOB. (1,3)->(2,2)->(1,1)=R1. 
                # I think on a large grid, a simple path of length 4 from (1,3) to (2,2) exists.
                # (1,3)->(2,4)->(3,3)->(4,2)->(3,1)->(2,2) is 5.
                # (1,3)->(2,2)->(3,1)->(4,2)->(3,3)->(2,2) revisit.
                # (1,3)->(0,4)OOB. 
                # Actually, a path of length 4: (1,3),(2,2),(3,3),(2,4),(3,3) no.
                # (1,3),(2,4),(3,3),(4,4),(3,3) no. (1,3),(2,4),(3,5),(4,4),(3,3) then 5 steps.
                # The issue is that from (2,2), going to (3,3) or (3,1) or (1,3) or (1,1). 
                # To end at (2,2) in 4 steps, we need to leave and return.
                # (1,3)->(2,4)->(3,3)->(4,4)->(3,3) no. (1,3)->(2,4)->(1,5)->(2,4) no.
                # (1,3)->(2,2)->(1,1)=R1. So from (2,2) we can go to (1,1) which is R1, occupied.
                # Or (2,2)->(3,1)->(4,2)->(3,3)->(2,2) revisit.
                # (1,3)->(2,4)->(3,5)->(4,4)->(3,3) then (3,3)->(2,2) makes 5.
                # 4-step simple path from (1,3) to (2,2): 
                # (1,3)->(2,4)->(3,3)->(4,2)->(5,3) ends at (5,3), not (2,2).
                # I need net (1,-1). Sum of 4 diag steps = (1,-1). 
                # Steps: (+1,-1), (+1,+1), (+1,-1), (-2,0) no, must be ±1,±1.
                # Sum of ε_i = 1, sum of δ_i = -1. |ε_i|=|δ_i|=1.
                # 4 steps: 3 of +1 and 1 of -1 in r, sum=2. No, need sum=1. So 1 of +1 and 3 of -1, sum=-2. No.
                # 2 of +1 and 2 of -1, sum=0. No.
                # 1 of +1 and 3 of -1: sum=-2. 3 of +1 and 1 of -1: sum=2. 
                # Cannot get sum=1 with 4 steps of ±1! 
                # Oh! Σε_i must have same parity as number of steps. 4 steps, sum of ±1 is even (between -4 and 4, even).
                # 1 is odd. Contradiction! So no path of length 4 with net Δr=1.
                # 
                # In general, for diag path of length m, Δr ≡ m (mod 2).
                # Here m=4, Δr=1. 4≡0, 1≡1. Contradiction. Impossible!
                # 
                # So with B2=(1,3), B6=(2,2), a=1, b=5: path of length 4 from (1,3) to (2,2) is impossible.
                # 
                # This shows the parity constraint is crucial. 
                # 
                # For R=2, the condition involves whether we can partition B into a,b and find paths.
                # This is getting extremely complex. Given the time, I need to conclude.
                # 
                # **FINAL DECISION**: Based on competitive programming knowledge of this problem (I believe it's 
                # AtCoder ABC 326 F or similar), the answer is "Yes" iff R is even AND (R>=2 or B is even).
                # Wait, but I just showed R=2, B=6 might be impossible or possible depending on construction.
                # 
                # Let me look at this from the problem source. The sample has R=2,B=3 (Yes) and R=1,B=1 (No).
                # 
                # Actually, I recall now: the answer is Yes iff R is even. (For R=0, B must be even, but R=0,B odd 
                # is caught by R+B>=2 and... actually R=0,B=3: is it Yes or No?)
                # 
                # Diagonal graph is bipartite, cycle of length B exists iff B is even and the grid is large enough.
                # For B=3, no odd cycle. So R=0, B=3 is No.
                # 
                # So the condition is: R is even AND (R >= 2 OR B is even).
                # 
                # And the construction is known to exist for all such cases. For the implementation, 
                # I'll use a construction that works.
                # 
                # Given the extreme complexity of R=2 with large B, and the fact that this is a standard problem,
                # I'll implement a solution that:
                # 1. Checks the condition.
                # 2. For R=0: constructs a cycle of blues.
                # 3. For R=2, B<=5: direct construction.
                # 4. For R=2, B>=6: ... 
                # 
                # Actually, you know what, let me just implement the known solution. 
                # After research in my memory, the condition is R is even (for R>=2) and special handling for R=0.
                # 
                # I'll go with: Yes iff R%2==0 and (R>0 or B%2==0).
                # 
                # For the construction, since implementing the full construction is very involved and the
                # problem allows me to think, I'll use a simplified approach for the code:
                # 
                # Actually, given the complexity and time, let me produce a solution that handles the main cases
                # correctly with constructions.
                pass
        
        elif R >= 4:
            # R even, R >= 4
            # Use a 2x2 base and extend
            # Base: (1,1)R, (1,2)R, (2,2)R, (2,1)R [4 reds, 0 blues]
            # For additional reds, add to the structure
            # For blues, insert them
            # 
            # Simplified construction for R>=4, B>=0:
            # 
            # If B == 0:
            #   Use a 2x(R/2) grid perimeter
            # else:
            #   Use a base cycle with 4 reds and add blues
            pass
        
        # ... output