import time
from subprocess import call

while True:
    time.sleep(30)
    call('python process.py', shell=True)
