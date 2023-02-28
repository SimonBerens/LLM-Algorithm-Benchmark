input()
a = list(map(int, input().split()))


def merge(a1, a2):
    res = []
    i, j = 0, 0
    while i < len(a1) or j < len(a2):
        e1 = a1[i] if i < len(a1) else float("inf")
        e2 = a2[j] if j < len(a2) else float("inf")
        if e1 <= e2:
            res.append(e1)
            i += 1
        else:
            res.append(e2)
            j += 1
    return res


def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    m = len(arr) // 2
    a1, a2 = arr[:m], arr[m:]
    s1, s2 = merge_sort(a1), merge_sort(a2)
    return merge(s1, s2)


print(merge_sort(a))
