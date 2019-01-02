import sys
import time
import subprocess as sp

if __name__ == "__main__":
	cmd = "./runBenchmark.sh dm.prop"
	p = sp.Popen(cmd, bufsize=0,stdout=sp.PIPE,universal_newlines=True, shell=True)
	while True:
		l = p.stdout.readline()
		print(l.strip())
		if l == "":
			break
	print("done")
