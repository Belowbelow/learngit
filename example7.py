
# (b=a) != (b=a[:])
a = [1, 2, 3]
b = a
c = a[:]
print("a:", a)
print("b:", b)
print("c:", c)
a.append(4)
print("a:", a)
print("b:", b)
print("c:", c)