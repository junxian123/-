
import time

timeStamp = 1427349630000
timeStamp /= 1000.0

timearr = time.localtime(timeStamp)
otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timearr)
print(otherStyleTime)