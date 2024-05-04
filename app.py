from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Function to create a connection to the SQLite database
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn
# Create users table (insert this code before any route definitions)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
             (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS blogs
             (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, content TEXT)''')
conn.commit()
conn.close()

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for the login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = cursor.fetchone()
        if user:
            # Valid login, redirect to blogs page
            return redirect(url_for('blogs'))
        else:
            # Invalid login, show error message
            error = 'Invalid username or password. Please try again.'
            return render_template('login.html', error=error)
    return render_template('login.html')

# Route for the registration page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = get_db_connection()
        conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/create_blog', methods=['GET', 'POST'])
def create_blog():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        conn.execute('INSERT INTO blogs (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return redirect(url_for('blogs'))
    return render_template('create_blog.html')

# Route for the blogs page (vulnerable to SQL injection)
@app.route('/blogs')
def blogs():
    id = request.args.get('id', '1')  # Default id is set to '1'
    print("ID:", id)  # For debugging
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM blogs WHERE id = ?', (id,))
    blog = cursor.fetchone()
    conn.close()
    print("Blog:", blog)  # For debugging
    return render_template('blogs.html', blog=blog)





if __name__ == '__main__':
    app.run(debug=True)