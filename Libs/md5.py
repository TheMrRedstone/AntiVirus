from tkinter import messagebox
from bs4 import BeautifulSoup
from itertools import islice
import urllib.request
import requests
import math
import time
import os

class scanViruses():
    def __init__(self, file, statusLbl, virusLbl, virusList, fileRes, prog, progressLbl, lengt, start):
        status = False
        virusStatus = "No Virus Found"
        theurl = "https://virusshare.com/hashes"
        thepage = urllib.request.urlopen(theurl)
        self.length = lengt
        self.newI = 0
        arr = []
        # arr.append("b2558655b266018ac338ad37d03fe60f")
        # arr.append("74f2e6adee7ed58c42714838ed356c55")
        soup = BeautifulSoup(thepage)
        for link in soup.findAll('a'):
            if link.string.isnumeric():
                print(link.string)
                self.length = int(link.string)   
        for link in soup.findAll('a'):
            if link.string.isnumeric():
                virus = 0
                print(f"https://virusshare.com//hashfiles/VirusShare_{link.string.zfill(5)}.md5")
                print(int(link.string))
                res = requests.get(f"https://virusshare.com//hashfiles/VirusShare_{link.string.zfill(5)}.md5")
                arr.append(res.content.split(b"\n"))
                for z in range(len(file)):
                    for i in range(len(arr)):
                        prog.config(length=self.length)
                        if self.newI <= i:
                            self.newI = i
                            prog['value'] = i / (self.length / 100)
                            progressLbl.config(text=f"{math.floor(i / (self.length / 100))}%")

                        if file[z] == arr[i]:
                            virusStatus = "Found Virus"
                            virus += 1
                            virusLbl.config(text=f"Viruses Found: {virus}")
                            virusList.delete(i + 2)
                            virusList.insert(i + 2, fileRes[z])
                            if status == False:
                                statusLbl.config(text="Status: Your PC Is Infected!")
                                status = True
                        else:
                            virusStatus = "No Virus Found"
                            if status == False:
                                statusLbl.config(text="Status: Your PC Is Clean!")
                                status = False
        
        end_time = time.perf_counter()
        messagebox.askokcancel("AntiVirus", f"The Task Has Successfully Finished At {round(end_time - start, 2)} Seconds")

# os.remove("md5.txt")