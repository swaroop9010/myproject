from bottle import Bottle, template, request, redirect, run
import sqlite3

app = Bottle()

# SQLite Database Initialization
conn = sqlite3.connect('cars.db')
cursor = conn.cursor()

# Create cars table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS cars (
        car_id INTEGER PRIMARY KEY AUTOINCREMENT,
        car_name TEXT NOT NULL,
        car_model TEXT NOT NULL
    )
''')

# Create manufacturers table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS manufacturers (
        manufacturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        manufacturer_name TEXT NOT NULL
    )
''')

conn.commit()

# Routes

# Cars CRUD
@app.route('/')
def index():
    return template('index')

@app.route('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='./static')

@app.route('/cars')
def cars():
    cursor.execute("SELECT * FROM cars")
    result = cursor.fetchall()
    return template('cars', rows=result)

@app.route('/cars/add', method='GET')
def add_car_form():
    return template('add_car')

@app.route('/cars/add', method='POST')
def add_car():
    car_name = request.forms.get('car_name')
    car_model = request.forms.get('car_model')

    cursor.execute("INSERT INTO cars (car_name, car_model) VALUES (?, ?)", (car_name, car_model))
    conn.commit()

    redirect('/cars')

@app.route('/cars/edit/<car_id:int>', method='GET')
def edit_car_form(car_id):
    cursor.execute("SELECT * FROM cars WHERE car_id=?", (car_id,))
    car = cursor.fetchone()
    return template('edit_car', car=car)

@app.route('/cars/edit/<car_id:int>', method='POST')
def edit_car(car_id):
    car_name = request.forms.get('car_name')
    car_model = request.forms.get('car_model')

    cursor.execute("UPDATE cars SET car_name=?, car_model=? WHERE car_id=?", (car_name, car_model, car_id))
    conn.commit()

    redirect('/cars')

@app.route('/cars/delete/<car_id:int>')
def delete_car(car_id):
    cursor.execute("DELETE FROM cars WHERE car_id=?", (car_id,))
    conn.commit()

    redirect('/cars')

# Manufacturers CRUD

@app.route('/manufacturers')
def manufacturers():
    cursor.execute("SELECT * FROM manufacturers")
    result = cursor.fetchall()
    return template('manufacturers', rows=result)

@app.route('/manufacturers/add', method='GET')
def add_manufacturer_form():
    return template('add_manufacturer')

@app.route('/manufacturers/add', method='POST')
def add_manufacturer():
    manufacturer_name = request.forms.get('manufacturer_name')

    cursor.execute("INSERT INTO manufacturers (manufacturer_name) VALUES (?)", (manufacturer_name,))
    conn.commit()

    redirect('/manufacturers')

@app.route('/manufacturers/edit/<manufacturer_id:int>', method='GET')
def edit_manufacturer_form(manufacturer_id):
    cursor.execute("SELECT * FROM manufacturers WHERE manufacturer_id=?", (manufacturer_id,))
    manufacturer = cursor.fetchone()
    return template('edit_manufacturer', manufacturer=manufacturer)

@app.route('/manufacturers/edit/<manufacturer_id:int>', method='POST')
def edit_manufacturer(manufacturer_id):
    manufacturer_name = request.forms.get('manufacturer_name')

    cursor.execute("UPDATE manufacturers SET manufacturer_name=? WHERE manufacturer_id=?", (manufacturer_name, manufacturer_id))
    conn.commit()

    redirect('/manufacturers')

@app.route('/manufacturers/delete/<manufacturer_id:int>')
def delete_manufacturer(manufacturer_id):
    cursor.execute("DELETE FROM manufacturers WHERE manufacturer_id=?", (manufacturer_id,))
    conn.commit()

    redirect('/manufacturers')

# Search option for cars
@app.route('/cars/search', method='POST')
def search_cars():
    search_term = request.forms.get('search_term')
    cursor.execute("SELECT * FROM cars WHERE car_name LIKE ? OR car_model LIKE ?", ('%' + search_term + '%', '%' + search_term + '%'))
    result = cursor.fetchall()
    return template('cars', rows=result)

# Static Routes
# ... (existing code)

# Run the application
if __name__ == '__main__':
    run(app, host='localhost', port=8084, debug=True)
