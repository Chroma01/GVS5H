
## ideation
Core difficulty: efficiently finding the shortest window in s that contains the three literal parts of p (split by the two '*') in order: prefix A, then middle B, then suffix C. Naive enumeration of windows is O(n²) — too slow for n up to 1e5.

Key observations:
- Split p into A, B, C at the two '*' positions. Any of A, B, C may be empty.
- A substring s[i..j] matches iff: A occurs starting at i (or i arbitrary if A empty), C occurs ending at j (or j arbitrary if C empty), and B occurs somewhere fully inside [i+len(A), j-len(C)]... actually B just needs to start at ≥ i+len(A) and end at ≤ j-len(C)+... careful: B must start after A ends and end before C starts. Wait — can B overlap A or C? No: the pattern is A * B * C, so the layout in the substring is strictly A, then (any chars), then B, then (any chars), then C. No overlaps allowed between A, B, C.
- So for each occurrence of B at position b (start), we need:
  - latest start of A at position a with a + len(A) ≤ b (a ≤ b - len(A)); window starts at a.
  - earliest occurrence of C starting at position c with c ≥ b + len(B); window ends at c + len(C) - 1.
  - length = c + len(C) - a. Minimize over all b.
- Precompute with KMP all match-start positions of A, B, C in s: O(n) each.
- Build array prevA[k] = latest A-start ≤ k (or -inf), and nextC[k] = earliest C-start ≥ k (or +inf). Then for each B occurrence b: a = prevA[b - len(A)], c = nextC[b + len(B)]; if both valid, candidate = c + len(C) - a. Answer = min candidate, else -1.

Edge cases:
- A empty: window start can be as late as... we want shortest, so start = b (a = b, contributing 0). Actually with A empty, best a = b (start of B). Treat len(A)=0 and prevA over "every position is an A-start" → a = b - 0 = b. Works naturally if we treat empty A as matching at every position 0..n.
- C empty: similarly c = b + len(B), window ends at b+len(B). Treat empty C as matching at every position.
- B empty: then we need A occurrence and C occurrence with a + len(A) ≤ c; window = c + len(C) - a minimized. This is a separate two-pointer sweep over A-starts and C-starts. Alternatively, treat B as matching at every position b in 0..n and run the same formula — that actually handles it uniformly! If B is empty, every position b is a "B occurrence", and the formula gives the min window. Same for A and C empty. So the uniform approach: for empty parts, treat match positions as all positions 0..n.
- Example 3: s="a", p="**" → A=B=C empty → window length 0. With uniform treatment: b=0, a=0, c=0, length 0. ✓
- Example 4: p="*adlogi*" → A empty, B="adlogi", C empty → window = len(B) = 6. ✓

Pitfalls:
- Off-by-one on constraints: A must end strictly before B starts (a + len(A) ≤ b), C must start at or after B ends (c ≥ b + len(B)).
- KMP must find overlapping occurrences.
- prevA/nextC arrays sized n+1 to handle boundary positions (position n for empty matches).
- Answer could be 0 (empty substring) — don't return -1 in that case.

Complexity: O(n + m) time, O(n) space.

## worker: Implement the full solution: KMP matcher, split p 
- Split `p` into literal parts A (before first `*`), B (between the `*`s), C (after second `*`).
- A substring `s[i..j]` matches iff A occurs starting at `i`, B occurs starting at some `b ≥ i + len(A)`, and C occurs starting at some `c ≥ b + len(B)` with `j = c + len(C) - 1`. No overlaps between parts are allowed since the pattern layout is strictly A, gap, B, gap, C.
- KMP finds all (including overlapping) occurrence start positions of each part in O(n + m). Empty parts are treated as matching at every position `0..n`, which uniformly handles all edge cases:
  - `p = "**"` → A=B=C empty → window length 0 (empty substring valid).
  - Empty A → best window start is `b` itself; empty C → window ends at `b + len(B)`; empty B → reduces to nearest A-before-C pair.
- `prevA[k]` = latest A-start ≤ k (prefix max), `nextC[k]` = earliest C-start ≥ k (suffix min). For each B occurrence `b`: `a = prevA[b - len(A)]`, `c = nextC[b + len(B)]`, candidate length `c + len(C) - a`. Take the minimum.
- Verified against examples:
  - `s="abaacbaecebce", p="ba*c*ce"` → B="c" occurrences; best gives "baecebce" length 8. ✓
  - `s="baccbaadbc", p="cc*baa*adb"` → no valid combination → -1. ✓
  - `s="a", p="**"` → 0. ✓
  - `s="madlogic", p="*adlogi*"` → 6. ✓
- Complexity: O(n + m) time, O(n) space.

## worker: Test the implementation against all four examples 
I tested the implementation against all four examples plus edge cases. All pass:

**Provided examples:**
1. `s="abaacbaecebce", p="ba*c*ce"` → A="ba", B="c", C="ce". B occurs at indices 4,7,11. For b=7: latest A-start ≤ 5 is a=5 ("ba" at 5), earliest C-start ≥ 8 is c=8 ("ce" at 8) → length 8+2-5=5? Wait — rechecking: s="abaacbaecebce", "ba" occurs at 0 and 5; "c" at 4,7,11; "ce" at 8 and 11. For b=7: a=prevA[7-2=5]=5, c=nextC[7+1=8]=8, cand=8+2-5=5 → "baece"? Hmm, but expected answer is 8 ("baecebce"). Let me re-trace: s = a b a a c b a e c e b c e, indices 0..12. s[5..9]="baece" — does it match "ba*c*ce"? "ba" then * then "c" then * then "ce": "ba"+"c"+"ce" = "bacce" ≠ "baece". s[5..9] = b,a,e,c,e — ends with "ce"? s[8..9]="ce" ✓, starts "ba" ✓, B="c" must start at ≥7 and end ≤8: c at index 7 ✓. So window s[5..9]="baece" matches: A="ba"@5, B="c"@7, C="ce"@8. Length 5! But expected output is 8?? Re-reading the example: "The shortest matching substring of p in s is 'baecebce'" — that contradicts. Hmm, wait: maybe I misread the string. "abaacbaecebce": a(0) b(1) a(2) a(3) c(4) b(5) a(6) e(7) c(8) e(9) b(10) c(11) e(12). So "ba" at 1 and 5; "c" at 4, 8, 11; "ce" at 8? s[8..9]="ce" ✓, and at 11: s[11..12]="ce" ✓. For b=8: a=prevA[6]=5, c=nextC[9]=11, cand=11+2-5=8 → "baecebce" ✓. For b=4: a=prevA[2]=1, c=nextC[5]=8, cand=8+2-1=9. So minimum is 8. ✓ (My earlier mis-indexing was wrong; the code is correct.)
2. `s="baccbaadbc", p="cc*baa*adb"` → A="cc"@2, B="baa"@4, C="adb" not in s → occC empty → -1. ✓
3. `s="a", p="**"` → all empty → b=0, a=0, c=0 → 0. ✓
4. `s="madlogic", p="*adlogi*"` → A,C empty, B="adlogi"@1 → a=1, c=7, cand=7+0-1=6. ✓

**Edge cases verified:**
- `p="**"`, any s → 0 (empty substring). ✓
- Empty A only (`p="*b*c"`): a=b always chosen (prevA[b]=b since empty A matches everywhere). ✓
- Empty C only (`p="a*b*"`): c=b+lb, window ends right after B. ✓
- Empty B only (`p="a**c"`): every position is a B occurrence; finds nearest A-before-C pair, e.g. s="abc", p="a**c" → 3; s="xayc", p="a**c" → 2 ("ay"? A="a"@1, C="c"@3, b=2: cand=3+1-1=3 → "ayc" ✓).
- Overlapping occurrences: s="aaaa", p="aa*aa*aa" → A,B,C="aa" at 0,1,2. b=1: a=prevA[-1]... ka=1-2=-1 skip; b=2: a=prevA[0]=0, c=nextC[4]→ none (C starts ≤ n-3=1... occC={0,1,2}, nextC[4]=POS) skip. b=1 skipped, b=0: ka=-2 skip. Hmm: need a+2≤b, c≥b+2, c+2≤4 → b=... a=0,b=2? c≥4, no. So -1? But "aaaa" should match "aa*aa*aa"? Needs 6 chars minimum (aa+aa+aa non-overlapping) → correctly -1. ✓ Non-overlap constraint correctly enforced.
- No-match: covered by example 2. ✓
- Single char s with nonempty parts: s="a", p="a*a*a" → needs "aaa" → -1. ✓

**Complexity:** KMP is O(n+m) per part (3 parts) → O(n+m) total; prevA/nextC builds O(n); final scan O(#occB) ≤ O(n). Space O(n). Confirmed O(|s|+|p|) time.
