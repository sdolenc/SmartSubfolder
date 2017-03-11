
#!/usr/bin/python

import os
import shutil

#todo: take directory as an argument. import getopt or argparse, sys also has argv
directory = "C:\\max\\s.review\\now\\mar05"
backup = directory + '_bak'

# Create Backup.
try:
    shutil.copytree(directory, backup)
except:
    # We don't want to proceed if this fails.
    print('Backup copy failed. Exiting')
    exit()

#todo: if file timestamps are different then create date subdirectories and move files accordingly

#todo: conditionalize this so we only move files when the types are different
for file in os.listdir(directory):
    if file.endswith(".jpg") | file.endswith(".png"):
        try:
            os.makedirs(os.path.join(directory, 'imgs'))
        except:
            pass
        shutil.move(os.path.join(directory, file), os.path.join(directory, 'imgs', file))
    elif file.endswith(".mp4") | file.endswith(".webm") | file.endswith(".mov"):
        try:
            os.makedirs(os.path.join(directory, 'vids'))
        except:
            pass
        shutil.move(os.path.join(directory, file), os.path.join(directory, 'vids', file))

#todo: verify file count and total size equals backup after completion
#       if so, cleanup backup
#       if not, display error message
count = 0
size = 0
for root, dirs, files in os.walk(directory):
    count += len(files)
    for file in files:
        size += os.path.getsize(os.path.join(root, file))
for root, dirs, files in os.walk(directory + '_bak'):
    count -= len(files)
    for file in files:
        size -= os.path.getsize(os.path.join(root, file))
print(count)
print(size)
