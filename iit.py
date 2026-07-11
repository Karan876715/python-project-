from flask import Flask, render_template_string, request, redirect, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from datetime import datetime
import os
import re

app = Flask(__name__)
app.secret_key = 'iitplacement_secret_2026'

# Gmail Config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'shindekarandeepak@gmail.com'
app.config['MAIL_PASSWORD'] = 'bpmm hxrr waax osgr'
mail = Mail(app)

DB = 'students.db'

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    return re.match(pattern, email) is not None

def init_db():
    with sqlite3.connect(DB) as con:
        # Juni table drop karun navin banav
        con.execute('DROP TABLE IF EXISTS students')
        con.execute('''CREATE TABLE students
                     (id INTEGER PRIMARY KEY,
                      username TEXT UNIQUE,
                      password TEXT,
                      name TEXT,
                      email TEXT,
                      phone TEXT,
                      address TEXT,
                      college TEXT,
                      college_address TEXT,
                      status TEXT DEFAULT 'Pending',
                      company TEXT,
                      lpa REAL)''')
init_db()

def create_certificate(name, email, phone, address, college, company, lpa):
    filename = f"certificate_{name.replace(' ','_')}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Background Gradient
    c.setFillColorRGB(0.04, 0.24, 0.57)
    c.rect(0, 0, width, height, fill=1)
    c.setFillColorRGB(0.4, 0.49, 0.92)
    c.rect(0, height/2, width, height/2, fill=1)

    # White content box - Height vadhvali
    c.setFillColorRGB(1, 1, 1)
    c.rect(40, 80, width-80, height-160, fill=1)

    # Header - ATA WHITE BOX MADHE AALA, Thoda Khali
    c.setFillColorRGB(0.04, 0.24, 0.57)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(width/2, height-120, "IIT PLACEMENT PRO")
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, height-145, "Official Placement Certificate")

    # Congratulations
    c.setFillColorRGB(0, 0.6, 0)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height-190, f"Congratulations {name}!")

    # Details Box
    c.setFillColorRGB(0.95, 0.95, 0.95)
    c.rect(70, height-420, width-140, 190, fill=1, stroke=0)

    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica-Bold", 12)
    y = height-240
    c.drawString(90, y, f"Name: {name}"); y-=25
    c.drawString(90, y, f"Email: {email}"); y-=25
    c.drawString(90, y, f"Phone: {phone}"); y-=25
    c.drawString(90, y, f"Address: {address[:50]}"); y-=25
    c.drawString(90, y, f"College: {college}"); y-=25
    c.drawString(90, y, f"Company: {company}"); y-=25
    c.setFillColorRGB(0.8, 0, 0)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(90, y, f"Package: {lpa} LPA")

    # Date - Thoda Var Aanla
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 10)
    c.drawString(90, 180, f"Issue Date: {datetime.now().strftime('%d %B %Y')}")

    # Admin Details - Thoda Var Aanla
    c.setFillColorRGB(0.04, 0.24, 0.57)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(width-250, 200, "Verified By: KARAN DIPAK SHINDE")
    c.setFont("Helvetica", 10)
    c.drawString(width-250, 185, "Admin - IIT Placement Pro")
    c.drawString(width-250, 170, "Hingoli, Maharashtra")

    # IIT PLACEMENT PRO STAMP - ATA WHITE PAGE VAR, THODA VAR
    c.setFillColorRGB(0.04, 0.24, 0.57)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, 115, "IIT PLACEMENT PRO")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, 100, "Official Placement Portal - Certified Document")

    # Circular Seal - ATA WHITE PAGE VAR + "IIT PLACEMENTS PRO" Small Madhe
    c.setStrokeColorRGB(0.04, 0.24, 0.57)
    c.setLineWidth(2.5)
    c.circle(width-120, 155, 35, stroke=1, fill=0)
    c.setFillColorRGB(0.04, 0.24, 0.57)
    c.setFont("Helvetica-Bold", 6.5)
    c.drawCentredString(width-120, 168, "IIT")
    c.drawCentredString(width-120, 158, "PLACEMENTS")
    c.drawCentredString(width-120, 148, "PRO")
    c.drawCentredString(width-120, 138, "2026")

    # Slogan - ATA WHITE PAGE VAR
    c.setFillColorRGB(0.4, 0.4, 0.4)
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width/2, 130, '"Dream Big, Achieve Bigger! Success is where Preparation meets Opportunity!"')

    c.save()
    return filename
def send_mail(to, subject, html, attachment=None):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.html = html
    if attachment and os.path.exists(attachment):
        with open(attachment, 'rb') as f:
            msg.attach(attachment, 'application/pdf', f.read())
    mail.send(msg)

BASE = '''
<!DOCTYPE html>
<html>
<head>
    <title>IIT PLACEMENT PRO</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        *{margin:0;padding:0;box-sizing:border-box;font-family:Arial,sans-serif}
        body{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);min-height:100vh}

        /* Navbar - Mobile Only */
       .navbar{display:none;background:#0b3d91;color:white;padding:15px 20px;align-items:center;position:sticky;top:0;z-index:100}
       .menu-btn{font-size:26px;cursor:pointer;margin-right:15px;display:none}

        /* Sidebar */
       .sidebar{position:fixed;left:0;top:0;width:260px;height:100%;background:#0b3d91;padding-top:20px;z-index:99;overflow-y:auto;transition:0.3s}
       .sidebar h3{color:white;padding:15px 20px;font-size:18px;text-align:center}
       .sidebar a{display:block;color:white;padding:12px 20px;text-decoration:none;font-size:14px;border-bottom:1px solid rgba(255,255,255,0.1)}
       .sidebar a:hover{background:rgba(255,255,255,0.2)}

        /* Main Content */
       .main-content{margin-left:260px;padding:15px;min-height:100vh;transition:0.3s}
       .card{background:white;padding:20px;border-radius:12px;box-shadow:0 4px 15px rgba(0,0,0,0.2);margin:15px auto;max-width:1200px}
       .stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:15px 0}
       .stat-box{padding:18px;border-radius:10px;color:white;text-align:center}
       .stat-box div{font-size:12px;opacity:0.9}
       .stat-box h2{font-size:28px;margin-top:5px}
       .btn-row{display:flex;gap:10px;margin-top:10px;flex-wrap:wrap}
       .btn{background:#28a745;color:white;padding:10px 20px;border:none;border-radius:6px;cursor:pointer;font-size:14px;text-decoration:none;display:inline-block}
       .btn-purple{background:#6f42c1}
       .btn-blue{background:#0b3d91;width:100%;margin-top:10px}
       .wall-of-fame{background:linear-gradient(135deg,#f093fb,#f5576c);padding:15px;border-radius:10px;margin:8px 0;color:white;text-align:center}
       .wall-of-fame h3{font-size:16px;margin:0}
       .wall-of-fame p{font-size:13px;margin:3px 0}
        input,select,textarea{width:100%;padding:12px;margin:8px 0;border:1px solid #ddd;border-radius:6px;font-size:14px}
       .btn-green{background:#28a745}
       .btn-red{background:#dc3545}
       .btn-orange{background:#fd7e14}
        table{width:100%;border-collapse:collapse;margin-top:15px;font-size:13px}
        th,td{padding:12px;text-align:left;border-bottom:1px solid #ddd}
        th{background:#0b3d91;color:white}
       .badge{background:#ffc107;padding:3px 8px;border-radius:10px;font-size:11px;font-weight:bold;color:#000}
       .flash{padding:12px;margin:10px;border-radius:6px;font-size:14px}
       .flash.success{background:#d4edda;color:#155724}
       .flash.danger{background:#f8d7da;color:#721c24}
       .flash.warning{background:#fff3cd;color:#856404}
       .update-box{background:#fff3cd;padding:15px;border-radius:8px;margin:15px 0;border:2px solid #ffc107}
       .footer{text-align:center;color:white;padding:20px;margin-top:30px;font-size:14px}
       .footer h4{font-size:18px;margin-bottom:5px}
       .company-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-top:15px}
       .company-item{background:#f0f0f0;padding:10px;border-radius:6px;text-align:center;font-size:13px}
       .guide-point{background:#e3f2fd;padding:12px;margin:8px 0;border-left:4px solid #0b3d91;border-radius:4px}
       .notif-item{background:#f8f9fa;padding:12px;margin:8px 0;border-radius:6px;border-left:4px solid #28a745}

        /* Overlay for mobile */
       .overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.5);z-index:98}
       .overlay.active{display:block}

        /* MOBILE VIEW */
        @media(max-width:768px){
           .navbar{display:flex}
           .menu-btn{display:block}
           .sidebar{left:-260px;box-shadow:2px 0 10px rgba(0,0,0,0.3)}
           .sidebar.active{left:0}
           .main-content{margin-left:0;padding:10px}
           .stats{grid-template-columns:repeat(2,1fr);gap:10px}
           .company-grid{grid-template-columns:repeat(2,1fr)}
           .card{padding:15px;margin:10px auto}
            table{font-size:11px}
            th,td{padding:8px 5px}
            h1{font-size:24px!important}
            h2{font-size:20px!important}
        }
    </style>
    <script>
        function toggleMenu(){
            document.querySelector('.sidebar').classList.toggle('active');
            document.querySelector('.overlay').classList.toggle('active');
        }
        function closeMenu(){
            document.querySelector('.sidebar').classList.remove('active');
            document.querySelector('.overlay').classList.remove('active');
        }
    </script>
</head>
<body>
    <div class="navbar">
        <span class="menu-btn" onclick="toggleMenu()">☰</span>
        <h2 style="font-size:20px">IIT PLACEMENT PRO</h2>
    </div>

    <div class="overlay" onclick="closeMenu()"></div>

    <div class="sidebar">
        <h3>🚀 IITPlacements Pro</h3>
        <a href="/" onclick="closeMenu()">🏠 Home</a>
        <a href="/register" onclick="closeMenu()">📝 Student Form</a>
        <a href="/login" onclick="closeMenu()">👤 Student Login</a>
        <a href="/admin/login" onclick="closeMenu()">🔐 Admin Panel</a>
        <a href="/list" onclick="closeMenu()">📄 List</a>
        <a href="/companies" onclick="closeMenu()">🏢 Companies (100+)</a>
        <a href="/guide" onclick="closeMenu()">🎯 Placement Guide</a>
        <a href="/stats" onclick="closeMenu()">📊 Live Stats</a>
        <a href="/resume" onclick="closeMenu()">📄 Resume Builder</a>
        <a href="/wall" onclick="closeMenu()">🏆 Wall of Fame</a>
        <a href="/notifications" onclick="closeMenu()">🔔 Notifications</a>
        <a href="/contact" onclick="closeMenu()">📞 Contact</a>
    </div>

    <div class="main-content">
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="flash {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        {{ content|safe }}
    </div>
</body>
</html>
'''

@app.route('/')
def home():
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM students")
        total_reg = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM students WHERE status='Accepted'")
        total_placed = cur.fetchone()[0]

    return render_template_string(BASE, content=f'''
    <div class="card" style="text-align:center">
        <h1 style="color:#0b3d91;font-size:32px;margin-bottom:15px">🚀 Welcome to IIT PLACEMENT PRO</h1>
        <h2 style="color:#667eea;margin-bottom:20px">Your Gateway to 100+ Top Companies</h2>

        <div style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:25px;border-radius:12px;margin:20px 0">
            <p style="font-size:20px;margin:10px 0"><b>"Dream Big, Achieve Bigger!"</b></p>
            <p style="font-size:16px;margin:5px 0"><i>"Your Success is Our Mission"</i></p>
        </div>

        <div class="stats">
            <div class="stat-box" style="background:linear-gradient(135deg,#667eea,#764ba2)">
                <div>Registered Students</div><h2>{total_reg}</h2>
            </div>
            <div class="stat-box" style="background:linear-gradient(135deg,#f093fb,#f5576c)">
                <div>Students Placed</div><h2>{total_placed}</h2>
            </div>
            <div class="stat-box" style="background:linear-gradient(135deg,#4facfe,#00f2fe)">
                <div>Partner Companies</div><h2>100+</h2>
            </div>
            <div class="stat-box" style="background:linear-gradient(135deg,#43e97b,#38f9d7)">
                <div>Highest LPA</div><h2>50</h2>
            </div>
        </div>

        <p style="font-size:17px;color:#333;line-height:1.6;margin:20px 0">
            Connect with <b>Google, Microsoft, Amazon, TCS, Infosys</b> and 100+ companies.<br>
            Get placed with packages up to <b style="color:#28a745">50 LPA</b>!
        </p>

        <div class="btn-row" style="justify-content:center">
            <a href="/register"><button class="btn" style="font-size:16px;padding:14px 30px">📝 Register Now</button></a>
            <a href="/login"><button class="btn btn-purple" style="font-size:16px;padding:14px 30px">👤 Student Login</button></a>
        </div>
    </div>

    <div class="footer">
        <h4>IIT PLACEMENT PRO</h4>
        <p>"Empowering Students, Building Futures"</p>
        <p style="font-size:12px;margin-top:10px">© 2026 IIT Placement Pro | Admin: KARAN DIPAK SHINDE | Hingoli, Maharashtra</p>
    </div>
    ''')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        college = request.form['college']
        college_address = request.form['college_address']

        if not is_valid_email(email):
            flash('Invalid Gmail! Please use real Gmail like yourname@gmail.com. Fake emails not allowed.', 'danger')
            return redirect('/register')

        try:
            with sqlite3.connect(DB) as con:
                con.execute("INSERT INTO students (username,password,name,email,phone,address,college,college_address) VALUES (?,?,?,?,?,?,?,?)",
                           (username,password,name,email,phone,address,college,college_address))
            return render_template_string(BASE, content=f'''
            <div class="card" style="max-width:600px;text-align:center">
                <h1 style="color:#0b3d91;margin-bottom:10px">Welcome {username}! 🎉</h1>
                <h2 style="color:#667eea;margin:15px 0">IIT PLACEMENT PRO</h2>
                <div style="background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:20px;border-radius:10px;margin:20px 0">
                    <p style="font-size:18px;margin:5px 0"><b>"Dream Big, Achieve Bigger!"</b></p>
                    <p style="font-size:16px;margin:5px 0"><i>"Your Success is Our Mission"</i></p>
                    <p style="font-size:16px;margin:5px 0"><i>"From Campus to Corporate - We Build Careers"</i></p>
                </div>
                <p style="font-size:15px;color:#28a745;margin:15px 0"><b>Registration Successful!</b> Now login to check your status.</p>
                <a href="/login"><button class="btn btn-blue">👤 Student Login</button></a>
            </div>
            ''')
        except sqlite3.IntegrityError:
            flash('Username already exists! Try another.', 'danger')

    return render_template_string(BASE, content='''
    <div class="card" style="max-width:600px">
        <h2>Student Registration Form</h2>
        <form method="POST">
            <input name="username" placeholder="Username *" required>
            <input type="password" name="password" placeholder="Password *" required>
            <input name="name" placeholder="Full Name *" required>
            <input type="email" name="email" placeholder="Gmail Address * (e.g. yourname@gmail.com)" required>
            <input name="phone" placeholder="Phone Number *" required>
            <textarea name="address" placeholder="Your Full Address *" rows="2" required></textarea>
            <input name="college" placeholder="College Name *" required>
            <textarea name="college_address" placeholder="College Address *" rows="2" required></textarea>
            <button class="btn btn-blue">Register Now</button>
        </form>
        <p style="font-size:12px;color:#666;margin-top:10px">* All fields required. Only real & valid Gmail accepted.</p>
    </div>
    ''')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with sqlite3.connect(DB) as con:
            cur = con.cursor()
            cur.execute("SELECT id, password, name FROM students WHERE username=?", (username,))
            row = cur.fetchone()
            if row and check_password_hash(row[1], password):
                session['user_id'] = row[0]
                session['name'] = row[2]
                return redirect('/dashboard')
            flash('Invalid username or password!', 'danger')
    return render_template_string(BASE, content='''
    <div class="card" style="max-width:400px">
        <h2>Student Login</h2>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button class="btn btn-blue">Login</button>
        </form>
        <p style="text-align:center;margin-top:15px">New User? <a href="/register" style="color:#0b3d91;font-weight:bold">Register Here</a></p>
    </div>
    ''')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        cur.execute("SELECT name,status,company,lpa FROM students WHERE id=?", (session['user_id'],))
        s = cur.fetchone()
    return render_template_string(BASE, content=f'''
    <div class="card" style="text-align:center">
        <h2>Welcome {s[0]}!</h2>
        <div style="background:#e3f2fd;padding:20px;border-radius:10px;margin:20px 0">
            <h3>Your Placement Status</h3>
            <p style="font-size:24px;margin:15px 0"><span class="badge" style="font-size:20px;padding:8px 20px;background:{'#28a745' if s[1]=='Accepted' else '#dc3545' if s[1]=='Rejected' else '#ffc107'}">{s[1]}</span></p>
            {f'<p style="font-size:18px"><b>Company:</b> {s[2]}</p><p style="font-size:18px"><b>Package:</b> {s[3]} LPA</p>' if s[1]=='Accepted' else ''}
        </div>
        <a href="/logout"><button class="btn-red">Logout</button></a>
    </div>
    ''')

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin_karan' and request.form['password'] == 'Karan@123':
            session['admin'] = True
            return redirect('/admin')
        flash('Invalid admin credentials!', 'danger')
    return render_template_string(BASE, content='''
    <div class="card" style="max-width:400px">
        <h2>Admin Login</h2>
        <form method="POST">
            <input name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button class="btn btn-blue">Login</button>
        </form>
    </div>
    ''')

@app.route('/admin')
def admin():
    if 'admin' not in session:
        return redirect('/admin/login')

    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        cur.execute("SELECT id,username,name,email,status,company,lpa FROM students ORDER BY id DESC")
        rows = cur.fetchall()

    table_rows = ""
    for r in rows:
        status_badge = f'<span class="badge" style="background:{"#28a745" if r[4]=="Accepted" else "#dc3545" if r[4]=="Rejected" else "#ffc107"}">{r[4]}</span>'
        actions = ""
        if r[4] == 'Pending':
            actions = f'''
                <a href="/accept/{r[0]}"><button class="btn-green" style="padding:6px 12px;font-size:12px">✓ Accept</button></a>
                <a href="/reject/{r[0]}"><button class="btn-red" style="padding:6px 12px;font-size:12px">✗ Reject</button></a>
            '''
        elif r[4] == 'Accepted':
            actions = f'<a href="/accept/{r[0]}"><button class="btn-orange" style="padding:6px 12px;font-size:12px">✏️ Edit</button></a> <span style="color:#28a745;font-weight:bold">{r[5]} - {r[6]} LPA</span>'

        table_rows += f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{status_badge}</td><td>{actions}</td></tr>"

    return render_template_string(BASE, content=f'''
    <div class="card">
        <h2>🔐 Admin Dashboard - All Students</h2>
        <p style="color:#666;margin-bottom:15px"><b>Note:</b> Mail will be sent only once when you Accept a Pending student. Updating Accepted students will NOT send email.</p>
        <table>
            <tr><th>ID</th><th>Username</th><th>Name</th><th>Email</th><th>Status</th><th>Action</th></tr>
            {table_rows}
        </table>
        <a href="/logout" style="float:right"><button class="btn-red">Logout</button></a>
    </div>
    ''')

@app.route('/accept/<int:id>', methods=['GET','POST'])
def accept(id):
    if 'admin' not in session:
        return redirect('/admin/login')

    if request.method == 'POST':
        company = request.form['company']
        lpa = request.form['lpa']

        with sqlite3.connect(DB) as con:
            cur = con.cursor()
            cur.execute("SELECT status, name, email, phone, address, college FROM students WHERE id=?", (id,))
            data = cur.fetchone()

            if not data:
                flash('Student not found!', 'danger')
                return redirect('/admin')

            current_status = data[0]
            name, email, phone, address, college = data[1], data[2], data[3], data[4], data[5]

            cur.execute("UPDATE students SET status='Accepted', company=?, lpa=? WHERE id=?", (company, lpa, id))
            con.commit()

            # MAIL FAKT JAR STATUS 'Pending' HOTA TARACH PATHAV
            if current_status == 'Pending':
                pdf_file = create_certificate(name, email, phone, address, college, company, lpa)
                send_mail(
                    email,
                    f"🎉 Congratulations! Placed at {company} - {lpa} LPA",
                    f"""
                    <div style='font-family:Arial;padding:20px;max-width:600px'>
                        <h2 style='color:#0b3d91'>Congratulations {name}! 🎉</h2>
                        <p style='font-size:16px'>We are thrilled to inform you that <b>{company}</b> has selected you!</p>
                        <div style='background:#e8f5e9;padding:15px;border-left:4px solid #28a745;margin:20px 0'>
                            <h3 style='margin:0 0 10px 0'>Your Placement Details:</h3>
                            <p><b>Name:</b> {name}</p>
                            <p><b>Email:</b> {email}</p>
                            <p><b>Phone:</b> {phone}</p>
                            <p><b>Address:</b> {address}</p>
                            <p><b>College:</b> {college}</p>
                            <p><b>Company:</b> {company}</p>
                            <p><b>Package:</b> {lpa} LPA</p>
                        </div>
                        <p style='color:#28a745;font-size:18px'><b>"Dream Big, Achieve Bigger!"</b></p>
                        <p>PFA: Your Official Placement Certificate</p>
                        <hr>
                        <p style='color:#666;font-size:12px'>
                            <b>IIT PLACEMENT PRO</b><br>
                            Admin: KARAN DIPAK SHINDE<br>
                            Hingoli, Maharashtra
                        </p>
                    </div>
                    """,
                    pdf_file
                )
                flash(f'{name} placed at {company} - {lpa} LPA. Certificate sent to {email}!', 'success')
            else:
                flash(f'{name} details updated to {company} - {lpa} LPA. No email sent.', 'warning')

        return redirect('/admin')

    return render_template_string(BASE, content='''
    <div class="card" style="max-width:500px">
        <h2>Accept Student - Enter Details</h2>
        <form method="POST">
            <input name="company" placeholder="Company Name *" required>
            <input name="lpa" placeholder="Package LPA * (e.g. 12.5)" required>
            <button class="btn-green">Accept & Send Certificate</button>
        </form>
        <p style="font-size:12px;color:#666;margin-top:10px">* Email will be sent only if student is in Pending status</p>
    </div>
    ''')

@app.route('/reject/<int:id>')
def reject(id):
    if 'admin' not in session:
        return redirect('/admin/login')
    with sqlite3.connect(DB) as con:
        con.execute("UPDATE students SET status='Rejected', company=NULL, lpa=NULL WHERE id=?", (id,))
    flash('Student rejected!', 'warning')
    return redirect('/admin')

@app.route('/list')
def list_students():
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        cur.execute("SELECT name, college, email, company, lpa, status FROM students WHERE status='Accepted' ORDER BY lpa DESC")
        rows = cur.fetchall()

    table_rows = ""
    for i, r in enumerate(rows):
        status_color = "#28a745" if r[5]=='Accepted' else "#dc3545"
        table_rows += f"""
        <tr>
            <td>{i+1}</td>
            <td><b>{r[0]}</b></td>
            <td>{r[1]}</td>
            <td>{r[2]}</td>
            <td><span style='color:#28a745;font-weight:bold'>{r[3]}</span></td>
            <td><b>{r[4]} LPA</b></td>
        </tr>"""

    return render_template_string(BASE, content=f'''
    <div class="card">
        <div style="text-align:center;margin-bottom:20px">
            <h1 style="color:#0b3d91;font-size:28px;margin-bottom:8px">🚀 IIT PLACEMENT PRO</h1>
            <p style="color:#667eea;font-size:16px;margin:5px 0"><b>"Dream Big, Achieve Bigger!"</b></p>
            <p style="color:#764ba2;font-size:14px"><i>"From Campus to Corporate - We Build Careers"</i></p>
        </div>

        <h2 style="text-align:center">📄 Placed Students List - 2026 Batch</h2>
        <p style="text-align:center;color:#666;margin-bottom:15px">Celebrating our successfully placed students</p>

        <table>
            <tr>
                <th>Sr</th>
                <th>Student Name</th>
                <th>College Name</th>
                <th>Gmail ID</th>
                <th>Company</th>
                <th>Package</th>
            </tr>
            {table_rows if table_rows else '<tr><td colspan="6" style="text-align:center;color:#666">No placements yet. Be the first!</td></tr>'}
        </table>

        <div style="text-align:center;margin-top:20px;padding:15px;background:#e8f5e9;border-radius:8px">
            <p style="color:#28a745;font-size:16px;margin:0"><b>🎉 Total Placed: {len(rows)} Students</b></p>
            <p style="color:#666;font-size:13px;margin:5px 0 0 0">"Success is where Preparation meets Opportunity!"</p>
        </div>
    </div>
    ''')
@app.route('/companies')
def companies():
    companies_list = [
        'Google','Microsoft','Amazon','TCS','Infosys','Wipro','Accenture','IBM','Cognizant','Capgemini',
        'HCL','Tech Mahindra','Deloitte','EY','KPMG','PwC','Adobe','Oracle','Salesforce','SAP',
        'Apple','Meta','Netflix','Uber','Airbnb','Twitter','LinkedIn','Dell','HP','Intel',
        'Cisco','Nvidia','Qualcomm','Broadcom','Texas Instruments','AMD','VMware','Citrix','Red Hat','Zoho',
        'Paytm','PhonePe','Flipkart','Myntra','Meesho','Zomato','Swiggy','Ola','Razorpay','CRED',
        'BYJU\'S','Unacademy','Vedantu','UpGrad','Physics Wallah','Groww','Zerodha','PolicyBazaar','Digit','Nykaa',
        'L&T','Reliance','Adani','Tata Motors','Mahindra','Bajaj Auto','Maruti Suzuki','Hero MotoCorp','TVS','Ashok Leyland',
        'JP Morgan','Morgan Stanley','Goldman Sachs','Barclays','HSBC','Citibank','Bank of America','Wells Fargo','Deutsche Bank','BNP Paribas',
        'PayPal','Visa','Mastercard','American Express','Walmart Labs','Target','Samsung','LG','Sony','Panasonic',
        'Siemens','Bosch','Honeywell','Schneider Electric','ABB','General Electric','Shell','BP','ExxonMobil','Chevron'
    ]
    companies_html = "".join([f'<div class="company-item">{c}</div>' for c in companies_list])
    return render_template_string(BASE, content=f'''
    <div class="card">
        <h2>🏢 100+ Partner Companies</h2>
        <p style="text-align:center;color:#666;margin-bottom:20px">We are partnered with top MNCs and startups across the globe</p>
        <div class="company-grid">{companies_html}</div>
    </div>
    ''')

@app.route('/guide')
def guide():
    return render_template_string(BASE, content='''
    <div class="card">
        <h2>🎯 Placement Guide - 2026 Batch</h2>
        <div class="guide-point"><b>1. Aptitude Test:</b> Practice Quantitative, Logical, Verbal. 60% cutoff.</div>
        <div class="guide-point"><b>2. Technical Round:</b> DSA, DBMS, OS, OOPs. Leetcode 200+ problems.</div>
        <div class="guide-point"><b>3. Coding Round:</b> 2-3 problems in 90 mins. Focus on arrays, strings, trees.</div>
        <div class="guide-point"><b>4. HR Interview:</b> Be confident. Know your resume. Ask questions.</div>
        <div class="guide-point"><b>5. Resume Tips:</b> 1 page, projects first, no typos, PDF format.</div>
        <div class="guide-point"><b>6. Group Discussion:</b> Speak clearly, listen, don't argue, give data.</div>
    </div>
    ''')

@app.route('/stats')
def stats():
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        cur.execute("SELECT COUNT(*) FROM students")
        total_reg = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM students WHERE status='Accepted'")
        total_placed = cur.fetchone()[0]
        cur.execute("SELECT MAX(lpa) FROM students WHERE status='Accepted'")
        max_lpa = cur.fetchone()[0] or 0
        cur.execute("SELECT company, COUNT(*) as cnt FROM students WHERE status='Accepted' GROUP BY company ORDER BY cnt DESC LIMIT 5")
        top_companies = cur.fetchall()

    placement_percent = int((total_placed / total_reg * 100)) if total_reg > 0 else 0
    companies_html = "".join([f'<div class="company-item"><b>{c[0]}</b><br>{c[1]} Students</div>' for c in top_companies])

    return render_template_string(BASE, content=f'''
    <div class="card">
        <h2>📊 Live Placement Stats - 2026 Batch</h2>
        <div class="stats">
            <div class="stat-box" style="background:linear-gradient(135deg,#667eea,#764ba2)">
                <div>Total Registered</div><h2>{total_reg}</h2>
            </div>
            <div class="stat-box" style="background:linear-gradient(135deg,#f093fb,#f5576c)">
                <div>Students Placed</div><h2>{total_placed}</h2>
            </div>
            <div class="stat-box" style="background:linear-gradient(135deg,#4facfe,#00f2fe)">
                <div>Partner Companies</div><h2>100+</h2>
            </div>
            <div class="stat-box" style="background:linear-gradient(135deg,#43e97b,#38f9d7)">
                <div>Highest Package</div><h2>{max_lpa} LPA</h2>
            </div>
        </div>

        <div class="card" style="margin-top:20px;background:#e3f2fd">
            <h3>📈 Placement Percentage: {placement_percent}%</h3>
            <div style="background:#ddd;border-radius:10px;height:25px;margin-top:10px">
                <div style="background:#28a745;height:25px;border-radius:10px;width:{placement_percent}%;text-align:center;color:white;line-height:25px;font-weight:bold">
                    {placement_percent}%
                </div>
            </div>
        </div>

        <h3 style="margin-top:25px">🏆 Top 5 Companies</h3>
        <div class="company-grid">
            {companies_html if companies_html else '<p style="text-align:center;color:#666">No placements yet</p>'}
        </div>

        <p style="text-align:center;margin-top:20px;color:#0b3d91;font-size:16px"><b>"Data Speaks Louder Than Words - {placement_percent}% Success Rate!"</b></p>
    </div>
    ''')

@app.route('/resume')
def resume():
    return render_template_string(BASE, content='''
    <div class="card">
        <h2>📄 Resume Builder Tips</h2>
        <div class="guide-point"><b>1. Keep it 1 Page:</b> Recruiters spend 6 seconds on resume. Be concise.</div>
        <div class="guide-point"><b>2. Projects First:</b> Mention 2-3 best projects with Tech Stack + GitHub link.</div>
        <div class="guide-point"><b>3. Skills Section:</b> Python, Java, SQL, React - Add only what you know.</div>
        <div class="guide-point"><b>4. No Typos:</b> Use Grammarly. 1 typo = Rejection.</div>
        <div class="guide-point"><b>5. PDF Format:</b> Always send PDF, never Word file.</div>
        <div class="guide-point"><b>6. CGPA:</b> Mention only if > 7.5. Else skip.</div>
        <div class="guide-point"><b>7. LinkedIn:</b> Add profile link. Keep it updated.</div>
        <a href="#"><button class="btn btn-blue" onclick="alert('Coming Soon! Use Canva for now.')">📥 Download Sample Resume</button></a>
    </div>
    ''')

@app.route('/wall')
def wall():
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        cur.execute("SELECT name, company, lpa FROM students WHERE status='Accepted' ORDER BY lpa DESC LIMIT 10")
        rows = cur.fetchall()

    wall_html = "".join([f'''
    <div class="wall-of-fame">
        <h3>🏆 {r[0]}</h3>
        <p><b>{r[1]}</b> - {r[2]} LPA</p>
        <p style="font-size:11px;opacity:0.9">"Hard Work Pays Off!"</p>
    </div>
    ''' for r in rows])

    return render_template_string(BASE, content=f'''
    <div class="card">
        <h2>🏆 Wall of Fame - Our Achievers</h2>
        <p style="text-align:center;color:#666;margin-bottom:20px">Celebrating our top placed students!</p>
        {wall_html if wall_html else '<p style="text-align:center;color:#666">No placements yet. Be the first!</p>'}
    </div>
    ''')

@app.route('/notifications')
def notifications():
    return render_template_string(BASE, content='''
    <div class="card">
        <h2>🔔 Latest Notifications</h2>
        <div class="notif-item">
            <b>🎯 New Drive:</b> Google hiring SDE - 45 LPA. Apply by 15th July 2026
        </div>
        <div class="notif-item">
            <b>📢 Update:</b> Microsoft test scheduled on 20th July. Check email.
        </div>
        <div class="notif-item">
            <b>🏆 Achievement:</b> 850+ students placed this year! New record.
        </div>
        <div class="notif-item">
            <b>📝 Workshop:</b> Resume building session on 10th July at 4 PM.
        </div>
        <div class="notif-item">
            <b>💼 Internship:</b> Amazon SDE Intern - 1.2 Lakh/month. 2nd/3rd year eligible.
        </div>
    </div>
    ''')

@app.route('/contact')
def contact():
    return render_template_string(BASE, content='''
    <div class="card" style="max-width:600px;text-align:center">
        <h2>📞 Contact Us</h2>
        <div style="background:#e3f2fd;padding:25px;border-radius:10px;margin:20px 0">
            <h3 style="color:#0b3d91;margin-bottom:15px">IIT PLACEMENT PRO</h3>
            <p style="font-size:16px;margin:10px 0"><b>👤 Admin:</b> KARAN DIPAK SHINDE</p>
            <p style="font-size:16px;margin:10px 0"><b>📧 Email:</b> shindekarandeepak@gmail.com</p>
            <p style="font-size:16px;margin:10px 0"><b>📱 Phone:</b> 8767156551</p>
            <p style="font-size:16px;margin:10px 0"><b>📍 Address:</b> S.R.P.F Camp, Near Dakshata Nagar, Hingoli, Maharashtra - 431513</p>
            <p style="font-size:16px;margin:10px 0"><b>🏫 College:</b> Government Polytechnic, Hingoli</p>
        </div>
        <p style="color:#28a745;font-size:18px;margin-top:20px"><b>"Your Success is Our Mission!"</b></p>
    </div>
    ''')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)