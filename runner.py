import sys
import subprocess

procs = []
for i in range(2):
    proc = subprocess.Popen([sys.executable, 'deepLearn.py', str(i)])
    proc.append(proc)