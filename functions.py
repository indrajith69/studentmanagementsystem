import mysql.connector
from datetime import date


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="studentrecordsystem"
)

mycursor = mydb.cursor()

def formatName(fname, mname, lname):
    return f'{fname} {mname} {lname}'

def formatDob(dob):
    return dob.strftime("%Y-%m-%d")

def getSemester(registerno):
    mycursor.execute(f"SELECT MAX(SEM) FROM RESULTS WHERE REGISTERNO={registerno}")
    return mycursor.fetchone()[0]


def getAllStudents():
    allStudents = []

    mycursor.execute("SELECT * FROM STUDENT")

    for student in mycursor.fetchall():
        allStudents.append({
            'registerno':student[0],
            'name': formatName(student[1],student[2],student[3]),
            'phoneno': student[4],
            'email':student[5],
            'dob': formatDob(student[6]),
            'semester': getSemester(student[0])
        })
    
    return allStudents

def getFilteredStudents(fieldData):
    filteredStudents = filterByAdmissionNumber(fieldData)
    if len(filteredStudents)==0:
        filteredStudents = filterByName(fieldData)
    if len(filteredStudents)==0:
        filteredStudents = filterByPhoneNo(fieldData)
    if len(filteredStudents)==0:
        filteredStudents = filterByEmail(fieldData)
    
    return filteredStudents

def filterByAdmissionNumber(admissionNo):
    filteredStudents = []
    allStudents = getAllStudents()

    try:
        admissionNo = int(admissionNo)
    except:
        return []

    for student in allStudents:
        if student['registerno']==admissionNo:
            filteredStudents.append(student)

    print("search by admission no worked")
    return filteredStudents

def filterByName(name):
    filteredStudents = []
    allStudents = getAllStudents()

    for student in allStudents:
        if student['name'].replace(" ","")==name.replace(" ",""):
            filteredStudents.append(student)

    print("search by name worked")
    return filteredStudents

def filterByPhoneNo(phoneNo):
    filteredStudents = []
    allStudents = getAllStudents()

    for student in allStudents:
        if student['phoneno']==phoneNo:
            filteredStudents.append(student)

    print("search by phone no worked")
    return filteredStudents

def filterByEmail(email):
    filteredStudents = []
    allStudents = getAllStudents()

    for student in allStudents:
        if student['email']==email:
            filteredStudents.append(student)

    print("search by email worked")
    return filteredStudents

def getUserData(registerNo):
    userData = {}

    # Execute queries
    mycursor.execute(f"SELECT * FROM STUDENT WHERE REGISTERNO={registerNo}")
    basicDetails = mycursor.fetchone()

    mycursor.execute(f"SELECT * FROM PERSONALINFO WHERE REGISTERNO={registerNo}")
    personalDetails = mycursor.fetchone()

    mycursor.execute(f"SELECT SEM, CGPA FROM RESULTS WHERE REGISTERNO={registerNo} ORDER BY SEM DESC")
    resultDetails = mycursor.fetchone()

    mycursor.execute(f"SELECT AVG(CGPA) FROM RESULTS WHERE REGISTERNO={registerNo} GROUP BY REGISTERNO")
    cgpa = mycursor.fetchone()

    # Populate userData dictionary
    userData['registerno'] = registerNo
    userData['fname'] = basicDetails[1]
    userData['mname'] = basicDetails[2]
    userData['lname'] = basicDetails[3]
    userData['phoneno'] = basicDetails[4]
    userData['email'] = basicDetails[5]
    userData['dob'] = basicDetails[6]

    userData['address'] = personalDetails[1]
    userData['fathername'] = personalDetails[2]
    userData['fatheroccupation'] = personalDetails[3]
    userData['mothername'] = personalDetails[4]
    userData['motheroccupation'] = personalDetails[5]

    userData['semester'] = resultDetails[0]
    userData['sgpa'] = resultDetails[1]
    #userData['cgpa'] = cgpa[0]
    print(cgpa)

    print(userData)
    return userData
