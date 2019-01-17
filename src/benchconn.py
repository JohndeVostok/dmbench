import subprocess as sp

if __name__ == "__main__":
    cmd = "./runBenchmark.sh dm.prop"
    p = sp.Popen(cmd, bufsize=0, stdout=sp.PIPE, universal_newlines=True, shell=True)
    while True:
        l = p.stdout.readline()
        if (l != ""):
            print(l.strip())
        if l == "done":
            break
