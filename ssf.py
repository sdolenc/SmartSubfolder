
#!/usr/bin/python

import os
import sys
import time
import shutil

# take directory as an argument.
# future: use getopt or argparse
if (len(sys.argv) != 2):
    exit(3)
directory = sys.argv[1] # "C:\\max\\import\\combined"
#todo: verify a) exists b) directory and c) doesn't end w/ slash

backup = directory + '_bak'
images = [ ".jpg", ".png" ]
videos = [ ".mp4", ".webm", ".mov" ]

# CLASSES

class Directories:
    'Tracking potential file moves'
    baseDirectory = ''
    subDirToFiles = dict() # keys: Subdirectory, values: files

    def __init__(self, basePath):
        self.baseDirectory = basePath

    def addFile(self, folder, file):
        # Ensure Folder Exists
        if (self.subDirToFiles.get(folder) == None):
            self.subDirToFiles[folder] = list()

        # Add file
        self.subDirToFiles[folder].append(file)

    def moveFiles(self):
        # Only move files if there are going to be two ore more subdirectories
        if (len(self.subDirToFiles) > 1):
            # iterate over dictionary. key=subFolder, value=files
            for subFolder, files in self.subDirToFiles.items():
                # iterate over file list.
                for file in files:
                    moveFile(self.baseDirectory, subFolder, file)

# HELPERS

#todo: use for each major stage
def printStatus(step, action):
    strMap = {
        "pre": 'Start: {}...',
        "post": 'Finished: {}!',
        "error": 'Failed: {}. Exiting'
    }
    print(strMap.get(step, step + ' is not a member of printStatus. Encountered during: {}').format(action))

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
        #raise
        pass
    # Move File
    shutil.move(os.path.join(directory, fileName), os.path.join(directory, subDirectory, fileName))

def getDate(fileName):
    parts = fileName.replace("-", '.').replace("_", '.').replace(" ", '.').split(".")
    for p in parts:
        try:
            date = time.strptime(p, "%Y%m%d")
        except:
            continue
        formatted = time.strftime("%Y%b%d", date)
        return formatted
    # todo: get "date taken" from file meta data
    return "unknownDate"

def getType(filename):
    if hasEnding(filename, images):
        return "imgs"
    elif hasEnding(filename, videos):
        return "vids"
    else:
        return "unknownType"

# WORK

def makeBackup():
    action='creating backup'

    printStatus('pre', action)
    try:
        shutil.copytree(directory, backup)
    except:
        printStatus('error', action)
        # We don't want to proceed if this fails.
        #raise
        pass
    printStatus('post', action)

# todo: conditionalize when the dates are different, recurse to subdirs
def directoryByDate():
    pendingDateMoves = Directories(directory)
    for file in os.listdir(directory):
        #todo: can python take a functionName as a param? if os, we can consolidate these functions.
        date = getDate(file)
        pendingDateMoves.addFile(date, file)
    pendingDateMoves.moveFiles()

#todo: conditionalize when the types are different, recurse to subdirs
def directoryByType():
    pendingTypeMoves = Directories(directory)
    for file in os.listdir(directory):
        #todo: can python take a functionName as a param? if os, we can consolidate these functions.
        fileType = getType(file)
        pendingTypeMoves.addFile(fileType, file)
    pendingTypeMoves.moveFiles()

# EXECUTION

makeBackup()

#directoryByDate()

for newRoot, subDirs, files in os.walk(directory):
    print(newRoot)
    print(files)
    print()

#todo: reactivate after above todos
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
