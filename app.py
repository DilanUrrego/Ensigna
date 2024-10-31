from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from src.controller.users_controller import ControladorUsuarios
from src.controller.products_controller import ControladorProductos
from src.controller.comments_controller import ControladorComentarios


from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash("Por favor, inicia sesión para acceder a esta página", "warning")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Cambia esto por una clave segura

@app.route('/')
def index():
    return render_template('index.html')  # Aquí va la página de inicio, si tienes una

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        correo = request.form['email']
        contrasena = request.form['password']
        
        rol = ControladorUsuarios.verificar_credenciales(correo, contrasena)
        
        if rol:
            session['logged_in'] = True
            session['user_role'] = rol  # Guardar el rol en la sesión
            flash("Inicio de sesión exitoso", "success")
            
            # Redirección basada en el rol del usuario
            if rol == 'administrador':
                return redirect(url_for('administrador'))
            elif rol == 'operario':
                return redirect(url_for('operario'))
        else:
            flash("Usuario o contraseña incorrectos", "danger")
            return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/administrador')
@login_required
def administrador():
    # Aquí puedes agregar el contenido de la página de dashboard
    return render_template('administrador.html')

@app.route('/operario')
@login_required
def operario():
    return render_template('operario.html')

@app.route('/deteccion')
@login_required
def deteccion():
    return render_template('deteccion.html')

@app.route('/crear_producto', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if request.method == 'POST':
        data = request.get_json()
        id = data.get("id")
        tipo_producto = data.get("tipo_producto")
        modelo = data.get("modelo")
        num_serie = data.get("num_serie")

        try:
            # Llamar al método de creación de producto
            success = ControladorProductos.agregar_producto(id, tipo_producto, modelo, num_serie)
            if success:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False, "error": "Error al agregar producto a la base de datos"})
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    return render_template('crear_producto.html')

@app.route('/eliminar_producto', methods=['GET', 'POST'])
@login_required
def eliminar_producto():
    if request.method == 'POST':
        id = request.form.get('product-id')

        try:
            ControladorProductos.eliminar_producto(id)
            flash("Producto eliminado correctamente", "success")
        except Exception as e:
            flash(f"Error al eliminar producto: {e}", "danger")
        
        return redirect(url_for('administrador'))  # Redirige de nuevo a la página del operario
    return render_template('eliminar_producto.html')


@app.route('/crear_reporte', methods=['GET', 'POST'])
@login_required
def crear_reporte():
    if request.method == 'POST':
        id = request.form.get('product-id')

        try:
            ControladorProductos.eliminar_producto(id)
            flash("Producto eliminado correctamente", "success")
        except Exception as e:
            flash(f"Error al eliminar producto: {e}", "danger")
        
        return redirect(url_for('administrador'))  # Redirige de nuevo a la página del operario
    return render_template('crear_reporte.html')

@app.route('/actualizar_producto', methods=['GET', 'POST'])
@login_required
def actualizar_producto():
    if request.method == 'POST':
        product_id = request.form.get('product-id')
        tipo_producto = request.form.get('tipo-producto')
        modelo = request.form.get('modelo')
        num_serie = request.form.get('num-serie')

        # Construir un diccionario solo con los campos no vacíos
        update_data = {}
        if tipo_producto:
            update_data['tipo_producto'] = tipo_producto
        if modelo:
            update_data['modelo'] = modelo
        if num_serie:
            update_data['num_serie'] = num_serie

        # Verificar que haya al menos un campo para actualizar
        if not update_data:
            flash("Por favor, complete al menos un campo para actualizar.", "warning")
            return redirect(url_for('actualizar_producto'))

        # Intentar actualizar el producto
        try:
            ControladorProductos.actualizar_producto(product_id, update_data)
            flash("Producto actualizado correctamente.", "success")
        except Exception as e:
            flash(f"Error al actualizar el producto: {e}", "danger")
        
        return redirect(url_for('administrador'))  # Redirige de nuevo a la página del administrador
    
    return render_template('actualizar_producto.html')

@app.route('/obtener_producto', methods=['POST'])
def obtener_producto():
    data = request.get_json()
    id_producto = data.get('id_producto')
    
    # Obtener los detalles del producto
    producto = ControladorProductos.obtener_producto_por_id(id_producto)
    
    # Obtener los comentarios del producto
    comentarios = ControladorComentarios.obtener_comentarios_por_producto(id_producto)
    
    if producto:
        # Devolver los datos en formato JSON
        return jsonify({
            'modelo': producto['modelo'],
            'num_serie': producto['num_serie'],
            'tipo_producto': producto['tipo_producto'],
            'defecto': producto['defecto'],
            'comentarios': comentarios
        })
    else:
        return jsonify({'error': 'Producto no encontrado'}), 404



@app.route('/logout')
def logout():
    session.pop('logged_in', None)  # Elimina el estado de inicio de sesión
    flash("Sesión cerrada con éxito", "success")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
