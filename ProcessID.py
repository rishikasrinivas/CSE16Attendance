class ProcessID:
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
                    classList.append(i.strip().split(",")[2])
                countClass += 1

        for i in classList:
            if i not in loggedIn:
                absent.append(i)
        return absent
p = ProcessID()
p.removeBackground("AttendanceSheet.txt", "ProcessID.txt")
absent = p.compareWithRoster("ProcessID.txt", "AttendanceSheet.txt")

