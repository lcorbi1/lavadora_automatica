import time

end_time = time.time() + 10
countTimer = 0
sleepTime = 0.500
while time.time() < end_time:
    time.sleep(sleepTime)
    countTimer += sleepTime
    print('hello, ja passaram {} secs'.format(countTimer))