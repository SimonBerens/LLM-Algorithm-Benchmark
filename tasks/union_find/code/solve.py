class UnionFind:
    def __init__(self, V):
        self.p = [i for i in range(V)]
        self.sz = [1 for _ in range(V)]

    def root(self, u):
        seen = []
        while self.p[u] != u:
            seen.append(u)
            u = self.p[u]
        for v in seen:
            self.p[v] = u
        return u

    def merge(self, u, v):
        ru, rv, = self.root(u), self.root(v)
        if ru == rv:
            return
        if self.sz[ru] > self.sz[rv]:
            ru, rv = rv, ru
        self.p[ru] = rv
        self.sz[rv] += self.sz[ru]

    def are_connected(self, u, v):
        return self.root(u) == self.root(v)


n, q = map(int, input().split())
uf = UnionFind(n)

res = []
for _ in range(q):
    t, u, v = map(int, input().split())
    if t == 0:
        uf.merge(u, v)
    else:
        res.append(uf.are_connected(u, v))
print(res)
