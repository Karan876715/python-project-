from flask import Flask, request, redirect, url_for, session, render_template_string
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(_name_)
app.secret_key = "karan_final_2026_v3"
DB = "placement.db"

COMPANIES_100 = ["Google","Microsoft","Amazon","Infosys","TCS","Wipro","Meta","Apple","Netflix","Adobe","Goldman Sachs","Flipkart","Samsung","Intel","IBM","Oracle","Deloitte","Accenture","Capgemini","Cognizant","HCL","Tech Mahindra","L&T","BYJU'S","Paytm","Zomato","Swiggy","Ola","Uber","Zoho","PhonePe","Razorpay","CRED","Meesho","Unacademy","PhysicsWallah","JP Morgan","Morgan Stanley","Deutsche Bank","HSBC","Qualcomm","Nvidia","Cisco","HP","Dell","Tata Motors","Mahindra","Bajaj Auto","Reliance Jio","Airtel","ISRO","DRDO","BHEL","ONGC","Mindtree","Mphasis","Hexaware","Persistent","KPIT","Siemens","Tesla","SpaceX","Twitter","LinkedIn","Salesforce","SAP","Atlassian","Walmart","PayPal","Stripe","Coinbase","Dream11","Nykaa","Boat","OnePlus","Xiaomi","Realme","Vivo","Nokia","Bosch","Adani","Tata Steel","JSW","Maruti","Hyundai","Kia","Honda","Yamaha","Bajaj Finserv","ICICI Bank","HDFC Bank","Axis Bank","SBI","Kotak","ZScaler","ServiceNow"]

ADMIN_USER = "admin_karan"
ADMIN_PASS_HASH = generate_password_hash("Karan@123")

def init_db():
    con=sqlite3.connect(DB)
    cur=con.cursor()
    cur.execute("DROP TABLE IF EXISTS students")
    cur.execute("DROP TABLE IF EXISTS companies")
    cur.execute("CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT, name TEXT, college TEXT, address TEXT, phone TEXT, enrollment TEXT, email TEXT, status TEXT DEFAULT 'Pending')")
    cur.execute("CREATE TABLE companies (id INTEGER PRIMARY KEY, name TEXT, info TEXT)")
    for i,nm in enumerate(COMPANIES_100,1):
        cur.execute("INSERT INTO companies VALUES (?,?,?)",(i,nm,f"{8+i%25} LPA"))
    con.commit()
    con.close()

init_db()

BASE = """<!DOCTYPE html><html><head><title>IITPlacements</title>
<style>*{margin:0;padding:0;box-sizing:border-box;font-family:Arial}body{display:flex;flex-direction:column;min-height:100vh;background:#0e4fa3}.wrapper{display:flex;flex:1}.sidebar{width:230px;background:#0b3d91;color:#fff;padding:15px;position:fixed;height:100vh;overflow-y:auto}.sidebar h3{color:orange;margin-bottom:15px;text-align:center}.sidebar a{display:block;color:#fff;text-decoration:none;padding:11px;margin:5px 0;border-radius:6px;font-size:14px}.sidebar a:hover{background:#1a5ed7}.main{margin-left:230px;padding:20px;width:100%;padding-bottom:60px}.card{background:#fff;padding:25px;border-radius:15px;text-align:center;margin-bottom:20px;box-shadow:0 4px 10px #0002}.comp-btn{padding:8px 16px;margin:5px;border:none;border-radius:6px;color:#fff;font-weight:bold}.blue{background:#2196F3}.orange{background:#FF9800}.green{background:#2e7d32}.info-box{background:#fff;padding:20px;border-radius:12px;text-align:left;line-height:1.8}.btn{padding:10px 18px;border:none;border-radius:6px;color:#fff;cursor:pointer}.form-box{background:#fff;padding:20px;border-radius:12px;max-width:600px;margin:auto;text-align:left}input,textarea{width:100%;padding:10px;margin:6px 0 12px;border:1px solid #ccc;border-radius:6px}table{width:100%;border-collapse:collapse;background:#fff;border-radius:10px;overflow:hidden}th,td{padding:10px;border-bottom:1px solid #ddd;font-size:13px}th{background:#0b3d91;color:#fff}.footer{background:#081f4d;color:white;text-align:center;padding:15px;margin-left:230px;font-size:14px;letter-spacing:0.5px}
</style></head>
<body><div class="wrapper"><div class="sidebar"><h3>IITPlacements</h3>
<a href="/">Home</a><a href="/register">Student Form</a><a href="/login">Student Login</a><a href="/admin/login">Admin Panel</a><a href="/list">List</a><a href="/companies">Companies (100+)</a><a href="/contact">Contact</a><a href="/">Home Page</a>
</div><div class="main">{{content|safe}}</div></div><div class="footer">IIT PLACEMENTS 2026. Developed by KARAN DIPAK SHINDE.</div></body></html>"""

@app.route('/')
def home():
    c50="".join([f'<span style="display:inline-block;background:#e3f2fd;margin:4px;padding:6px 10px;border-radius:15px;font-size:12px">{x}</span>' for x in COMPANIES_100[:50]])
    return render_template_string(BASE, content=f'<div class="card"><h1 style="color:#0b3d91">IITPlacements</h1><p>Connecting <span style="background:yellow">IIT Students</span> with <span style="background:yellow">Top Companies</span></p><br><button class="comp-btn blue">GOOGLE</button><button class="comp-btn blue">MICROSOFT</button><button class="comp-btn orange">AMAZON</button><br><br><a href="/register"><button class="btn green">Student Registration</button></a> <a href="/login"><button class="btn blue">Student Login</button></a></div><div class="card" style="text-align:left"><h3>50+ Companies on Home</h3><div style="margin-top:10px">{c50}</div><br><a href="/companies"><button class="btn" style="background:#0b3d91">View 100+ Companies</button></a></div><div class="info-box"><h3>IIT Placement Info</h3><p>Best portal for IIT students. Registration nanter Admin Accept karel.</p><p>Package 8-45 LPA. 100% Placement Support.</p></div>')

@app.route('/companies')
def companies_page():
    con=sqlite3.connect(DB);cur=con.cursor();cur.execute("SELECT * FROM companies");rows=cur.fetchall();con.close()
    html="".join([f'<span style="display:inline-block;background:#fff;margin:5px;padding:8px 12px;border-radius:8px">{r[1]} - {r[2]}</span>' for r in rows])
    return render_template_string(BASE, content=f"<div class=card style=text-align:left><h2>100+ Companies</h2><div>{html}</div></div>")

@app.route('/list')
def list_page():
    con=sqlite3.connect(DB);cur=con.cursor();cur.execute("SELECT username,college,status FROM students");rows=cur.fetchall();con.close()
    tr="".join([f"<tr><td>{i+1}</td><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td></tr>" for i,r in enumerate(rows)]) or "<tr><td colspan=4>No Data</td></tr>"
    return render_template_string(BASE, content=f"<div class=card><h2>Registered Usernames</h2></div><table><tr><th>#</th><th>Username</th><th>College</th><th>Status</th></tr>{tr}</table><br><a href='/'><button class=btn style=background:#0b3d91>Home Page</button></a>")

@app.route('/contact')
def contact():
    top4 = "".join([f'<p> {c} - Top Recruiter</p>' for c in COMPANIES_100[:4]])
    content = f'''
    <div class="card" style="text-align:left; max-width:600px; margin:auto">
        <h2 style="text-align:center; color:#0b3d91">IIT PLACEMENTS</h2>
        <hr style="margin:15px 0">
        <h3>Top 4 Companies:</h3>
        <div style="margin:10px 0; background:#e3f2fd; padding:15px; border-radius:8px">{top4}</div>
        <hr style="margin:15px 0">
        <p><b>Phone Number:</b> 8767156551, 9960978900</p>
        <p><b>Gmail:</b> shindekarandeepak@gmail.com</p>
        <br>
        <p style="background:#fff3cd; padding:10px; border-radius:6px"><b>Admin:</b> KARAN DIPAK SHINDE - For any query contact on above numbers.</p>
    </div>
    '''
    return render_template_string(BASE, content=content)

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            con=sqlite3.connect(DB)
            con.execute("INSERT INTO students (username,password,name,college,address,phone,enrollment,email) VALUES (?,?,?,?,?,?,?,?)",(request.form['username'],generate_password_hash(request.form['password']),request.form['name'],request.form['college'],request.form['address'],request.form['phone'],request.form['enrollment'],request.form['email']))
            con.commit();con.close()
            return redirect(url_for('thankyou', username=request.form['username']))
        except:
            return render_template_string(BASE, content="<div class=card><h3 style=color:red>Username already exists</h3></div>")
    return render_template_string(BASE, content='<div class="form-box"><h2>Student Form</h2><form method="POST"><input name="username" placeholder="Username" required><input type="password" name="password" placeholder="Password" required><input name="name" placeholder="Full Name" required><input name="college" placeholder="College Name" required><textarea name="address" placeholder="Address"></textarea><input name="phone" placeholder="Phone"><input name="enrollment" placeholder="Enrollment No"><input name="email" type="email" placeholder="Gmail"><button class="btn green" style="width:100%">Submit</button></form></div>')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        con=sqlite3.connect(DB);cur=con.cursor();cur.execute("SELECT password FROM students WHERE username=?",(request.form['username'],));row=cur.fetchone();con.close()
        if row and check_password_hash(row[0], request.form['password']):
            return redirect(url_for('thankyou', username=request.form['username']))
        return render_template_string(BASE, content="<div class=card><h3 style=color:red>Wrong Password</h3></div>")
    return render_template_string(BASE, content='<div class="form-box"><h2>Student Login</h2><form method="POST"><input name="username" placeholder="Username" required><input type="password" name="password" placeholder="Password" required><button class="btn blue" style="width:100%">Login</button></form></div>')

@app.route('/thankyou/<username>')
def thankyou(username):
    con=sqlite3.connect(DB);cur=con.cursor();cur.execute("SELECT status FROM students WHERE username=?",(username,));r=cur.fetchone();con.close();s=r[0] if r else 'Pending'
    if s == 'Accept':
        msg = '<div style="background:#d4edda;color:#155724;padding:15px;border-radius:8px;margin-top:15px;border:1px solid #c3e6cb"><b>Congratulations!</b><br>Tumcha form Accept jhala aahe! Company lavkarach tumhala interview sathi call karel. All the best!</div>'
    elif s == 'Reject':
        msg = '<div style="background:#f8d7da;color:#721c24;padding:15px;border-radius:8px;margin-top:15px;"><b>Sorry!</b> Tumcha form Reject jhala aahe. Pudchya veli prayatna kara.</div>'
    else:
        msg = '<div style="background:#fff3cd;color:#856404;padding:15px;border-radius:8px;margin-top:15px;">Pending - Admin tumcha form check kartoy.</div>'
    return render_template_string(BASE, content=f"<div class=card><h2>Thanks for visit IIT Placement Portal</h2><h3>Welcome {username}</h3><div style=display:flex;gap:15px;margin-top:20px><div style=flex:1;padding:25px;background:#ffcdd2;border-radius:10px;border:2px solid red>REJECT</div><div style=flex:1;padding:25px;background:#c8e6c9;border-radius:10px;border:2px solid green>ACCEPT</div></div><p style=margin-top:15px>Status: <b>{s}</b></p>{msg}</div>")

@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method=='POST':
        if request.form['username']==ADMIN_USER and check_password_hash(ADMIN_PASS_HASH, request.form['password']):
            session['admin']=True;return redirect('/admin/dashboard')
        return render_template_string(BASE, content="<div class=card><h3 style=color:red>Invalid Admin</h3></div>")
    return render_template_string(BASE, content='<div class="form-box"><h2>Admin Login (Hidden)</h2><form method="POST"><input name="username" placeholder="Admin Username"><input type="password" name="password" placeholder="Admin Password"><button class="btn" style="background:#0b3d91;width:100%">Login</button></form></div>')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'): return redirect('/admin/login')
    con=sqlite3.connect(DB);cur=con.cursor();cur.execute("SELECT * FROM students");rows=cur.fetchall();con.close()
    tr="".join([f"<tr><td>{r[0]}</td><td>{r[1]}</td><td>{r[3]}</td><td>{r[9]}</td><td><a href=/admin/action/{r[0]}/Accept style='background:green;color:white;padding:4px 8px;border-radius:4px;text-decoration:none'>Accept</a> <a href=/admin/action/{r[0]}/Reject style='background:orange;color:white;padding:4px 8px;border-radius:4px;text-decoration:none'>Reject</a> <a href=/admin/delete/{r[0]} style='background:red;color:white;padding:4px 8px;border-radius:4px;text-decoration:none'>Delete</a></td></tr>" for r in rows]) or "<tr><td colspan=5>No Students</td></tr>"
    return render_template_string(BASE, content=f"<div class=card><h2>Admin - All Student Forms</h2></div><table><tr><th>ID</th><th>Username</th><th>Name</th><th>Status</th><th>Action</th></tr>{tr}</table>")

@app.route('/admin/action/<int:id>/<status>')
def admin_action(id,status):
    con=sqlite3.connect(DB);con.execute("UPDATE students SET status=? WHERE id=?",(status,id));con.commit();con.close();return redirect('/admin/dashboard')

@app.route('/admin/delete/<int:id>')
def admin_delete(id):
    con=sqlite3.connect(DB);con.execute("DELETE FROM students WHERE id=?",(id,));con.commit();con.close();return redirect('/admin/dashboard')

if _name=='main_':
    app.run(debug=True)