import configparser
import mysql.connector
import time

class AttendanceCheck:
    def __init__(self):
        self.lineNum = 1
        self.connection=None

    def connectToDatabase(self):
        self.connection = mysql.connector.connect(
          host= "localhost",
          port=3306,
          user= "root",
          password= "Krishna@2004!",
          database = "Quizzes"
        )
    def closeConnection(self):
        self.connection.close()

    def insertData(self,id,first_name,last_name):
        cursor = self.connection.cursor(buffered=True)
        insert_new_student = ("INSERT IGNORE INTO Attendance (ID, LAST_NAME, FIRST_NAME) VALUES (%s, %s, %s)")
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
            cursor.execute(insert_new_student,(id,last_name,first_name))
            # cursor.execute("DELETE FROM Attendance")
            self.connection.commit()

    def getStudentInfo(self, file):
        with open(file, "r") as f:
            for index, line in enumerate(f):
                if index > 0:
                    lines = line.split(",")
                    self.insertData(lines[0], lines[1],lines[2])

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
            f1.write("ID,LAST_NAME,FIRST_NAME")


    def getLineFromFile(self, file):
        with open(file, 'r') as fp:
        # lines to read
            line_numbers = [1]
            for i, line in enumerate(fp):
            # read line 4 and 7
                if i == self.lineNum:
                    return line

def main():
    file = "AttendanceSheet.dat"
    a = AttendanceCheck()
    interval = 1
    lasttime = time.time()
    count = 0
    empty = 0
    a.connectToDatabase()
    while True:
        #check cur time
        now = time.time()
        if (abs(now - lasttime)) > interval:
            if not a.isEmpty("AttendanceSheet.dat"):
                print("updating database")
                a.getStudentInfo(file)
            else:
                empty += 1
            lasttime = now
        if empty == 5:
            break
    a.closeConnection()
main()
