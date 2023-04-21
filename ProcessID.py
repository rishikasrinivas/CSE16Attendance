class ProcessID:
    def removeBackground(self,file, writeFile):
       with open(file, "r") as f:
           with open(writeFile, "a") as f1:
            for index, line in enumerate(f):
                if index > 0:
                    trunc = str(line)[6:13]
                    f1.write(trunc)
p = ProcessID()
p.removeBackground("AttendanceSheet.txt", "ProcessID.txt")
