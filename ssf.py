
#!/usr/bin/python

import os
import sys
import time
import shutil
import exifread

# take directory as an argument.
# future: use getopt or argparse
if (len(sys.argv) != 2):
    print("Path Expected")
    exit(3)
directory = sys.argv[1] # "C:\\max\\import\\combined"
#todo: verify a) exists b) directory os.path.isdir and c) doesn't end w/ slash

backup = directory + '_bak'
images = [ ".jpg", ".webp", ".png" ]
videos = [ ".mp4", ".webm", ".mov" ]

# CLASSES

class Directories:
    'Tracking potential file moves'

    def __init__(self, basePath):
        self.baseDirectory = basePath
        self.subDirToFiles = dict() # keys: Subdirectory, values: files

    def addFile(self, folder, file):
        # Ensure Folder Exists
        if (self.subDirToFiles.get(folder) == None):
            self.subDirToFiles[folder] = list()

        # Add file
        self.subDirToFiles[folder].append(file)

    def moveFiles(self):
        # Only move files if there are going to be two ore more subdirectories.
        # OR if desired subfolder already exists
        if (len(self.subDirToFiles) > 1) or \
            ((len(self.subDirToFiles) == 1) and list(self.subDirToFiles.keys())[0] in next(os.walk(self.baseDirectory))[1]):
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
        if (fileName.lower().endswith(ext)):
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
    shutil.move(os.path.join(baseDir, fileName), os.path.join(baseDir, subDirectory, fileName))

def getDateFromString(toParse):
    # Normalize and split.
    parts = toParse.replace(':', '').replace("-", '.').replace("_", '.').replace(" ", '.').split(".")
    for p in parts:
        try:
            date = time.strptime(p, "%Y%m%d")
            return date
        except:
            continue
    return None

def getDateFromMetaData(filePath):
    f = open(filePath, 'rb')
    tags = exifread.process_file(f)

    date = None
    if ("EXIF DateTimeOriginal" in tags):
        date = getDateFromString(str(tags["EXIF DateTimeOriginal"]))
    elif ("EXIF DateTimeDigitized" in tags):
        date = getDateFromString(str(tags["EXIF DateTimeDigitized"]))
    return date

def getFormattedDate(fileName, path):
    date = getDateFromString(fileName)

    if (date == None):
        date = getDateFromMetaData(os.path.join(path, fileName))

    if (date != None):
        return time.strftime("%Y%b%d", date)

    return "unknownDate"

def getType(filename, path = ""):
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
        #raise
        pass
    printStatus('post', action)

def moveFilesToSubDirs(getSubFolderFn):
    for newRoot, subDirs, files in os.walk(directory):
        pendingMoves = Directories(newRoot)
        for file in files:
            subDir = getSubFolderFn(file, newRoot)
            # Build record of potential moves
            pendingMoves.addFile(subDir, file)
        # Trigger the file moves.
        pendingMoves.moveFiles()

# EXECUTION

makeBackup()
moveFilesToSubDirs(getFormattedDate)
moveFilesToSubDirs(getType)

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
