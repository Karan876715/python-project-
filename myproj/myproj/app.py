from flask import Flask, render_template
app = Flask(__name__)

students = [
    {"name": "karan", "roll": 1, "marks": 85},
    {"name": "abhay", "roll": 2, "marks": 90},
    {"name": "rudra", "roll": 3, "marks": 82},
    {"name": "naman", "roll": 4, "marks": 88}
]

@app.route('/')
def home():
    return render_template('home.html', total=len(students))  # HEY IMPORTANCE AAHE: total_students NAKO, fakt total

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/students')
def students_page():  # LIST CHE NAV 'students' AAHE, MHANUN FUNCTION CHE NAV 'students_page'
    return render_template('students.html', students=students)

if __name__ == '_main_':
    print("INSIDE MAIN")
    app.run(debug=True)