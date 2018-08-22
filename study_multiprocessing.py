import os

print("Process (%d) start..." % os.getpid())
pid = os.fork()

if pid == 0:
	print("Child Process {0}, Parent Process is {1}".format(os.getpid(), os.getpid()))
else:
	print("Create Child Process {}".format(pid))