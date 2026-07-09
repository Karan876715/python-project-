from flask import Flask, request, redirect, url_for, session, render_template_string, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import io

app = Flask(__name__)
app.secret_key = "karan_iit_2026_final_pro"
DB = "placement.db"

COMPANIES_100 = ["Google","Microsoft","Amazon","Infosys","TCS","Wipro","Meta","Apple","Netflix","Adobe","Goldman Sachs","Flipkart","Samsung","Intel","IBM","Oracle","Deloitte","Accenture","Capgemini","Cognizant","HCL","Tech Mahindra","L&T","BYJU'S","Paytm","Zomato","Swiggy","Ola","Uber","Zoho","PhonePe","Razorpay","CRED","Meesho","Unacademy","PhysicsWallah","JP Morgan","Morgan Stanley","Deutsche Bank","HSBC","Qualcomm","Nvidia","Cisco","HP","Dell","Tata Motors","Mahindra","Bajaj Auto","Reliance Jio","Airtel","ISRO","DRDO","BHEL","ONGC","Mindtree","Mphasis","Hexaware","Persistent","KPIT","Siemens","Tesla","SpaceX","Twitter","LinkedIn","Salesforce","SAP","Atlassian","Walmart","PayPal","Stripe","Coinbase","Dream11","Nykaa","Boat","OnePlus","Xiaomi","Realme","Vivo","Nokia","Bosch","Adani","Tata Steel","JSW","Maruti","Hyundai","Kia","Honda","Yamaha","Bajaj Finserv","ICICI Bank","HDFC Bank","Axis Bank","SBI","Kotak","ZScaler","ServiceNow"]

ADMIN_USER = "admin_karan"
ADMIN_PASS_HASH = generate_password_hash("Karan@123")

def init_db():
    with sqlite3.connect(DB, timeout=10) as con:
        cur=con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, name TEXT, college TEXT, address TEXT, phone TEXT, enrollment TEXT, email TEXT, status TEXT DEFAULT 'Pending', company TEXT DEFAULT '', package TEXT DEFAULT '')")
        cur.execute("CREATE TABLE IF NOT EXISTS companies (id INTEGER PRIMARY KEY, name TEXT, info TEXT)")
        cur.execute("CREATE TABLE IF NOT EXISTS notifications (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, message TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP)")
        cur.execute("SELECT COUNT(*) FROM companies")
        if cur.fetchone()[0] == 0:
            for i,nm in enumerate(COMPANIES_100,1):
                cur.execute("INSERT INTO companies VALUES (?,?,?)",(i,nm,f"{8+i%25} LPA"))
        con.commit()

init_db()

BASE = '''<!DOCTYPE html><html><head><title>IITPlacements Pro</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',Arial}
body{display:flex;flex-direction:column;min-height:100vh;background:linear-gradient(135deg,#667eea 0%,#764ba2 100%)}
.wrapper{display:flex;flex:1}
.sidebar{width:250px;background:#0b3d91;color:#fff;padding:15px;position:fixed;height:100vh;overflow-y:auto}
.sidebar h3{color:#FFD700;margin-bottom:20px;text-align:center;font-size:20px}
.sidebar a{display:block;color:#fff;text-decoration:none;padding:12px;margin:6px 0;border-radius:8px;transition:0.3s}
.sidebar a:hover{background:#1a5ed7;transform:translateX(8px)}
.main{margin-left:250px;padding:20px;width:100%;padding-bottom:70px}
.card{background:rgba(255,255,255,0.95);padding:25px;border-radius:15px;margin-bottom:20px;box-shadow:0 8px 25px #0003}
.btn{padding:12px 20px;border:none;border-radius:8px;color:#fff;cursor:pointer;font-weight:bold}
.green{background:#2e7d32}.blue{background:#2196F3}.purple{background:#7b1fa2}.red{background:#d32f2f}.orange{background:#FF9800}
.form-box{background:#fff;padding:25px;border-radius:15px;max-width:700px;margin:auto}
input,textarea{width:100%;padding:12px;margin:8px 0 15px;border:2px solid #e0e0e0;border-radius:8px}
table{width:100%;border-collapse:collapse;background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 15px #0002}
th,td{padding:14px;border-bottom:1px solid #eee;text-align:left}
th{background:#0b3d91;color:#fff}
.footer{background:#081f4d;color:white;text-align:center;padding:18px;margin-left:250px}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:15px;margin:25px 0}
.stat-box{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);color:white;padding:25px;border-radius:15px;text-align:center}
.stat-box h2{font-size:36px;margin:8px 0}
.badge{padding:5px 12px;border-radius:20px;font-size:12px;font-weight:bold}
.badge-accept{background:#c8e6c9;color:#2e7d32}
.badge-reject{background:#ffcdd2;color:#c62828}
.badge-pending{background:#fff3cd;color:#f57c00}
.wall-item{background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%);color:white;padding:20px;border-radius:12px;margin:10px 0;text-align:center}
.notif-box{background:#e3f2fd;padding:15px;border-radius:8px;margin:10px 0;border-left:4px solid #2196F3}
.info-box{background:#fff;padding:20px;border-radius:12px;margin-bottom:20px;border-left:5px solid #0b3d91}
</style></head>
<body><div class="wrapper"><div class="sidebar"><h3>🚀 IITPlacements Pro</h3>
<a href="/">🏠 Home</a>
<a href="/register">📝 Student Form</a>
<a href="/login">👤 Student Login</a>
<a href="/admin/login">🔐 Admin Panel</a>
<a href="/list">📄 List</a>
<a href="/companies">🏢 Companies (100+)</a>
<a href="/placement-guide">🎯 Placement Guide</a>
<a href="/stats">📊 Live Stats</a>
<a href="/resume-builder">📄 Resume Builder</a>
<a href="/wall-of-fame">🏆 Wall of Fame</a>
<a href="/notifications">🔔 Notifications</a>
<a href="/contact">📞 Contact</a>
</div><div class="main">{{content|safe}}</div></div>
<div class="footer">🏢IIT PLACEMENTS PRO👨‍💻 © 2026. Developed by KARAN DIPAK SHINDE</div></body></html>'''

@app.route('/')
def home():
    with sqlite3.connect(DB, timeout=10) as con:
        cur=con.cursor()
        cur.execute("SELECT COUNT(*) FROM students"); total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM students WHERE status='Accept'"); placed = cur.fetchone()[0]
        cur.execute("SELECT name,company,package FROM students WHERE status='Accept' ORDER BY id DESC LIMIT 3"); recent = cur.fetchall()
    recent_html = "".join([f'<div class="wall-item"><h3>🎉 {r[0]}</h3><p>Placed at <b>{r[1] or "Top MNC"}</b></p><p>Package: <b>{r[2] or "18 LPA"}</b></p></div>' for r in recent]) if recent else '<p style="text-align:center;color:#666">Be the first to get placed!</p>'
    return render_template_string(BASE, content=f'''
    <div class="card"><h1 style="color:#0b3d91;font-size:40px">IITPlacements Pro Portal</h1>
    <div class="stats">
        <div class="stat-box"><p>Registered</p><h2>{total}</h2></div>
        <div class="stat-box" style="background:linear-gradient(135deg,#f093fb 0%,#f5576c 100%)"><p>Placed</p><h2>{placed}</h2></div>
        <div class="stat-box" style="background:linear-gradient(135deg,#4facfe 0%,#00f2fe 100%)"><p>Companies</p><h2>100+</h2></div>
        <div class="stat-box" style="background:linear-gradient(135deg,#43e97b 0%,#38f9d7 100%)"><p>Highest</p><h2>45 LPA</h2></div>
    </div>
    <a href="/register"><button class="btn green">📝 Register Now</button></a> 
    <a href="/resume-builder"><button class="btn purple">📄 Build Resume</button></a>
    </div>
    <div class="card" style="text-align:left"><h3>🏆 Recent Placements - Wall of Fame</h3>{recent_html}
    <a href="/wall-of-fame"><button class="btn" style="background:#0b3d91;width:100%;margin-top:15px">View All Success Stories →</button></a></div>''')

@app.route('/resume-builder')
def resume_builder():
    return render_template_string(BASE, content='''
    <div class="card" style="max-width:800px;margin:auto;text-align:left">
        <h2 style="color:#0b3d91;text-align:center">📄 Professional Resume Builder</h2>
        <div class="info-box"><h3>🎯 How it Works:</h3>
        <p><b>Step 1:</b> Register on portal with complete details</p>
        <p><b>Step 2:</b> Login and click "Download Resume" button</p>
        <p><b>Step 3:</b> Auto-generated ATS-friendly resume ready!</p></div>
        <div class="info-box" style="background:#e8f5e9"><h3>✅ Features:</h3>
        <p>✓ One Page Professional Format</p>
        <p>✓ Auto-fill from your profile</p>
        <p>✓ Skills, Projects, Education sections</p>
        <p>✓ Download as TXT format</p></div>
        <a href="/login"><button class="btn green" style="width:100%">Login to Generate Resume →</button></a>
    </div>''')

@app.route('/download-resume/<username>')
def download_resume(username):
    with sqlite3.connect(DB, timeout=10) as con:
        cur=con.cursor()
        cur.execute("SELECT * FROM students WHERE username=?",(username,));s=cur.fetchone()
    if not s: return "User not found"
    resume = f"""
IIT PLACEMENTS - PROFESSIONAL RESUME
{'='*60}
Name: {s[3]}
Email: {s[8]}
Phone: {s[6]}
College: {s[4]}

EDUCATION
{'='*60}
B.Tech - {s[4]}
CGPA: 8.5/10

TECHNICAL SKILLS
{'='*60}
Programming: Python, Java, C++
Web Development: Flask, HTML, CSS, JavaScript
Database: SQLite, MySQL
Tools: Git, VS Code, Linux

PROJECTS
{'='*60}
1. IIT Placement Portal - Flask + SQLite
   Full stack web application with Admin Panel
   
2. Resume Builder System - Python
   Auto-generates professional resumes

ACHIEVEMENTS
{'='*60}
- Outstanding Project by KARAN DIPAK SHINDE
- IITPlacements Pro Portal Developer

{'='*60}
Generated via IITPlacements Pro | 2026
"""
    return send_file(io.BytesIO(resume.encode()), mimetype='text/plain', as_attachment=True, download_name=f'{username}_Resume.txt')

@app.route('/wall-of-fame')
def wall_of_fame():
    with sqlite3.connect(DB, timeout=10) as con:
        cur=con.cursor()
        cur.execute("SELECT name,college,company,package FROM students WHERE status='Accept' ORDER BY id DESC"); placed = cur.fetchall()
    html = "".join([f'<div class="wall-item"><h2>🎉 {r[0]}</h2><p><b>College:</b> {r[1]}</p><p><b>Company:</b> {r[2] or "Top MNC"}</p><p><b>Package:</b> {r[3] or "18 LPA"}</p></div>' for r in placed]) if placed else '<div class="info-box"><p style="text-align:center">No placements yet. Be the first!</p></div>'
    return render_template_string(BASE, content=f'<div class="card"><h2 style="color:#0b3d91">🏆 Wall of Fame - Success Stories</h2><p>Our placed students!</p></div>{html}')

@app.route('/notifications')
def notifications():
    if 'username' not in session: return redirect('/login')
    with sqlite3.connect(DB, timeout=10) as con:
        cur=con.cursor()
        cur.execute("SELECT message,created_at FROM notifications WHERE username=? ORDER BY id DESC LIMIT 20",(session['username'],)); notifs = cur.fetchall()
    html = "".join([f'<div class="notif-box"><p>{n[0]}</p><small>{n[1]}</small></div>' for n in notifs]) if notifs else '<div class="info-box"><p>No notifications yet.</p></div>'
    return render_template_string(BASE, content=f'<div class="card"><h2>🔔 Your Notifications</h2></div>{html}')

@app.route('/placement-guide')
def placement_guide():
    return render_template_string(BASE, content='''
    <div class="card" style="text-align:left"><h2 style="color:#0b3d91;text-align:center">🎯 IIT Placement Guide</h2>
    <div class="info-box"><h3>📘 Resume Tips</h3><p>✅ 1 Page Resume</p><p>✅ Projects: Python, Flask, ML</p><p>✅ CGPA > 7.5 | GitHub + LinkedIn</p></div>
    <div class="info-box"><h3>💻 Technical Prep</h3><p>✅ DSA: LeetCode 200+ Problems</p><p>✅ OOPs, DBMS, OS - Core CS</p></div>
    <div class="info-box" style="background:#fff3cd"><h3>⚡ Golden Tips by KARAN DIPAK SHINDE</h3><p>1. Daily 3 DSA problems</p><p>2. 1 project on GitHub</p><p>3. Mock Interview practice</p></div></div>''')

@app.route('/stats')
def stats():
    with sqlite3.connect(DB, timeout=10) as con:
        cur=con.cursor()
        cur.execute("SELECT COUNT(*) FROM students"); total = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM students WHERE status='Accept'"); accept = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM students WHERE status='Pending'"); pending = cur.fetchone()[0]
    return render_template_string(BASE, content=f'''
    <div class="card"><h2>📊 Live Statistics</h2></div>
    <div class="stats">
        <div class="stat-box"><p>Total</p><h2>{total}</h2></div>
        <div class="stat-box" style="background:linear-gradient(135deg,#43e97b 0%,#38f9d7 100%)"><p>Placed</p><h2>{accept}</h2></div>
        <div class="stat-box" style="background:linear-gradient(135deg,#fa709a 0%,#fee140 100%)"><p>Pending</p><h2>{pending}</h2></div>
    </div>''')

@app.route('/companies')
def companies_page():
    with sqlite3.connect(DB, timeout=10) as con:
        cur=con.cursor();cur.execute("SELECT * FROM companies");rows=cur.fetchall()
    html="".join([f'<span style="display:inline-block;background:#fff;margin:6px;padding:12px 18px;border-radius:10px;box-shadow:0 3px 8px #0002"><b>{r[1]}</b><br><small>{r[2]}</small></span>' for r in rows])
    return render_template_string(BASE, content=f"<div class=card style=text-align:left><h2>🏢 100+ Companies</h2><div>{html}</div></div>")

@app.route('/list')
def list_page():
    with sqlite3.connect(DB, timeout=10) as con:
        cur=con.cursor();cur.execute("SELECT username,college,status FROM students");rows=cur.fetchall()
    tr="".join([f"<tr><td>{i+1}</td><td>{r[0]}</td><td>{r[1]}</td><td><span class='badge badge-{r[2].lower()}'>{r[2]}</span></td></tr>" for i,r in enumerate(rows)]) or "<tr><td colspan=4>No Data</td></tr>"
    return render_template_string(BASE, content=f"<div class=card><h2>📄 Registered Students</h2></div><table><tr><th>#</th><th>Username</th><th>College</th><th>Status</th></tr>{tr}</table>")

@app.route('/contact')
def contact():
    top4 = "".join([f'<p>🔹 <b>{c}</b> - Premium Recruiter | 25 LPA</p>' for c in COMPANIES_100[:4]])
    return render_template_string(BASE, content=f'''
    <div class="card" style="text-align:left;max-width:700px;margin:auto">
        <h2 style="text-align:center;color:#0b3d91">📞 IIT PLACEMENTS - Contact</h2><hr>
        <h3>🏆 Top 4 Companies:</h3><div style="background:#e3f2fd;padding:18px;border-radius:10px">{top4}</div><hr>
        <p><b>📱 Phone:</b> 8767156551, 9960978900</p>
        <p><b>📧 Gmail:</b> shindekarandeepak@gmail.com</p>
        <div style="background:#d1ecf1;padding:18px;border-radius:10px;border-left:5px solid #0c5460">
            <p><b>👨‍💼 Admin:</b> KARAN DIPAK SHINDE</p><p><b>Role:</b> Full Stack Developer</p>
        </div></div>''')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            with sqlite3.connect(DB, timeout=10) as con:
                con.execute("INSERT INTO students (username,password,name,college,address,phone,enrollment,email) VALUES (?,?,?,?,?,?,?,?)",(request.form['username'],generate_password_hash(request.form['password']),request.form['name'],request.form['college'],request.form['address'],request.form['phone'],request.form['enrollment'],request.form['email']))
                con.commit()
            with sqlite3.connect(DB, timeout=10) as con:
                con.execute("INSERT INTO notifications (username,message) VALUES (?,?)",(request.form['username'], "🎉 Welcome! Registration successful. Admin will verify soon."))
                con.commit()
            return redirect(url_for('thankyou', username=request.form['username']))
        except:
            return render_template_string(BASE, content="<div class=card><h3 style=color:red>Username exists</h3></div>")
    return render_template_string(BASE, content='<div class="form-box"><h2>📝 Student Registration</h2><form method="POST"><input name="username" placeholder="Username *" required><input type="password" name="password" placeholder="Password *" required><input name="name" placeholder="Full Name *" required><input name="college" placeholder="College *" required><textarea name="address" placeholder="Address"></textarea><input name="phone" placeholder="Phone"><input name="enrollment" placeholder="Enrollment No"><input name="email" type="email" placeholder="Gmail *" required><button class="btn green" style="width:100%">Submit</button></form></div>')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        with sqlite3.connect(DB, timeout=10) as con:
            cur=con.cursor();cur.execute("SELECT password FROM students WHERE username=?",(request.form['username'],));row=cur.fetchone()
        if row and check_password_hash(row[0], request.form['password']):
            session['username']=request.form['username']
            return redirect(url_for('thankyou', username=request.form['username']))
        return render_template_string(BASE, content="<div class=card><h3 style=color:red>Wrong Password</h3></div>")
    return render_template_string(BASE, content='<div class="form-box"><h2>👤 Student Login</h2><form method="POST"><input name="username" placeholder="Username" required><input type="password" name="password" placeholder="Password" required><button class="btn blue" style="width:100%">Login</button></form></div>')

@app.route('/thankyou/<username>')
def thankyou(username):
    with sqlite3.connect(DB, timeout=10) as con:
        cur=con.cursor();cur.execute("SELECT status FROM students WHERE username=?",(username,));r=cur.fetchone()
    s=r[0] if r else 'Pending'
    resume_btn = f'<a href="/download-resume/{username}"><button class="btn purple" style="width:100%;margin-top:15px">📄 Download Your Resume</button></a>' if session.get('username')==username else ''
    if s == 'Accept':
        msg = '<div style="background:#d4edda;color:#155724;padding:20px;border-radius:10px;margin-top:20px;border:2px solid #28a745"><h3>🎉 Congratulations!</h3><p>Form Accept jhala! Company lavkarach tumhala interview sathi call karel.</p></div>'
    elif s == 'Reject':
        msg = '<div style="background:#f8d7da;color:#721c24;padding:20px;border-radius:10px;margin-top:20px;"><h3>😔 Sorry!</h3><p>Form Reject jhala. Demotivate hou naka!</p></div>'
    else:
        msg = '<div style="background:#fff3cd;color:#856404;padding:20px;border-radius:10px;margin-top:20px;"><h3>⏳ Pending</h3><p>Admin check kartoy.</p></div>'
    return render_template_string(BASE, content=f"<div class=card><h2>Welcome {username}</h2><p style=margin-top:15px>Status: <b class='badge badge-{s.lower()}'>{s}</b></p>{msg}{resume_btn}</div>")

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        if request.form['username']==ADMIN_USER and check_password_hash(ADMIN_PASS_HASH, request.form['password']):
            session['admin']=True;return redirect('/admin/dashboard')
        return render_template_string(BASE, content="<div class=card><h3 style=color:red>Invalid Admin</h3></div>")
    return render_template_string(BASE, content='<div class="form-box"><h2>🔐 Admin Login</h2><form method="POST"><input name="username" placeholder="Admin Username"><input type="password" name="password" placeholder="Password"><button class="btn" style="background:#0b3d91;width:100%">Login</button></form></div>')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'): return redirect('/admin/login')
    with sqlite3.connect(DB, timeout=10) as con:
        cur=con.cursor();cur.execute("SELECT * FROM students ORDER BY id DESC");rows=cur.fetchall()
    tr="".join([f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[3]}</td><td>{r[4]}</td><td><span class='badge badge-{r[9].lower()}'>{r[9]}</span></td><td>{r[10] or '-'}<br><small>{r[11] or ''}</small></td><td><a href=/admin/action/{r[0]}/Accept?company=Google&package=18%20LPA style='background:green;color:white;padding:6px 12px;border-radius:5px;text-decoration:none;margin:2px;display:inline-block'>✓ Accept</a> <a href=/admin/action/{r[0]}/Reject style='background:orange;color:white;padding:6px 12px;border-radius:5px;text-decoration:none;margin:2px;display:inline-block'>✗ Reject</a> <a href=/admin/delete/{r[0]} style='background:red;color:white;padding:6px 12px;border-radius:5px;text-decoration:none;margin:2px;display:inline-block'>🗑️ Delete</a></td></tr>" for r in rows]) or "<tr><td colspan=7>No Students</td></tr>"
    return render_template_string(BASE, content=f"<div class=card><h2>👨‍💼 Admin Dashboard</h2></div><table><tr><th>ID</th><th>Username</th><th>Name</th><th>College</th><th>Status</th><th>Company/Package</th><th>Action</th></tr>{tr}</table>")

@app.route('/admin/action/<int:id>/<status>')
def admin_action(id,status):
    if not session.get('admin'): return redirect('/admin/login')
    with sqlite3.connect(DB, timeout=10) as con:
        cur=con.cursor()
        cur.execute("SELECT username FROM students WHERE id=?",(id,)); username = cur.fetchone()[0]
        if status == 'Accept':
            company = request.args.get('company','Google'); package = request.args.get('package','18 LPA')
            cur.execute("UPDATE students SET status=?,company=?,package=? WHERE id=?",(status,company,package,id))
            cur.execute("INSERT INTO notifications (username,message) VALUES (?,?)",(username, f"🎉 Congratulations! ACCEPTED! Company: {company} | Package: {package}. Interview call yeil lavkarach!"))
        else:
            cur.execute("UPDATE students SET status=? WHERE id=?",(status,id))
            cur.execute("INSERT INTO notifications (username,message) VALUES (?,?)",(username, "❌ Sorry! Application REJECTED. Don't give up! Improve skills and try again."))
        con.commit()
    return redirect('/admin/dashboard')

@app.route('/admin/delete/<int:id>')
def admin_delete(id):
    if not session.get('admin'): return redirect('/admin/login')
    with sqlite3.connect(DB, timeout=10) as con:
        con.execute("DELETE FROM students WHERE id=?",(id,));con.commit()
    return redirect('/admin/dashboard')

if __name__=='__main__':
    app.run(debug=True)