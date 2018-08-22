import pickle
d = dict(name = 'Bob', age = 10, score = 99)
with open('dump_test.txt', 'wb') as f:
	pickle.dump(d, f)

f = open('dump_test.txt', 'rb')
print(f.read())
f.close()

f = open('dump_test.txt', 'rb')
d = pickle.load(f)
f.close()
print(d)