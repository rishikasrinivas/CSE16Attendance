class ProcessID:
    # removes noise from ID scan
    def removeBackground(self,file, writeFile):
       with open(file, "r") as f:
           with open(writeFile, "a") as f1:
            for index, line in enumerate(f):
                if index > 0:
                    trunc = str(line)[6:13]
                    f1.write(trunc)

    def compareWithRoster(self,checkedInStudents, classRoster):
        loggedIn = []
        classList = []
        countCheckedIn = 0
        countClass = 0
        absent = []
        with open(checkedInStudents, "r") as f:
            update = f.readlines()
            for i in update:
                if countCheckedIn > 0:
                    loggedIn.append(i.strip())
                countCheckedIn += 1
        with open(classRoster, "r") as f1:
            update = f1.readlines()
            for i in update:
                if countClass > 0:
                    classList.append(i.strip().split(",")[0])
                countClass += 1

        for i in classList:
            if i not in loggedIn:
                absent.append(i)
        return self.getNames(classRoster, absent)

    def getNames(self, file, ids):
        absent = []
        with open(file, "r") as f:
            lines = f.readlines()
            for i in ids:
                for j in lines:
                    if j.strip().split(",")[0] == i:
                        absent.append([j.strip().split(",")[0], j.strip().split(","
                                                                                "")[1], j.strip().split(",")[3]])
        return absent

p = ProcessID()
        #file you scanned barcodes into     file you want to store the ID# (no noise) into
p.removeBackground("AttendanceSheet.txt", "ProcessID.txt")
                                                #main roster
absent = p.compareWithRoster("ProcessID.txt", "mockSheet.txt")
for i in absent:
    print(i)

