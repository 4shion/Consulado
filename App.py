# pip3 install flask flask-mysqldb
import base64
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# Creamos un objeto con el nombre app y le pasamos el parámetro name
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Cambia 'password' por tu contraseña real
app.config['MYSQL_DB'] = 'cafe_consulado'  # Verifica el nombre de tu base de datos
app.config['MYSQL_SSL_CA'] = 'C:/xampp/mysql/certs/ca-cert.pem'
app.config['MYSQL_SSL_CERT'] = 'C:/xampp/mysql/certs/server-cert.pem'
app.config['MYSQL_SSL_KEY'] = 'C:/xampp/mysql/certs/server-key.pem'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'
#Creacion de bandera
bandera = False

#Inicio
@app.route('/')
def Index():
    return render_template('index.html')

#Boton Main
@app.route('/swicht_main')
def swicht_main():
    return render_template('index.html')

#Boton Clientes
@app.route('/swicht_clientes')
def swicht_clientes():
    return render_template('clientes.html')

#Boton Empleados
@app.route('/swicht_empleados')
def swicht_empleados():
    return render_template('empleados.html')

#Boton Productos
@app.route('/swicht_productos')
def swicht_productos():
    cur = mysql.connection.cursor()
    cur.execute('''
        SELECT p.idProductos, p.nombre, p.precio, p.cantidad, p.imagen, p.estado, pr.nombre AS proveedor_nombre
        FROM productos p
        JOIN proveedores pr ON p.proveedores_idProveedor = pr.idProveedor
        WHERE p.estado = TRUE
    ''')
    data = cur.fetchall()
    # Codificar solo la imagen en base64
    productos = []
    for row in data:
        # Codificar la imagen en base64 si existe
        imagen_base64 = base64.b64encode(row[4]).decode('utf-8') if row[4] else None
        # Reemplazar la imagen binaria con su versión en base64 en el tuple
        productos.append((row[0], row[1], row[2], row[3], imagen_base64, row[5], row[6]))

    return render_template('productos.html', productos = productos)

#Boton Proveedores
@app.route('/swicht_proveedores')
def swicht_proveedores():
    return render_template('proveedores.html')

#Boton menu
#@app.route('/menu')
#def menu():
#    return

#Agregar productos
@app.route('/agg_productos', methods = ['POST'])
def agg_productos():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        cantidad = request.form['cantidad']
        proveedor = request.form['proveedor']

        # Si quieres manejar una imagen
        if 'imagen' in request.files:
            imagen = request.files['imagen']
            imagen_binaria = imagen.read()
            cur = mysql.connection.cursor()
            cur.execute('''
                            INSERT INTO productos (nombre, precio, cantidad, imagen, estado, proveedores_idProveedor)
                            VALUES (%s, %s, %s, %s, %s, (SELECT idProveedor FROM proveedores WHERE nombre = %s))
                        ''', (nombre, precio, cantidad, imagen_binaria, True, proveedor))
            mysql.connection.commit()
            flash('Producto añadido satisfactoriamente')
            return redirect(url_for('swicht_productos'))
        else:
            flash('No se ha subido ninguna imagen')
            return redirect(url_for('swicht_productos'))

#Eliminar productos
@app.route('/eliminar_productos/<id>')
def delete_productos(id):
    cur = mysql.connection.cursor()
    cur.execute('UPDATE productos SET estado = %s WHERE idProductos = %s', (False, id))
    mysql.connection.commit()
    flash('Producto removido correctamente')
    return redirect(url_for('swicht_productos'))

#Editar productos
@app.route('/editar_productos/<id>')
def editar_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM productos WHERE idProductos = %s', (id))
    data = cur.fetchall()
    global bandera
    bandera = True
    return render_template('productos.html', producto = data[0])

if __name__ == '__main__':
    app.run(port=5000, debug=True)