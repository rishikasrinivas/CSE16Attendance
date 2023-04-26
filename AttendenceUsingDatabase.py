# Uses a database to store scanned ID's
import mysql.connector
import time
from datetime import datetime
class AttendanceCheck:
    def __init__(self):
        self.lineNum = 1
        self.connection=None
        self.keepRunning = True
        self.lasttime = datetime.now()
        self.now = datetime.now()

    def connectToDatabase(self):
        self.connection = mysql.connector.connect(
          host= "localhost",
          port=3306,
          user= "root",
          password= "yourpasswd",
          database = "Quizzes"
        )
    def closeConnection(self):
        self.connection.close()

    def insertData(self,id):
        cursor = self.connection.cursor(buffered=True)
        insert_new_student = ("INSERT IGNORE INTO Attendance (ID) VALUES (%s)")
        if self.connection.is_connected():
            db_Info =  self.connection.get_server_info()
            print("Connected to MySQL database... MySQL Server version on ", db_Info)

            # global connection timeout arguments
            global_connect_timeout = 'SET GLOBAL connect_timeout=180'
            global_wait_timeout = 'SET GLOBAL connect_timeout=180'
            global_interactive_timeout = 'SET GLOBAL connect_timeout=180'

            cursor.execute(global_connect_timeout)
            cursor.execute(global_wait_timeout)
            cursor.execute(global_interactive_timeout)
            cursor.execute(insert_new_student,(id,))
            #cursor.execute("DELETE FROM Attendance")
            self.connection.commit()

    def getStudentInfo(self, file):
        with open(file, "r") as f:
            for index, line in enumerate(f):
                if index > 0:
                    trunc = str(line)[6:13]
                    self.insertData(trunc)

        self.clearFile(file)

    def isEmpty(self,file):
        with open(file, "r") as f:
            read = f.readlines()
            if len(read) == 1:
                return True
            return False

    def clearFile(self,file):
        with open(file, 'r+') as f:
            f.seek(1)
            f.truncate()
        with open(file, "w") as f1:
            f1.write("ID")


    def getLineFromFile(self, file):
        with open(file, 'r') as fp:
        # lines to read
            line_numbers = [1]
            for i, line in enumerate(fp):
            # read line 4 and 7
                if i == self.lineNum:
                    return line

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

    def gapBetweenEntries(self, curTime, lastTime):
        if (abs(curTime -lastTime)).total_seconds() > 60:
            return True
        return False
def main():
    file = "AttendanceSheet.txt"
    a = AttendanceCheck()
    while not a.gapBetweenEntries(a.now, a.lasttime):
        #check cur time
        if not a.isEmpty(file):
            a.now = datetime.now()
            a.lasttime = datetime.now()
            a.connectToDatabase()
            a.getStudentInfo(file)
            a.closeConnection()
        else:
            a.now = datetime.now()
        time.sleep(180)
    list_of_now_show = a.compareWithRoster('ProcessID.txt', 'mockSheet.txt')
    print(list_of_now_show)
main()
