import os
from datetime import datetime
print(os.stat("../../test/test_metadata/good.pdf"))
import tinfo as tinfo

from setctime import setctime

# setctime("good.pdf", 375285863)

os.utime("../../test/test_metadata/good.pdf", (1479823463, 1479823463))


# atime must be a datetime
filename = "../../test/test_metadata/good.pdf"
stat = os.stat(filename)
# times must have two floats (unix timestamps): (atime, mtime)
atime = datetime(1970, 1, 1, 0, 0, 0)
os.utime(filename, times=(1479823463, stat.st_mtime))

import os, sys

# Showing stat information of file
stinfo = os.stat(filename)
print(stinfo)

# Using os.stat to recieve atime and mtime of file
print ("access time of a2.py: " ,stinfo.st_atime)
print ("modified time of a2.py: " ,stinfo.st_mtime)

# Modifying atime and mtime
os.utime(filename,(1330712280, 1330712292))
print ("done!!")

print(os.stat(filename))