from typing import List
from array import array

class Solution:
    def longestCommonPrefix(self, words: List[str], k: int) -> List[int]:
        n = len(words)
        if n - 1 < k:
            return [0] * n

        ALPHA = 26
        EMPTY = array('i', [-1]) * ALPHA
        children = EMPTY[:]

        cnt = [0]
        depth = [0]

        path_nodes = []
        path_start = [0] * n
        path_len = [0] * n
        max_len = 0

        for idx, w in enumerate(words):
            path_start[idx] = len(path_nodes)
            path_nodes.append(0)

            node = 0
            lw = len(w)
            if lw > max_len:
                max_len = lw

            for ch in w:
                pos = node * ALPHA + (ord(ch) - 97)
                nxt = children[pos]

                if nxt == -1:
                    nxt = len(cnt)
                    children[pos] = nxt
                    children.extend(EMPTY)
                    cnt.append(0)
                    depth.append(depth[node] + 1)

                node = nxt
                cnt[node] += 1
                path_nodes.append(node)

            path_len[idx] = lw + 1

        max_count = [0] * (max_len + 1)
        count_k = [0] * (max_len + 1)
        last_k = [-1] * (max_len + 1)

        for node in range(1, len(cnt)):
            d = depth[node]
            c = cnt[node]

            if c > max_count[d]:
                max_count[d] = c

            if c == k:
                count_k[d] += 1
                last_k[d] = node

        status = [0] * (max_len + 1)
        except_node = [-1] * (max_len + 1)
        kp1 = k + 1

        for d in range(1, max_len + 1):
            if max_count[d] >= kp1 or count_k[d] >= 2:
                status[d] = 1
            elif count_k[d] == 1:
                status[d] = 2
                except_node[d] = last_k[d]

        del children, cnt, depth, max_count, count_k, last_k, words

        ans = [0] * n
        st_arr = status
        ex_arr = except_node
        ml = max_len
        pn = path_nodes
        ps = path_start
        pl = path_len

        for i in range(n):
            lo = 0
            hi = ml
            start = ps[i]
            plen = pl[i]

            while lo < hi:
                mid = (lo + hi + 1) // 2
                st = st_arr[mid]

                if st == 0:
                    hi = mid - 1
                elif st == 1:
                    lo = mid
                else:
                    if plen <= mid or pn[start + mid] != ex_arr[mid]:
                        lo = mid
                    else:
                        hi = mid - 1

            ans[i] = lo

        return ans