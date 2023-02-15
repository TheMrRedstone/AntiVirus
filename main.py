# Python Import Modules For Tkinter, and the os
from tkinter import filedialog, messagebox
from bs4 import BeautifulSoup
from systemscan import Scan
from md5 import scanViruses
from tkinter import ttk
from tkinter import *
import urllib.request
import threading
import requests
import hashlib
import json
import math
import time
import os

# Check For Updates
theurl = "https://raw.githubusercontent.com/TheMrRedstone/AntiVirus/main/version.txt"
for line in urllib.request.urlopen(theurl):
    print(line.decode('utf-8').replace("\n", ""))
    if open("User/Updates/version.txt").read() < line.decode("utf-8"):
        print(open("User/Updates/version.txt").read())
        print("Out Of Date Program")
        print("Updating....")

# Main Variables
data = json.load(open('User/Scan Settings/settings.json'))
totalViruses = 0
status = "Not Infected Clean"
totalItems = 0
totalFolders = 0
i = 0
theurl = "https://virusshare.com/hashes"
thepage = urllib.request.urlopen(theurl)
length = 0
download = data['User'][0]['User Settings']['Downloaded Md5']
start_time = time.perf_counter()

if download == True:
    try:
        with open('data/Offline Scan/md5.txt', 'r') as f:
            if "" != open('data/Offline Scan/md5.txt').read():
                pass
            else:
                print("Error Data Might Be Courupted!")
                download = False
                data['User'][0]['User Settings']['Downloaded Md5'] = download
                with open('User/Scan Settings/settings.json', "w") as f:
                    dict = json.dumps(data, indent=4)
                    f.write(dict)
                    f.close()
    except:
        print("Error Data Might Be Courupted!")
        download = False
        data['User'][0]['User Settings']['Downloaded Md5'] = download
        with open('User/Scan Settings/settings.json', "w") as f:
            dict = json.dumps(data, indent=4)
            f.write(dict)
            f.close()

win = Tk()

# Functions
def customScan():
    # global i
    # global length
    # global val
    # os.system(f"start /b cmd /c {os.path.dirname(__file__)}\\md5.py")
    # root = Toplevel()
    # root.title("Downloading MD5...")
    # root.geometry("480x360")
    # root.lift()
    # soup = BeautifulSoup(thepage)
    # for link in soup.findAll('a'):
    #     if link.string.isnumeric():
    #         print(link.string)
    #         length = int(link.string)
    # progress = ttk.Progressbar(root, length=length)
    # progress.pack()
    # val = 0
    # def prog():
    #     progress['value'] += 1
    #     progress.update()
    #     progress.after(1000, prog)
    
    # prog()
    fileLog = filedialog.askdirectory()
    res = []
    dirRes = []
    filesHash = []
    virusList.delete(0, len(res) + 1)
    filesList.delete(0, len(res) + 1)
    dirList.delete(0, len(dirRes) + 1)
    filesList.insert(0, "             Files Found:")
    dirList.insert(0, "             Folders Found:")
    filesList.insert(1, "------------------------------")
    dirList.insert(1, "------------------------------")
    virusList.place(relx=0.5, rely=1, anchor="s")
    virusList.insert(0, "             Viruses Found:")
    virusList.insert(1, "------------------------------")
    for (dir_path, dir_names, file_names) in os.walk(fileLog):
        res.extend(file_names)
        totalItems = len(res)
        dirRes.extend(dir_names)
        totalFolders = len(dirRes)
        for x in file_names:
            print(os.path.join(dir_path, x))
            file = hashlib.md5(open(f"{os.path.join(dir_path, x)}", "rb").read()).hexdigest()
            filesHash.append(file)
            print(filesHash)
        itemsLabel.config(text=f"Found {totalItems} Items In Your Folder!")
        folderLabel.config(text=f"Found {totalFolders} Folders In Your Folder!")
    for i in range(len(res)):
        filesList.insert(i + 2, res[i])

    for i in range(len(dirRes)):
        dirList.insert(i + 2, dirRes[i])

    thread = threading.Thread(target=lambda fileArr = filesHash, statusLbl = statusLabel, virusLbl = virusLabel, virusList = virusList, fileRes = res, prog = scanProgress, progressLbl = progress, start = start_time: scanViruses(fileArr, statusLbl, virusLbl, virusList, fileRes, prog, progressLbl, 0, start))
    thread.start()

def FullScan():
    thread = threading.Thread(target=lambda itemsLabel = itemsLabel, folderLabel = folderLabel, fileArr = filesList, statusLbl = statusLabel, virusLbl = virusLabel, virusList = virusList, prog = scanProgress, progressLbl = progress, start = start_time: Scan(itemsLabel, folderLabel, fileArr, dirList, statusLbl, virusLbl, virusList, prog, progressLbl, start))
    thread.start()

def downloadFile():
    theurl = "https://virusshare.com/hashes"
    thepage = urllib.request.urlopen(theurl)
    soup = BeautifulSoup(thepage)
    arr = []
    i = 0
    if arr == "":
        arr.clear()
    if open('data/Offline Scan/md5.txt'):
        with open('data/Offline Scan/md5.txt', "w") as f:
            f.write("")
    with open('data/Offline Scan/md5.txt', "a") as f:
        global length
        for link in soup.findAll('a'):
            if link.string.isnumeric():
                print(link.string)
                length = int(link.string)   
        for link in soup.findAll('a'):
            if link.string.isnumeric():
                print(f"https://virusshare.com//hashfiles/VirusShare_{link.string.zfill(5)}.md5")
                print(int(link.string))
                res = requests.get(f"https://virusshare.com//hashfiles/VirusShare_{link.string.zfill(5)}.md5")
                arr.append(res.content)
                i += 1
                scanProgress['value'] = i / (length / 100)
                print(f"{math.floor(i / (length / 100))}%")
                progress.config(text=f"{math.floor(i / (length / 100))}%")
        f.write(str(arr))
        # os.system("TASKKILL /IM Python.exe /F")
        closeBox = messagebox.askquestion("Restart Is Required.", "Do You Want To Restart The Application. You Will Not Be Able To Offline Scan Until You Restart The Application")
        if closeBox == 'yes':
            win.destroy()
            os.startfile(__file__)

def downloadMd5():
    warningBox = messagebox.showinfo("WARNING!", "Please Do Not Close The Program While It Is Downloading After It Is Finsihed It Will Prompt You To Restart The App For Changes To Apply.", icon="warning")

    download = True
    data['User'][0]['User Settings']['Downloaded Md5'] = download
    with open('User/Scan Settings/settings.json', "w") as f:
        dict = json.dumps(data, indent=4)
        f.write(dict)
        f.close()
    thread = threading.Thread(target=downloadFile)
    thread.start()

# Main Code Options
style = ttk.Style(win)
win.title("AntiVirus")
win.geometry("720x480")
style.theme_use("winnative")
win.minsize(width=480, height=480)

# Screen Objects
scanFullBtn = Button(master=win, text="Full Scan", command=FullScan)
scanBtn = Button(master=win, text="Fast Scan")
customScanButton = Button(master=win, text="Custom Scan", command=customScan)
if download == False:
    downloadOfflineButton = Button(master=win, text="Download Offline Scan", command=downloadMd5)
else:
    downloadOfflineButton = Button(master=win, text="Run Offline Scan")
virusLabel = Label(master=win, text=f"Viruses Found: {totalViruses}")
statusLabel = Label(master=win, text=f"Status: {status}")
itemsLabel = Label(master=win, text=f"Found {totalItems} Items In Your Folder!")
folderLabel = Label(master=win, text=f"Found {totalFolders} Folders In Your Folder!")
filesList = Listbox(master=win, width=25, height=15)
dirList = Listbox(master=win, width=25, height=15)
virusList = Listbox(master=win, width=25, height=15)
scanProgress = ttk.Progressbar(win)
progress = Label(win, text="0%")

# Placing The Objects Onto The Screen.
scanFullBtn.place(relx=1, rely=0, anchor="ne")
scanBtn.place(relx=1, rely=0.08, anchor="ne")
customScanButton.place(relx=1, rely=0.16, anchor="ne")
# downloadOfflineButton.place(relx=1, rely=0.24, anchor="ne")
virusLabel.place(x=0, y=0)
statusLabel.place(x=0, y=20)
itemsLabel.place(x=0, y=40)
folderLabel.place(x=0, y=60)
filesList.place(relx=0, rely=1, anchor="sw")
dirList.place(relx=1, rely=1, anchor="se")
filesList.insert(0, "             Files Found:")
dirList.insert(0, "             Folders Found:")
filesList.insert(1, "------------------------------")
dirList.insert(1, "------------------------------")
virusList.place(relx=0.5, rely=1, anchor="s")
virusList.insert(0, "             Viruses Found:")
virusList.insert(1, "------------------------------")
scanProgress.place(relx=0.5, rely=0, anchor="n", width=200)
progress.place(relx=0.5, rely=0.04, anchor="n")

def closePython():
    os.abort()

win.protocol("WM_DELETE_WINDOW", closePython)
win.mainloop()