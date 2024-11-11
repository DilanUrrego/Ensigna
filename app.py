from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from src.controller.users_controller import ControladorUsuarios
from src.controller.products_controller import ControladorProductos
from src.controller.comments_controller import ControladorComentarios
from src.controller.filtered_controller import ControladorFiltrado
from src.controller.reports_controller import ControladorReportes
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
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            correo = request.form['email']
            contrasena = request.form['password']
            
            # Verificar credenciales
            rol = ControladorUsuarios.verificar_credenciales(correo, contrasena)
            
            if rol:
                session['logged_in'] = True
                session['user_role'] = rol
                session['user_email'] = correo
                flash("Inicio de sesión exitoso", "success")
                
                # Redirigir dependiendo del rol
                if rol.lower() == 'administrador':
                    return redirect(url_for('administrador'))
                elif rol.lower() == 'operario':
                    return redirect(url_for('operario'))
            else:
                flash("Usuario o contraseña incorrectos", "danger")
        
        except Exception as e:
            print(f"Error en login: {str(e)}")
            flash("Error en el inicio de sesión", "danger")
        
        return redirect(url_for('login'))
    
    return render_template('login.html')

@app.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        try:
            nombre = request.form['nombre']
            correo = request.form['correo']
            contrasena = request.form['contrasena']
            rol = request.form['rol']
            
            resultado = ControladorUsuarios.registrar_usuario(nombre, correo, contrasena, rol)
            
            if resultado:
                return jsonify({
                    "success": True,
                    "mensaje": "Usuario creado exitosamente"
                })
            else:
                return jsonify({
                    "success": False,
                    "error": "No se pudo crear el usuario"
                })
                
        except Exception as e:
            print(f"Error en crear_usuario: {str(e)}")
            return jsonify({
                "success": False,
                "error": str(e)
            })

    return render_template('crear_usuario.html')

@app.route('/administrador')
@login_required
def administrador():
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
            success = ControladorProductos.agregar_producto(id, tipo_producto, modelo, num_serie)
            if success:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False, "error": "Error al agregar producto"})
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
        
        return redirect(url_for('administrador'))
    return render_template('eliminar_producto.html')

@app.route('/crear_reporte', methods=['GET', 'POST'])
@login_required
def crear_reporte():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            id_producto = request.form.get('idProducto')
            nombre_producto = request.form.get('nombreProducto')
            tipo_defecto = request.form.get('tipoDefecto')
            descripcion = request.form.get('descripcion')
            estado = request.form.get('estadoProducto')
            
            # Crear el reporte
            resultado = ControladorReportes.crear_reporte(
                id_producto, 
                nombre_producto, 
                tipo_defecto, 
                descripcion, 
                estado
            )
            
            if resultado["success"]:
                return jsonify({
                    "success": True,
                    "mensaje": "Reporte creado exitosamente",
                    "reporte_id": resultado["reporte_id"]
                })
            else:
                return jsonify({
                    "success": False,
                    "error": resultado["error"]
                })
                
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            })

    return render_template('crear_reporte.html')

@app.route('/actualizar_producto', methods=['GET', 'POST'])
@login_required
def actualizar_producto():
    if request.method == 'POST':
        product_id = request.form.get('product-id')
        
        # Crear diccionario solo con los campos que tienen valor
        update_data = {}
        if request.form.get('tipo-producto'):
            update_data['tipo-producto'] = request.form.get('tipo-producto')
        if request.form.get('modelo'):
            update_data['modelo'] = request.form.get('modelo')
        if request.form.get('num-serie'):
            update_data['num-serie'] = request.form.get('num-serie')

        try:
            if ControladorProductos.actualizar_producto(product_id, update_data):
                flash("Producto actualizado correctamente", "success")
            else:
                flash("No se pudo actualizar el producto", "error")
        except Exception as e:
            flash(f"Error al actualizar el producto: {e}", "danger")
        
        return redirect(url_for('administrador'))
    
    return render_template('actualizar_producto.html')

@app.route('/obtener_producto', methods=['POST'])
def obtener_producto():
    try:
        data = request.get_json()
        id_producto = data.get('id_producto')
        
        if not id_producto:
            return jsonify({'error': 'ID de producto no proporcionado'}), 400
        
        producto = ControladorProductos.obtener_producto_por_id(id_producto)
        if producto:
            return jsonify(producto)
        else:
            return jsonify({'error': 'Producto no encontrado'}), 404
    except Exception as e:
        print(f"Error en obtener_producto: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/filtrar-productos')
@login_required
def filtrar_productos_view():
    return render_template('filtrado_productos.html')

@app.route('/api/filtrar-productos', methods=['POST'])
@login_required
def filtrar_productos():
    try:
        data = request.get_json()
        
        # Obtener los parámetros del request
        numero_serie = data.get('numeroSerie')
        tipo_defecto = data.get('tipoDefecto')
        tipo_producto = data.get('tipoProducto')
        
        # Llamar al controlador para obtener los productos filtrados
        productos = ControladorFiltrado.filtrar_productos(
            numero_serie=numero_serie,
            tipo_defecto=tipo_defecto,
            tipo_producto=tipo_producto
        )
        
        return jsonify(productos)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada con éxito", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
