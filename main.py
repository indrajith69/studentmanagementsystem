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

@app.route('/result/<int:id>')
def result(id):
    functions.getUserData(id)
    return render_template('details.html')

if __name__ == '__main__':
    app.run(host='192.168.1.48', port=5000, debug=True)
