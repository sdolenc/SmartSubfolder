
#!/usr/bin/python

import os
import shutil

#todo: take directory as an argument. import
#   getopt or argparse, sys also has argv
directory = "C:\\max\\import\\combined"

backup = directory + '_bak'
images = [ ".jpg", ".png" ]
videos = [ ".mp4", ".webm", ".mov" ]

# HELPERS

#todo: use for each major stage
def printStatus(step, action):
    strMap = {
        "pre": 'Start: {}...',
        "post": 'Finished: {}!',
        "error": 'Failed: {}. Exiting'
    }
    print(strMap.get(step, step + 'is unknown: {}').format(action))

def hasEnding(fileName, extensions):
    for ext in extensions:
        if (fileName.endswith(ext)):
            return True
    return False

def moveFile(baseDir, subDirectory, fileName):
    # If needed, create directory.
    try:
        os.makedirs(os.path.join(baseDir, subDirectory))
    except:
        pass
    # Move File
    shutil.move(os.path.join(directory, fileName), os.path.join(directory, subDirectory, fileName))

# WORK

def makeBackup():
    action='creating backup'

    printStatus('pre', action)
    try:
        shutil.copytree(directory, backup)
    except:
        printStatus('errors', action)
        # We don't want to proceed if this fails.
        raise
    printStatus('post', action)

#todo: conditionalize this so we only move files when the types are different
def directoryByType():
    for file in os.listdir(directory):
        if hasEnding(file, images):
            moveFile(directory, "imgs", file)
        elif hasEnding(file, videos):
            moveFile(directory, "vids", file)

# EXECUTION

makeBackup()

#todo: if file timestamps are different then create date subdirectories and move files accordingly
#directoryByDate()

directoryByType()

#todo: refactor into functions
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
if (count == 0) and (size == 0):
    #todo: delete backup
    exit()
