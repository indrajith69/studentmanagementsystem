import mysql.connector
from datetime import date,datetime


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="studentrecordsystem"
)

mycursor = mydb.cursor()

def clearCursor():
    try:
        mycursor.fetchall()
    except:
        pass

def formatName(fname, mname, lname):
    return f'{fname} {mname} {lname}'

def formatDob(dob):
    return dob.strftime("%Y-%m-%d")

def getSemester(registerno):
    clearCursor()
    mycursor.execute(f"SELECT MAX(SEM) FROM RESULTS WHERE REGISTERNO={registerno}")
    return mycursor.fetchone()[0]


def getAllStudents():
    allStudents = []
    print('error a')
    clearCursor()

    mycursor.execute("SELECT * FROM STUDENT")

    # Fetch all results before executing another query
    student_records = mycursor.fetchall()
    print('error b')

    for student in student_records:
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


def UpdateUserData(userdata):
    print()
    print(userdata)
    registerno = userdata['registerno']
    fname = userdata['fname']
    lname = userdata['lname']
    #cgpa = userdata['cgpa']
    email = userdata['email']
    phoneno = userdata['phoneno']
    dob = userdata['dob']
    address = userdata['address']
    mothername = userdata['mothername']
    fathername = userdata['fathername']
    motheroccupation = userdata['motheroccupation']
    fatheroccupation = userdata['fatheroccupation']
    #semester = userdata['semester']
    clearCursor()
    

    mycursor.execute(f"update student set fname='{fname}' where registerno={registerno}")
    mycursor.execute(f"update student set lname='{lname}' where registerno={registerno}")
    mycursor.execute(f"update student set phoneno='{phoneno}' where registerno={registerno}")
    mycursor.execute(f"update student set email='{email}' where registerno={registerno}")
    mycursor.execute(f"update student set dob='{dob}' where registerno={registerno}")

    mycursor.execute(f"update personalinfo set address='{address}' where registerno={registerno}")
    mycursor.execute(f"update personalinfo set fathername='{fathername}' where registerno={registerno}")
    mycursor.execute(f"update personalinfo set fatheroccupation='{fatheroccupation}' where registerno={registerno}")
    mycursor.execute(f"update personalinfo set mothername='{mothername}' where registerno={registerno}")
    mycursor.execute(f"update personalinfo set motheroccupation='{motheroccupation}' where registerno={registerno}")
    mydb.commit()
    print('worked?')




def getUserData(registerNo):
    userData = {}
    clearCursor()

    # Execute queries and fetch results
    mycursor.execute(f"SELECT * FROM STUDENT WHERE REGISTERNO={registerNo}")
    basicDetails = mycursor.fetchone()

    mycursor.execute(f"SELECT * FROM PERSONALINFO WHERE REGISTERNO={registerNo}")
    personalDetails = mycursor.fetchone()

    mycursor.execute(f"SELECT SEM, CGPA FROM RESULTS WHERE REGISTERNO={registerNo} ORDER BY SEM DESC")
    resultDetails = mycursor.fetchone()
    clearCursor()

    mycursor.execute(f"SELECT AVG(CGPA) FROM RESULTS WHERE REGISTERNO={registerNo} GROUP BY REGISTERNO")
    cgpa = mycursor.fetchone()

    # Populate userData dictionary if results are found
    if basicDetails:
        userData['registerno'] = registerNo
        userData['fname'] = basicDetails[1]
        userData['mname'] = basicDetails[2]
        userData['lname'] = basicDetails[3]
        userData['phoneno'] = basicDetails[4]
        userData['email'] = basicDetails[5]
        userData['dob'] = basicDetails[6]
        userData['age'] = calculate_age(userData['dob'])

    if personalDetails:
        userData['address'] = personalDetails[1]
        userData['fathername'] = personalDetails[2]
        userData['fatheroccupation'] = personalDetails[3]
        userData['mothername'] = personalDetails[4]
        userData['motheroccupation'] = personalDetails[5]

    if resultDetails:
        userData['semester'] = resultDetails[0]
        userData['sgpa'] = resultDetails[1]

    if cgpa:
        userData['cgpa'] = cgpa[0]

    print(userData)
    return userData


def calculate_age(birthday_str):
    # Convert the birthday string to a datetime object
    #birthday_date = datetime.strptime(birthday_str, '%Y-%m-%d')
    birthday_date = birthday_str
    # Get the current date
    current_date = datetime.now()

    # Calculate the difference between the current date and the birthday
    age = current_date.year - birthday_date.year

    # Adjust age if birthday hasn't occurred yet this year
    if current_date.month < birthday_date.month or \
            (current_date.month == birthday_date.month and current_date.day < birthday_date.day):
        age -= 1

    return age


def AddUserData(userdata):
    print()
    print(userdata)
    registerno = userdata['registerno']
    fname = userdata['fname']
    lname = userdata['lname']
    cgpa = userdata['cgpa']
    email = userdata['email']
    phoneno = userdata['phoneno']
    dob = userdata['dob']
    address = userdata['address']
    mothername = userdata['mothername']
    fathername = userdata['fathername']
    motheroccupation = userdata['motheroccupation']
    fatheroccupation = userdata['fatheroccupation']
    semester = userdata['semester']
    clearCursor()

    mycursor.execute(f"insert into student (registerno,fname,lname,phoneno,email,dob) values('{registerno}','{fname}','{lname}','{phoneno}','{email}','{dob}')")
    mycursor.execute(f"insert into personalinfo values('{registerno}','{address}','{fathername}','{fatheroccupation}','{mothername}','{motheroccupation}')")
    mycursor.execute(f"insert into results(registerno,sem,cgpa) values('{registerno}','{semester}','{cgpa}')")
    mydb.commit()


def delete(registerno):
    clearCursor()
    mycursor.execute(f"delete from student where registerno='{registerno}'")
    mycursor.execute(f"delete from personalinfo where registerno='{registerno}'")
    mycursor.execute(f"delete from results where registerno='{registerno}'")
    mydb.commit()