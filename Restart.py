from subprocess import Popen
import sys
import time
import os

#os.system('rclone mount GoogleDrive: ~/"Google Drive"/')

#filename = sys.argv[1]
filename = 'ScryBe.py'
directory = '/home/pi/Documents/ScryBe/'
while True:
    print("\nStarting " + filename)
    p = Popen("python3 " + filename, shell=True)
    p.wait()
    time.sleep(30)