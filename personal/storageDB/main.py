from flask import Flask, render_template_string, request, redirect, url_for, flash, session
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DB_HOST = "localhost"
DB_NAME = "people"
DB_USER = "postgres"
DB_PASS = "python"


def connect_db():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn


form_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>User Information Form</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f2f2f5;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }
        .container {
            max-width: 320px;
            width: 100%;
            text-align: center;
        }
        .form-signin {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        .form-signin img {
            max-width: 100px;
            margin-bottom: 20px;
        }
        .form-signin .form-control {
            margin-bottom: 20px;
            height: 45px;
            border-radius: 5px;
            font-size: 16px;
        }
        .form-signin button {
            width: 100%;
            padding: 12px 0;
            font-size: 16px;
            border-radius: 5px;
            background-color: #007bff;
            border-color: #007bff;
        }
        .btn-secondary {
            width: 100%;
            padding: 12px 0;
            font-size: 16px;
            border-radius: 5px;
            margin-top: 10px;
            background-color: #6c757d;
            border-color: #6c757d;
        }
        .alert {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <form class="form-signin" method="post" action="{{ url_for('add_user') }}">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png" alt="Python Logo">
            <h1 class="h3 mb-3 font-weight-normal">User Information Form</h1>
            <div class="form-group">
                <input type="text" class="form-control" id="first_name" name="first_name" placeholder="First Name" required>
            </div>
            <div class="form-group">
                <input type="text" class="form-control" id="last_name" name="last_name" placeholder="Last Name" required>
            </div>
            <div class="form-group">
                <input type="date" class="form-control" id="dob" name="dob" required>
            </div>
            <div class="form-group">
                <input type="tel" class="form-control" id="phone" name="phone" placeholder="Phone Number (optional)">
            </div>
            <div class="form-group">
                <input type="email" class="form-control" id="email" name="email" placeholder="Email Address (optional)">
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-success mt-3">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <a href="{{ url_for('admin') }}" class="btn btn-secondary">Admin Login</a>
    </div>
</body>
</html>
'''

search_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Search User</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
     <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f2f2f5;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }
        .container {
            max-width: 320px;
            width: 100%;
            text-align: center;
        }
        .form-signin {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        .form-signin img {
            max-width: 100px;
            margin-bottom: 20px;
        }
        .form-signin .form-control {
            margin-bottom: 20px;
            height: 45px;
            border-radius: 5px;
            font-size: 16px;
        }
        .form-signin button {
            width: 100%;
            padding: 12px 0;
            font-size: 16px;
            border-radius: 5px;
            background-color: #007bff;
            border-color: #007bff;
        }
        .btn-secondary {
            width: 100%;
            padding: 12px 0;
            font-size: 16px;
            border-radius: 5px;
            margin-top: 10px;
            background-color: #6c757d;
            border-color: #6c757d;
        }
        .alert {
            margin-top: 20px;
        }
        .user-info {
            background: #ffffff;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        .btn-warning, .btn-danger {
            width: 100%;
            padding: 12px 0;
            font-size: 16px;
            border-radius: 5px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <form class="form-signin" method="post">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png" alt="Python Logo">
            <h1 class="h3 mb-3 font-weight-normal">Search User</h1>
            <div class="form-group">
                <input type="text" class="form-control" id="search_query" name="search_query" placeholder="Enter Name, Phone, Email, or DOB" required>
            </div>
            <button type="submit" class="btn btn-primary">Search</button>
        </form>

        {% if users %}
            <table class="table table-striped mt-3">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">First Name</th>
                        <th scope="col">Last Name</th>
                        <th scope="col">Date of Birth</th>
                        <th scope="col">Phone</th>
                        <th scope="col">Email</th>
                        <th scope="col">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {% for user in users %}
                        <tr>
                            <th scope="row">{{ user[0] }}</th>
                            <td>{{ user[1] }}</td>
                            <td>{{ user[2] }}</td>
                            <td>{{ user[3] }}</td>
                            <td>{{ user[4] }}</td>
                            <td>{{ user[5] }}</td>
                            <td>
                                <a href="{{ url_for('edit_user', user_id=user[0]) }}" class="btn btn-warning">Edit</a>
                                <a href="{{ url_for('delete_user', user_id=user[0]) }}" class="btn btn-danger">Delete</a>
                            </td>
                        </tr>
                    {% endfor %}
                </tbody>
            </table>
        {% elif no_result %}
            <div class="alert alert-warning mt-3">No user found with that information.</div>
        {% endif %}

        <a href="{{ url_for('admin_panel') }}" class="btn btn-secondary mt-3">Back to Admin Panel</a>
        <a href="{{ url_for('index') }}" class="btn btn-secondary mt-3">Back to Home</a>
    </div>
</body>
</html>

'''

edit_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Edit User</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f2f2f5;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }
        .container {
            max-width: 320px;
            width: 100%;
            text-align: center;
        }
        .form-signin {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        .form-signin img {
            max-width: 100px;
            margin-bottom: 20px;
        }
        .form-signin .form-control {
            margin-bottom: 20px;
            height: 45px;
            border-radius: 5px;
            font-size: 16px;
        }
        .form-signin button {
            width: 100%;
            padding: 12px 0;
            font-size: 16px;
            border-radius: 5px;
            background-color: #007bff;
            border-color: #007bff;
        }
        .btn-secondary {
            width: 100%;
            padding: 12px 0;
            font-size: 16px;
            border-radius: 5px;
            margin-top: 10px;
            background-color: #6c757d;
            border-color: #6c757d;
        }
        .alert {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <form class="form-signin" method="post" action="{{ url_for('edit_user', user_id=user[0]) }}">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png" alt="Python Logo">
            <h1 class="h3 mb-3 font-weight-normal">Edit User</h1>
            <div class="form-group">
                <input type="text" class="form-control" id="first_name" name="first_name" placeholder="First Name" value="{{ user[1] }}" required>
            </div>
            <div class="form-group">
                <input type="text" class="form-control" id="last_name" name="last_name" placeholder="Last Name" value="{{ user[2] }}" required>
            </div>
            <div class="form-group">
                <input type="date" class="form-control" id="dob" name="dob" value="{{ user[3] }}" required>
            </div>
            <div class="form-group">
                <input type="tel" class="form-control" id="phone" name="phone" placeholder="Phone Number (optional)" value="{{ user[4] }}">
            </div>
            <div class="form-group">
                <input type="email" class="form-control" id="email" name="email" placeholder="Email Address (optional)" value="{{ user[5] }}">
            </div>
            <button type="submit" class="btn btn-primary">Update</button>
        </form>
        <a href="{{ url_for('search') }}" class="btn btn-secondary mt-3">Cancel</a>
        <a href="{{ url_for('admin') }}" class="btn btn-secondary mt-3">Admin Login</a>
    </div>
</body>
</html>
'''

admin_login_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Admin Login</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f2f2f5;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }
        .container {
            max-width: 320px;
            width: 100%;
            text-align: center;
        }
        .form-signin {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        .form-signin img {
            max-width: 100px;
            margin-bottom: 20px;
        }
        .form-signin .form-control {
            margin-bottom: 20px;
            height: 45px;
            border-radius: 5px;
            font-size: 16px;
        }
        .form-signin button {
            width: 100%;
            padding: 12px 0;
            font-size: 16px;
            border-radius: 5px;
            background-color: #007bff;
            border-color: #007bff;
        }
        .btn-secondary {
            width: 100%;
            padding: 12px 0;
            font-size: 16px;
            border-radius: 5px;
            margin-top: 10px;
            background-color: #6c757d;
            border-color: #6c757d;
        }
        .alert {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <form class="form-signin" method="post">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/800px-Python-logo-notext.svg.png" alt="Python Logo">
            <h1 class="h3 mb-3 font-weight-normal">Admin Login</h1>
            <div class="form-group">
                <input type="password" class="form-control" id="password" name="password" placeholder="Password" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
        </form>
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                {% for message in messages %}
                    <div class="alert alert-danger mt-3">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        <a href="{{ url_for('index') }}" class="btn btn-secondary mt-3">Back to Home</a>
    </div>
</body>
</html>
'''

admin_panel_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>Admin Panel</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f2f2f5;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }
        .container {
            max-width: 800px;
            width: 100%;
            text-align: center;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        .btn-secondary {
            width: 100%;
            padding: 12px 0;
            font-size: 16px;
            border-radius: 5px;
            margin-top: 10px;
            background-color: #6c757d;
            border-color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1 class="h3 mb-3 font-weight-normal">Admin Panel</h1>
            {% if users %}
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">First Name</th>
                            <th scope="col">Last Name</th>
                            <th scope="col">Date of Birth</th>
                            <th scope="col">Phone</th>
                            <th scope="col">Email</th>
                            <th scope="col">Actions</th> <!-- Added Actions header -->
                        </tr>
                    </thead>
                    <tbody>
                        {% for user in users %}
                            <tr>
                                <th scope="row">{{ user[0] }}</th>
                                <td>{{ user[1] }}</td>
                                <td>{{ user[2] }}</td>
                                <td>{{ user[3] }}</td>
                                <td>{{ user[4] }}</td>
                                <td>{{ user[5] }}</td>
                                <td>
                                    <a href="{{ url_for('edit_user', user_id=user[0]) }}" class="btn btn-warning">Edit</a>
                                    <a href="{{ url_for('delete_user', user_id=user[0]) }}" class="btn btn-danger">Delete</a>
                                </td> <!-- Added edit and delete buttons -->
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% else %}
                <div class="alert alert-info">No users found.</div>
            {% endif %}
            <a href="{{ url_for('search') }}" class="btn btn-secondary">Search for User</a>
            <a href="{{ url_for('logout') }}" class="btn btn-secondary">Logout</a>
        </div>
    </div>
</body>
</html>

'''

users_template = '''
<!DOCTYPE html>
<html>
<head>
    <title>All Users</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f2f2f5;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }
        .container {
            max-width: 800px;
            width: 100%;
            text-align: center;
        }
        .card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        }
        .btn-secondary {
            width: 100%;
            padding: 12px 0;
            font-size: 16px;
            border-radius: 5px;
            margin-top: 10px;
            background-color: #6c757d;
            border-color: #6c757d;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1 class="h3 mb-3 font-weight-normal">All Users</h1>
            {% if users %}
                <table class="table table-striped">
                    <thead>
                        <tr>
                            <th scope="col">#</th>
                            <th scope="col">First Name</th>
                            <th scope="col">Last Name</th>
                            <th scope="col">Date of Birth</th>
                            <th scope="col">Phone</th>
                            <th scope="col">Email</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for user in users %}
                            <tr>
                                <th scope="row">{{ user[0] }}</th>
                                <td>{{ user[1] }}</td>
                                <td>{{ user[2] }}</td>
                                <td>{{ user[3] }}</td>
                                <td>{{ user[4] }}</td>
                                <td>{{ user[5] }}</td>
                            </tr>
                        {% endfor %}
                    </tbody>
                </table>
            {% else %}
                <div class="alert alert-info">No users found.</div>
            {% endif %}
            <a href="{{ url_for('index') }}" class="btn btn-secondary">Back to Home</a>
        </div>
    </div>
</body>
</html>
'''


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template_string(form_template)


@app.route('/add', methods=['POST'])
def add_user():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        phone = request.form['phone']
        email = request.form['email']

        conn = connect_db()
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO users (first_name, last_name, dob, phone, email) VALUES (%s, %s, %s, %s, %s)",
                        (first_name, last_name, dob, phone, email))
            conn.commit()
            flash('User added successfully!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Error adding user: {e}', 'danger')
        finally:
            cur.close()
            conn.close()

        return redirect(url_for('index'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form['search_query'].strip()

        conn = connect_db()
        cur = conn.cursor()

        try:
            cur.execute(
                "SELECT * FROM users WHERE first_name ILIKE %s OR last_name ILIKE %s OR phone ILIKE %s OR email ILIKE %s OR dob::text ILIKE %s",
                (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%", f"%{search_query}%",
                 f"%{search_query}%"))
            users = cur.fetchall()
            if not users:
                no_result = True
            else:
                no_result = False
            return render_template_string(search_template, users=users, no_result=no_result)
        except Exception as e:
            flash(f'Error searching for user: {e}', 'danger')
        finally:
            cur.close()
            conn.close()

    return render_template_string(search_template)


@app.route('/edit/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        user = cur.fetchone()
        if user is None:
            flash('User not found!', 'danger')
            return render_template_string(admin_panel_template)

        if request.method == 'POST':
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            dob = request.form['dob']
            phone = request.form['phone']
            email = request.form['email']

            cur.execute("UPDATE users SET first_name=%s, last_name=%s, dob=%s, phone=%s, email=%s WHERE id=%s",
                        (first_name, last_name, dob, phone, email, user_id))
            conn.commit()

            return redirect(url_for('search'))  # Redirect to search page after update
    finally:
        cur.close()
        conn.close()

    return render_template_string(edit_template, user=user)


@app.route('/delete/<int:user_id>', methods=['GET'])
def delete_user(user_id):
    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
    except Exception as e:
        flash(f'Error deleting user: {e}', 'danger')
    finally:
        cur.close()
        conn.close()

    return render_template_string(admin_panel_template)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        password = request.form['password']
        if password == 'python':  # Replace with actual secure password check
            session['admin_logged_in'] = True
            return redirect(url_for('admin_panel'))
        else:
            flash('Invalid password!', 'danger')

    return render_template_string(admin_login_template)


@app.route('/admin/panel', methods=['GET'])
def admin_panel():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('admin'))

    conn = connect_db()
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
    except Exception as e:
        flash(f'Error fetching users: {e}', 'danger')
        users = []

    finally:
        cur.close()
        conn.close()

    return render_template_string(admin_panel_template, users=users)


@app.route('/admin/logout', methods=['GET'])
def logout():
    session.pop('admin_logged_in', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)