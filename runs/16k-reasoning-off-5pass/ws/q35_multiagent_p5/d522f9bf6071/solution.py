class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        indexed_intervals = [(l, r, w, i) for i, (l, r, w) in enumerate(intervals)]
        indexed_intervals.sort(key=lambda x: (x[1], x[0], x[3]))
        
        right_endpoints = sorted(set(x[1] for x in indexed_intervals))
        comp_map = {val: idx + 1 for idx, val in enumerate(right_endpoints)}
        m = len(right_endpoints)
        
        import bisect
        
        class BIT:
            def __init__(self, size):
                self.n = size
                self.tree = [None] * (self.n + 1)
                
            def update(self, i, weight, path):
                while i <= self.n:
                    if self.tree[i] is None:
                        self.tree[i] = (weight, path)
                    else:
                        curr_w, curr_path = self.tree[i]
                        if weight > curr_w or (weight == curr_w and path < curr_path):
                            self.tree[i] = (weight, path)
                    i += i & (-i)
                    
            def query(self, i):
                res = None
                while i > 0:
                    if self.tree[i] is not None:
                        if res is None:
                            res = self.tree[i]
                        else:
                            curr_w, curr_path = self.tree[i]
                            res_w, res_path = res
                            if curr_w > res_w or (curr_w == res_w and curr_path < res_path):
                                res = self.tree[i]
                    i -= i & (-i)
                return res
        
        bits = [BIT(m) for _ in range(4)]
        
        for l, r, w, idx in indexed_intervals:
            comp_r = comp_map[r]
            pos = bisect.bisect_left(right_endpoints, l)
            
            updates = []
            
            w0, p0 = 0, []
            w1_new = w0 + w
            p1_new = p0 + [idx]
            updates.append((1, w1_new, p1_new))
            
            res1 = bits[0].query(pos)
            if res1 is not None:
                w1, p1 = res1
                w2_new = w1 + w
                p2_new = p1 + [idx]
                updates.append((2, w2_new, p2_new))
                
            res2 = bits[1].query(pos)
            if res2 is not None:
                w2, p2 = res2
                w3_new = w2 + w
                p3_new = p2 + [idx]
                updates.append((3, w3_new, p3_new))
                
            res3 = bits[2].query(pos)
            if res3 is not None:
                w3, p3 = res3
                w4_new = w3 + w
                p4_new = p3 + [idx]
                updates.append((4, w4_new, p4_new))
                
            for k, weight, path in updates:
                bit_idx = k - 1
                bits[bit_idx].update(comp_r, weight, path)
                
        best_weight = -1
        best_path = []
        
        for i in range(4):
            res = bits[i].query(m)
            if res is not None:
                w, p = res
                if w > best_weight:
                    best_weight = w
                    best_path = p
                elif w == best_weight:
                    if p < best_path:
                        best_path = p
                        
        return best_path