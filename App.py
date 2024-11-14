# pip3 install flask flask-mysqldb
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# Creamos un objeto con el nombre app y le pasamos el parámetro name
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Cambia 'password' por tu contraseña real
app.config['MYSQL_DB'] = 'flaskcontacts'  # Verifica el nombre de tu base de datos
app.config['MYSQL_SSL_CA'] = 'C:/xampp/mysql/certs/ca-cert.pem'
app.config['MYSQL_SSL_CERT'] = 'C:/xampp/mysql/certs/server-cert.pem'
app.config['MYSQL_SSL_KEY'] = 'C:/xampp/mysql/certs/server-key.pem'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/swicht_main')
def swicht_main():
    return render_template('index.html')

@app.route('/swicht_clientes')
def swicht_clientes():
    return render_template('clientes.html')

@app.route('/swicht_empleados')
def swicht_empleados():
    return render_template('empleados.html')

@app.route('/swicht_productos')
def swicht_productos():
    return render_template('productos.html')

@app.route('/swicht_proveedores')
def swicht_proveedores():
    return render_template('proveedores.html')

#@app.route('/menu')
#def menu():
#    return

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)', 
        (fullname, phone, email))
        mysql.connection.commit()
        flash('Contacto añadido satisfactoriamente')
        return redirect(url_for('Index'))  # Redirige a la página principal

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.form == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE contacts SET fullname = %s, email = %s, phone = %s WHERE id = %s', (fullname, email, phone, id))
        flash('Contacto actualizado')
        mysql.connection.commit()
        return render_template(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto removido correctamente')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port=5000, debug=True)
