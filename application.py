from bottle import Bottle, template, request, redirect, run
import sqlite3

app = Bottle()

# SQLite Database Initialization
conn = sqlite3.connect('industries.db')
cursor = conn.cursor()

# Create industries table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS industries (
        industry_id INTEGER PRIMARY KEY AUTOINCREMENT,
        industry_name TEXT NOT NULL,
        industry_model TEXT NOT NULL
    )
''')

# Create divisions table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS divisions (
        division_id INTEGER PRIMARY KEY AUTOINCREMENT,
        division_name TEXT NOT NULL
    )
''')

conn.commit()

# Routes

# Industries CRUD
@app.route('/')
def index():
    return template('index')

@app.route('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='./static')

@app.route('/industries')
def industries():
    cursor.execute("SELECT * FROM industries")
    result = cursor.fetchall()
    return template('industries', rows=result)

@app.route('/industries/add', method='GET')
def add_industry_form():
    return template('add_industry')

@app.route('/industries/add', method='POST')
def add_industry():
    industry_name = request.forms.get('industry_name')
    industry_model = request.forms.get('industry_model')

    cursor.execute("INSERT INTO industries (industry_name, industry_model) VALUES (?, ?)", (industry_name, industry_model))
    conn.commit()

    redirect('/industries')

@app.route('/industries/edit/<industry_id:int>', method='GET')
def edit_industry_form(industry_id):
    cursor.execute("SELECT * FROM industries WHERE industry_id=?", (industry_id,))
    industry = cursor.fetchone()
    return template('edit_industry', industry=industry)

@app.route('/industries/edit/<industry_id:int>', method='POST')
def edit_industry(industry_id):
    industry_name = request.forms.get('industry_name')
    industry_model = request.forms.get('industry_model')

    cursor.execute("UPDATE industries SET industry_name=?, industry_model=? WHERE industry_id=?", (industry_name, industry_model, industry_id))
    conn.commit()

    redirect('/industries')

@app.route('/industries/delete/<industry_id:int>')
def delete_industry(industry_id):
    cursor.execute("DELETE FROM industries WHERE industry_id=?", (industry_id,))
    conn.commit()

    redirect('/industries')

# Divisions CRUD

@app.route('/divisions')
def divisions():
    cursor.execute("SELECT * FROM divisions")
    result = cursor.fetchall()
    return template('divisions', rows=result)

@app.route('/divisions/add', method='GET')
def add_division_form():
    return template('add_division')

@app.route('/divisions/add', method='POST')
def add_division():
    division_name = request.forms.get('division_name')

    cursor.execute("INSERT INTO divisions (division_name) VALUES (?)", (division_name,))
    conn.commit()

    redirect('/divisions')

@app.route('/divisions/edit/<division_id:int>', method='GET')
def edit_division_form(division_id):
    cursor.execute("SELECT * FROM divisions WHERE division_id=?", (division_id,))
    division = cursor.fetchone()
    return template('edit_division', division=division)

@app.route('/divisions/edit/<division_id:int>', method='POST')
def edit_division(division_id):
    division_name = request.forms.get('division_name')

    cursor.execute("UPDATE divisions SET division_name=? WHERE division_id=?", (division_name, division_id))
    conn.commit()

    redirect('/divisions')

@app.route('/divisions/delete/<division_id:int>')
def delete_division(division_id):
    cursor.execute("DELETE FROM divisions WHERE division_id=?", (division_id,))
    conn.commit()

    redirect('/divisions')

# Search option for industries
@app.route('/industries/search', method='POST')
def search_industries():
    search_term = request.forms.get('search_term')
    cursor.execute("SELECT * FROM industries WHERE industry_name LIKE ? OR industry_model LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
    result = cursor.fetchall()
    return template('industries', rows=result)

# Static Routes
# ... (existing code)

# Run the application
if __name__ == '__main__':
    run(app, host='localhost', port=8084, debug=True)
