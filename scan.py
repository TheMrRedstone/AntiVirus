import os
import time
import hashlib
import threading
from md5 import scanViruses
from tkinter import messagebox

res = []
dirRes = []
i = 0
totalItems = 0
totalFolders = 0

class Save():
    def __init__(self, itemsLabel, folderLabel, filesList, dirList):
        itemsLabel.config(text=f"Found {totalItems} Items In Your Folder!")
        folderLabel.config(text=f"Found {totalFolders} Folders In Your Folder!")
        for i in range(len(res)):
            filesList.insert(i + 2, res[i])

        for i in range(len(dirRes)):
            dirList.insert(i + 2, dirRes[i])

filesHash = []

class Scan():
    def __init__(self, fileArr, statusLbl, virusLbl, virusList, fileRes, prog, progressLbl, start):
        global i
        for (dir_path, dir_names, file_names) in os.walk("C:\\"):
            dirRes.extend(dir_names)
            res.extend(file_names)
            i += 1
            if os.path.isfile(res[i]):
                print(f"Reading File {len(res)}: {file_names}")
                for x in file_names:
                    print(os.path.join(dir_path, x))
                    file = hashlib.md5(open(f"{os.path.join(dir_path, x)}", "rb").read()).hexdigest()
                    filesHash.append(file)
                    print(filesHash)
            else:
                print(f"Reading Folder {len(res)}: {dir_names}")

        end_time = time.perf_counter()
        messagebox.askokcancel("AntiVirus", f"The Task Has Successfully Finished Reading All Files In {round(end_time - start, 2)} Seconds")

        thread = threading.Thread(target=lambda fileArr = filesHash, statusLbl = statusLbl, virusLbl = virusLbl, virusList = virusList, fileRes = res, prog = prog, progressLbl = progressLbl: scanViruses(fileArr, statusLbl, virusLbl, virusList, fileRes, prog, progressLbl, len(filesHash), start))
        thread.start()