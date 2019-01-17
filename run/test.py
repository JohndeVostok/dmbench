import sys
import time
import subprocess as sp


def test():
	cmd = "./runBenchmark.sh dm.prop"
	p = sp.Popen(cmd, bufsize=0, stdout=sp.PIPE, stderr=sp.STDOUT, universal_newlines=True, shell=True)
	returncode = p.poll()
	while returncode is None:
		print(p.stdout.readline().strip())
		returncode = p.poll()
		print("fuck")
	print("???")
	print(p.stdout.read())
	print(returncode)

if __name__ == "__main__":
	test()
