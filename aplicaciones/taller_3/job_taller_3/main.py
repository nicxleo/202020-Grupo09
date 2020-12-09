import time
from subprocess import call

print("###################### Start job service #####################")
while True:
    time.sleep(60)
    call('python process.py', shell=True)
    call('python extraction.py', shell=True)
