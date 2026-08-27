_OFF = [0] * 10
_off = 0
for _d in range(1, 10):
    _OFF[_d] = _off
    _off += _d
_TOTAL = _off

_TRANS = []
_ADD = []
for _x in range(10):
    _t = []
    for _d in range(1, 10):
        _base = _OFF[_d]
        for _r in range(_d):
            _t.append((_base + _r, _base + ((_r * 10 + _x) % _d)))
    _TRANS.append(_t)
    _ADD.append(tuple(_OFF[_d] + (_x % _d) for _d in range(1, 10)))


class Solution:
    def countSubstrings(self, s: str) -> int:
        cnt = [0] * _TOTAL
        ans = 0

        trans = _TRANS
        add = _ADD
        off = _OFF
        total = _TOTAL

        for ch in s:
            x = ord(ch) - 48
            new = [0] * total

            for idx in add[x]:
                new[idx] = 1

            for src, dst in trans[x]:
                new[dst] += cnt[src]

            cnt = new

            if x:
                ans += cnt[off[x]]

        return ans