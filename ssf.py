
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

#todo:init,adds
#todo:drain
class Directories:
    'Base Directory and collection of pending subfolders'
    baseDirectory = ''
    subFolders = dict() # Subdirectory object

    def __init__(self, basePath):
        self.baseDirectory = basePath

    def addFile(self, folder, file):
        # Ensure Folder Exists
        if (self.subFolders.get(folder) == None):
            subDir = Subdirectory(folder, file)
            self.subFolders[folder] = subDir
        else:
            # Add file
            self.subFolders[folder].files.append(file)

    def moveFiles(self):
        #print(self.subFolders["imgs"].files)
        #print(self.subFolders["vids"].files)
        print(self.subFolders)
        for a in self.subFolders:
            print(a)
            print()
        print(self.subFolders.items())
        for b in self.subFolders.items():
            print(b)
            print()
        exit()
        print(self.subFolders.values)
        if (len(self.subFolders) > 1):
            for sf, value in self.subFolders.items():
                print(str(sf))
                for f in sf.files:
                    moveFile(self.baseDirectory, sf.folderName, f)

#todo: consider making class act like a dictionary
class Subdirectory:
    'Folder and list of pending files'
    folderName = ''
    files = [] # fileName strings

    def __init__(self, folder, file):
        #self.folderName = folder
        self.files.append(file)

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

def getDate(fileName):
    parts = fileName.replace("-", '.').replace("_", '.').replace(" ", '.').split(".")
    for p in parts:
        try:
            date = time.strptime(p, "%Y%m%d")
        except:
            continue
        formatted = time.strftime("%Y%b%d", date)
        return formatted
    # todo: try "date taken" from media file meta data
    return ""

# WORK

def makeBackup():
    action='creating backup'

    printStatus('pre', action)
    try:
        shutil.copytree(directory, backup)
    except:
        printStatus('errors', action)
        # We don't want to proceed if this fails.
        #raise
        pass
    printStatus('post', action)

# todo: conditionalize when the dates are different, recurse to subdirs
def directoryByDate():
    for file in os.listdir(directory):
        date = getDate(file)
        if (date != ""):
            moveFile(directory, date, file)

#todo: conditionalize when the types are different, recurse to subdirs
def directoryByType():
    pendingMoves = Directories(directory)
    for file in os.listdir(directory):
        #todo: can this return subfolders? if so, conditionalize to files
        if hasEnding(file, images):
            #moveFile(directory, "imgs", file)
            pendingMoves.addFile("imgs", file)
        elif hasEnding(file, videos):
            #moveFile(directory, "vids", file)
            pendingMoves.addFile("vids", file)
    pendingMoves.moveFiles()

# EXECUTION

makeBackup()

#directoryByDate()

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
