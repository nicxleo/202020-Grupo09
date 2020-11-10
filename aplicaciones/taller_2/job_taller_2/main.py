import time
from subprocess import call

print("###################### Start job service #####################")
while True:
    time.sleep(30)
    print("###################### Start process #####################")
    call('python remove_tweet.py', shell=True)
    call('python process.py', shell=True)
    print("###################### Finish process #####################")
