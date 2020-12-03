import time
from subprocess import call

print("###################### Start job service #####################")
while True:
    time.sleep(30)
    call('python remove_tweet.py', shell=True)
    call('python process.py', shell=True)
