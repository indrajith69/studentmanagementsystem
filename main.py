from flask import Flask, render_template, redirect, url_for, request
import functions


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('search.html',allStudents=functions.getAllStudents())


@app.route('/submit', methods=['POST'])
def submit():
    fieldData = request.form.get('searchInput')
    filteredStudents = functions.getFilteredStudents(fieldData)
    return render_template('search.html',allStudents=filteredStudents)

@app.route('/edit_details', methods=['POST'])
def edit_details():
    registerno = request.form.get('registerno')
    print(registerno)
    userdata = functions.getUserData(registerno)
    return render_template('edit.html',userdata=userdata)

@app.route('/update_details', methods=['POST'])
def update_details():
    userData = {}
    #registerno = request.form.get('registerno')
    userData['registerno'] = request.form.get('registerno')
    userData['fname'] = request.form.get('fname')
    #userData['mname'] = request.form.get('')
    userData['lname'] = request.form.get('lname')
    userData['phoneno'] = request.form.get('phoneno')
    userData['email'] = request.form.get('email')
    userData['dob'] = request.form.get('dob')
    userData['age'] = request.form.get('age')

    userData['address'] = request.form.get('address')
    userData['fathername'] = request.form.get('fathername')
    userData['fatheroccupation'] = request.form.get('fatheroccupation')
    userData['mothername'] = request.form.get('mothername')
    userData['motheroccupation'] = request.form.get('motheroccupation')

    userData['semester'] = request.form.get('semester')
    userData['cgpa'] = request.form.get('cgpa')

    functions.UpdateUserData(userData)

    return render_template('details.html',userdata=userData)

@app.route('/result/<int:id>')
def result(id):
    userdata = functions.getUserData(id)
    return render_template('details.html',userdata=userdata)



@app.route('/add_student')
def add_student():
    return render_template('add.html')


@app.route('/add_details', methods=['POST'])
def add_details():
    userData = {}
    #registerno = request.form.get('registerno')
    userData['registerno'] = request.form.get('registerno')
    userData['fname'] = request.form.get('fname')
    #userData['mname'] = request.form.get('')
    userData['lname'] = request.form.get('lname')
    userData['phoneno'] = request.form.get('phoneno')
    userData['email'] = request.form.get('email')
    userData['dob'] = request.form.get('dob')

    userData['address'] = request.form.get('address')
    userData['fathername'] = request.form.get('fathername')
    userData['fatheroccupation'] = request.form.get('fatheroccupation')
    userData['mothername'] = request.form.get('mothername')
    userData['motheroccupation'] = request.form.get('motheroccupation')

    userData['semester'] = request.form.get('semester')
    userData['cgpa'] = request.form.get('cgpa')

    print(userData)
    functions.AddUserData(userData)
    
    return render_template('details.html',userdata=userData)

@app.route('/remove_student', methods=['POST'])
def remove_student():
    registerno = request.form.get('registerno')
    functions.delete(registerno)
    return render_template('search.html',allStudents=functions.getAllStudents())

if __name__ == '__main__':
    app.run(host='192.168.29.60', port=5000, debug=True)
