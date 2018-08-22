with open('test.txt', 'r') as f:
	for line in f.readlines():
		print(line.strip())

with open('test.txt', 'w') as f:
	f.write("hello, fileIO")

with open('test.txt', 'a') as f:
	f.write('append')

with open('test.txt', 'r') as f:
	print(f.read())

