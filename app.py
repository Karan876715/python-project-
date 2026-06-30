from flask import Flask
app = Flask (__name__)

#project data - dictonary
stud = [
   { "name": "karan", "roll_no": 51,"marks":85},
    { "name": "kartik", "roll_no": 42,"marks":75},
    { "name": "kunal", "roll_no": 71,"marks":95},
    { "name": "krushna", "roll_no": 41,"marks":45},
    ]

@app.route('/')
def home():
    #create using html

    html = '<h1>College portal - Students</h1>'
    html += '<ul>'
    for student in stud:
      html += f"<li>{student['name']} - roll_no: {student['roll_no']}, marks: {student['marks']}</li>"
    html += '</ul>'
    return  html

@app.route('/about')
def about():
    return '<h1>About Us</h1><p>This is a college management system.</p>'
@app.route('/students')
def students():
    return '<h1>Students List</h1><p>All students will show here</p>'

if __name__=='__main__':
    app.run(debug=True)
 