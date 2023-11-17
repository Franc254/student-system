from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
import re

app = Flask(__name__)

app.secret_key = 'mediocrity'

dbconfig = {'host': '127.0.0.1',
            'user': 'root',
            'password': '',
            'database': 'user_system',}

conn = mysql.connector.connect(**dbconfig)
cursor = conn.cursor()

@app.route('/')
@app.route('/home')
def home():
    # Check if the user is logged in
    if 'loggedin' in session:
        # User is logged in
        return render_template('index.html', username=session['username'])
    # User is not logged in
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong
    msg = ''
    # Check if "username", "password" and "email" POST requests exist
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']    
        password = request.form['password']
        email = request.form['email']
        # Check if account exists
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account :
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesn't exist, and the form data is valid, insert the new user
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            conn.commit()
            msg = 'You have succesfully registered!'

    elif request.method == 'POST':
        # Form is empty
        msg = 'Please fill out the form!'
    return render_template('register.html', msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output a message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist 
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table
        if account:
            # Create session data
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            #Account doesn't exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with the message (if any)
    return render_template('login.html', msg=msg)

   
@app.route('/logout')       
def logout():
    # Remove session data
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    # Check if the user is logged in
    if 'loggedin' in session:
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not logged in
    return redirect(url_for('login'))

@app.route('/units', methods=['GET', 'POST'])
def units():
    if request.method == 'POST' and 'year' in request.form:
        year = request.form['year']
        if year == 1:
            return render_template('year1_semesters.html')
        elif year == 2:
            return render_template('year2_semesters.html')
        elif year == 3:
            return render_template('year3_semesters.html')
        elif year == 4:
            return render_template('year4-semesters.html')
    return render_template('units.html')

@app.route('/year1_semesters', methods=['POST', 'GET'])
def year1_semesters():
    return render_template('year1_semesters.html')

@app.route('/year2_semesters', methods=['POST', 'GET'])
def year2_semesters():
    return render_template('year2_semesters.html')

@app.route('/year3_semesters', methods=['POST', 'GET'])
def year3_semesters():
    return render_template('year3_semesters.html')

@app.route('/year4_semesters', methods=['POST', 'GET'])
def year4_semesters():
    return render_template('year4_semesters.html')

@app.route('/register_y1_1', methods=['POST','GET'])
def register_y1_1():
    if request.method == 'POST':
        hiv = request.form['hiv']
        hiv_code = 'CSC 101'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (hiv_code, hiv))
        conn.commit()
        communication = request.form['communication']
        communication_code = 'CSC 102'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (communication_code, communication))
        conn.commit()
        programming = request.form['programming']
        programming_code = 'SIT 111'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (programming_code, programming))
        conn.commit()
        computers = request.form['computers']
        computers_code = 'SIT 112'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (computers_code, computers))
        conn.commit()
        return redirect(url_for('register_y1_1'))
    return render_template('year1_semesters.html')

@app.route('/register_y1_2', methods=['POST','GET'])
def register_y1_2():
    if request.method == 'POST':
        calculus = request.form['calculus']
        calculus_code = 'CSC 103'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (calculus_code, calculus))
        conn.commit()
        discrete = request.form['discrete']
        discrete_code = 'CSC 104'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (discrete_code, discrete))
        conn.commit()
        html = request.form['html']
        html_code = 'SIT 113'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (html_code, html))
        conn.commit()
        database = request.form['database']
        database_code = 'SIT 114'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (database_code, database))
        conn.commit()
        return redirect(url_for('register_y1_2'))
    return render_template('year1_semesters.html')

@app.route('/register_y2_1', methods=['POST','GET'])
def register_y2_1():
    if request.method == 'POST':
        cplus = request.form['cplus']
        cplus_code = 'CSC 201'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (cplus_code, cplus))
        conn.commit()
        javascript = request.form['javascript']
        javascript_code = 'CSC 202'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (javascript_code, javascript))
        conn.commit()
        css = request.form['css']
        css_code = 'SIT 211'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (css_code, css))
        conn.commit()
        ethics = request.form['ethics']
        ethics_code = 'SIT 212'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (ethics_code, ethics))
        conn.commit()
        return redirect(url_for('register_y2_1'))
    return render_template('year2_semesters.html')

@app.route('/register_y2_2', methods=['POST','GET'])
def register_y2_2():
    if request.method == 'POST':
        os = request.form['os']
        os_code = 'CSC 203'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (os_code, os))
        conn.commit()
        distributed = request.form['distributed']
        distributed_code = 'CSC 204'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (distributed_code, distributed))
        conn.commit()
        networking = request.form['networking']
        networking_code = 'SIT 213'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (networking_code, networking))
        conn.commit()
        ims = request.form['ims']
        ims_code = 'SIT 214'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (ims_code, ims))
        conn.commit()
        return redirect(url_for('register_y2_2'))
    return render_template('year2_semesters.html')


@app.route('/register_y3_1', methods=['POST','GET'])
def register_y3_1():
    if request.method == 'POST':
        system = request.form['system']
        system_code = 'CSC 301'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (system_code, system))
        conn.commit()
        software = request.form['software']
        software_code = 'CSC 302'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (software_code, software))
        conn.commit()
        scripting = request.form['scripting']
        scripting_code = 'SIT 311'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (scripting_code, scripting))
        conn.commit()
        security = request.form['security']
        security_code = 'SIT 312'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (security_code, security))
        conn.commit()
        return redirect(url_for('register_y3_1'))
    return render_template('year3_semesters.html')

@app.route('/register_y3_2', methods=['POST','GET'])
def register_y3_2():
    if request.method == 'POST':
        admin = request.form['admin']
        admin_code = 'CSC 303'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (admin_code, admin))
        conn.commit()
        research = request.form['research']
        research_code = 'CSC 304'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (research_code, research))
        conn.commit()
        ai = request.form['ai']
        ai_code = 'SIT 313'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (ai_code, ai))
        conn.commit()
        mobile = request.form['mobile']
        mobile_code = 'SIT 314'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (mobile_code, mobile))
        conn.commit()
        return redirect(url_for('register_y3_2'))
    return render_template('year3_semesters.html')


@app.route('/register_y4_1', methods=['POST','GET'])
def register_y4_1():
    if request.method == 'POST':
        graphics = request.form['graphics']
        graphics_code = 'CSC 401'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (graphics_code, graphics))
        conn.commit()
        iot = request.form['iot']
        iot_code = 'CSC 402'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (iot_code, iot))
        conn.commit()
        erp = request.form['erp']
        erp_code = 'SIT 411'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (erp_code, erp))
        conn.commit()
        apps = request.form['apps']
        apps_code = 'SIT 412'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (apps_code, apps))
        conn.commit()
        return redirect(url_for('register_y4_1'))
    return render_template('year4_semesters.html')

@app.route('/register_y4_2', methods=['POST','GET'])
def register_y4_2():
    if request.method == 'POST':
        project = request.form['project']
        project_code = 'CSC 403'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (project_code, project))
        conn.commit()
        group = request.form['group']
        group_code = 'CSC 404'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (group_code, group))
        conn.commit()
        cc = request.form['cc']
        cc_code = 'SIT 413'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (cc_code, cc))
        conn.commit()
        multimedia = request.form['multimedia']
        multimedia_code = 'SIT 414'
        cursor.execute('INSERT INTO units VALUES (%s, %s)', (multimedia_code, multimedia))
        conn.commit()
        return redirect(url_for('register_y4_2'))
    return render_template('year4_semesters.html')

@app.route('/view_units', methods=['GET', 'POST'])
def view_units():
    cursor.execute('SELECT * FROM units')
    units = cursor.fetchall()
    
    return render_template('view_units.html', units=units)

if __name__ == "__main__":
    app.run(debug=True)