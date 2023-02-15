import os
import scan
import threading
res = []
dirRes = []
i = 0

def init(i):
    return i

class Scan():
    def __init__(self, itemsLabel, folderLabel, filesList, dirList, statusLabel, virusLabel, virusList, scanProgress, progress, start):
        thread = threading.Thread(target=lambda fileArr = filesList, statusLbl = statusLabel, virusLbl = virusLabel, virusList = virusList, fileRes = res, prog = scanProgress, progressLbl = progress: scan.Scan(fileArr, statusLbl, virusLbl, virusList, fileRes, prog, progressLbl, start))
        thread.start()