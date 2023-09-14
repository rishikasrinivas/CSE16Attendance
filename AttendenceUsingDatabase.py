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
        self.roster = []
        self.cols = []

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
    def getRows(self):
        cursor = self.connection.cursor(buffered=True)
        if self.connection.is_connected():
            data = cursor.execute("SELECT * FROM Attendance")
            for row in cursor.description:
                self.cols.append(row[0])
    def insertStudent(self,id):
        cursor = self.connection.cursor(buffered=True)

        #ADD ALL COLUMNS manually
        insert_new_student = "INSERT INTO Attendance (ID, Quiz1) VALUES (%s,%s)"
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
            print(id)
            cursor.execute(insert_new_student, (id, 0))
           
            self.connection.commit()
    def updateData(self,quizNum, id, atten):
        cursor = self.connection.cursor(buffered=True)
        update_data = """UPDATE Attendance SET %s = '%s' WHERE ID = %s""" %(quizNum,atten,id)

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
            cursor.execute(update_data)
            self.connection.commit()

    def clear(self):
        cursor = self.connection.cursor(buffered=True)
        cursor.execute("DELETE FROM Attendance")
        self.connection.commit()

    def getStudentInfo(self, roster_file):
        with open(roster_file, "r") as f:
            for index, line in enumerate(f):
                if index > 0:
                    trunc = str(line)[4:9]
                    if trunc not in self.roster:
                        self.insertStudent(trunc)

                        if roster_file == 'mockSheet.txt':
                            self.roster.append(trunc)

    def getAttendance(self, scanned_file):
        with open(scanned_file, "r") as f:
            for index, line in enumerate(f):
                if index>0:
                    stud_id = str(line)[6:13]
                    print("Stud ", stud_id)
                    #id = self.selectrow(stud_id)
                    self.updateData("Quiz1", stud_id, "p")

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

    def getAbsent(self, quizNum):
        cursor = self.connection.cursor(buffered=True)
        update_data = """SELECT * FROM Attendance WHERE %s = %s""" %(quizNum, 0)
        cursor.execute(update_data)
        for i in cursor.fetchall():
            print(i[0])


    def compareWithRoster(self,checkedInStudents, classRoster):
        loggedIn = []
        classList = []
        countCheckedIn = 0
        countClass = 0
        absent = []
        with open(checkedInStudents, "r") as f:
            update = f.readlines()
            for i in update:
                i = i[6:13]
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
    roster = "mockSheet.txt"
    file = "AttendanceSheet.txt"
    a = AttendanceCheck()
    #while not a.gapBetweenEntries(a.now, a.lasttime):
        #check cur time
    setup = False
    if setup:
        a.getStudentInfo(roster)
    else:
        if not a.isEmpty(file):
            a.now = datetime.now()
            a.lasttime = datetime.now()
            a.connectToDatabase()
            delete = input("Delete entries? Y/N")
            if "y" in delete.lower():
                a.clear()
                return
            a.getRows()
            a.getAttendance(file)
            a.closeConnection()
    a.connectToDatabase()
    a.getAbsent("Quiz1")
    a.closeConnection()
main()
