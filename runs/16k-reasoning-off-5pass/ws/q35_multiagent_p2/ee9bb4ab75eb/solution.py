class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        # If removing any word leaves fewer than k words, answer is 0
        if n <= k:
            return [0] * n
        
        # Precompute prefix counts
        prefix_count = {}
        # Also store which prefixes each word has for quick lookup
        word_prefixes = []
        
        for word in words:
            prefixes = set()
            # Generate all prefixes for the word
            # To avoid storing too many, we can store them in a set for this word
            # But we need to add to global prefix_count
            # Since sum of lengths <= 10^5, we can iterate
            for j in range(1, len(word) + 1):
                p = word[:j]
                prefixes.add(p)
                prefix_count[p] = prefix_count.get(p, 0) + 1
            word_prefixes.append(prefixes)
        
        # Create list of all unique prefixes with their counts
        # We only care about prefixes that have count >= k or count >= k+1
        # Store as (length, count, prefix)
        all_prefixes = []
        for p, cnt in prefix_count.items():
            all_prefixes.append((len(p), cnt, p))
        
        # Sort by length descending
        all_prefixes.sort(key=lambda x: x[0], reverse=True)
        
        # Get top 2 prefixes for count >= k
        top_k = []
        for length, cnt, p in all_prefixes:
            if cnt >= k:
                top_k.append((length, cnt, p))
                if len(top_k) == 2:
                    break
        
        # Get top 2 prefixes for count >= k+1
        top_k1 = []
        for length, cnt, p in all_prefixes:
            if cnt >= k + 1:
                top_k1.append((length, cnt, p))
                if len(top_k1) == 2:
                    break
        
        # Precompute sets for top_k and top_k1 for quick lookup
        top_k_set = set(p for _, _, p in top_k)
        top_k1_set = set(p for _, _, p in top_k1)
        
        # For each word, compute the answer
        ans = []
        for i in range(n):
            # If the word itself is not in the top lists, we need to check
            # A = max length among prefixes of words[i] that are in top_k1
            A = 0
            for p in word_prefixes[i]:
                if p in top_k1_set:
                    # We need the length, so we should store it
                    # Actually, we can get it from the prefix itself
                    if len(p) > A:
                        A = len(p)
            
            # B = max length among top_k prefixes that are NOT in word_prefixes[i]
            B = 0
            for length, cnt, p in top_k:
                if p not in word_prefixes[i]:
                    if length > B:
                        B = length
            
            ans.append(max(A, B))
        
        return ans