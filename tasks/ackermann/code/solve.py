m, n = map(int, input().split())

def f(x, y):
    if x == 0:
        return y + 1
    if y == 0:
        return f(x - 1, 1)
    return f(x - 1, f(x, y - 1))

print(f(m, n))