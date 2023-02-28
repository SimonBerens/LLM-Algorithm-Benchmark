V = int(input())

for u in range(V):
    E = int(input())
    if E:
        l = list(map(int, input().split()))
        assert len(l) == E
        for v in l:
            assert 0 <= v < V
