from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf.csrf import CSRFProtect
from config import DevelopmentConfig
from models import db, Pizzas, Clientes, Pedidos, Detalles
from forms import PizzaForm
from flask_migrate import Migrate
import datetime

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect(app)
db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/pedidos", methods=['GET', 'POST'])
def registrarPizza():
    form = PizzaForm()
    if 'carrito' not in session:
        session['carrito'] = []
    if request.method == 'POST' and "agregar" in request.form:
        if form.validate_on_submit():
            session['cliente'] = {
				'nombre': form.nombre.data,
				'direccion': form.direccion.data,
				'telefono': form.telefono.data,
				'fecha': form.fecha.data.strftime('%Y-%m-%d')
			}
            precio_base = float(form.tamano.data)
            num_ingredientes = len(form.ingredientes.data)
            subtotal = (precio_base + (num_ingredientes * 10)) * form.cantidad.data
            nueva_pizza = {
                'tamano_val': form.tamano.data,
                'tamano_label': dict(form.tamano.choices).get(form.tamano.data),
                'ingredientes': ", ".join(form.ingredientes.data),
                'cantidad': form.cantidad.data,
                'subtotal': subtotal
            }
            
            carrito = session['carrito']
            carrito.append(nueva_pizza)
            session['carrito'] = carrito
            flash('Pizza agregada al detalle', 'success')
            return redirect(url_for('registrarPizza'))
    total_pedido = sum(item['subtotal'] for item in session['carrito'])
    
    return render_template("pedidos.html", form=form, carrito=session['carrito'], total=total_pedido)

@app.route("/quitar/<int:id>", methods=['POST'])
def quitarPizza(id):
    carrito = session.get('carrito', [])
    if 0 <= id < len(carrito):
        carrito.pop(id)
        session['carrito'] = carrito
        flash('Pizza eliminada del detalle', 'warning')
    return redirect(url_for('registrarPizza'))

@app.route("/terminar", methods=['POST'])
def terminarPedido():
    carrito = session.get('carrito', [])
    cliente_data = session.get('cliente', {})

    if not carrito or not cliente_data:
        flash('Faltan datos del pedido', 'danger')
        return redirect(url_for('registrarPizza'))

    try:
        cliente = Clientes(
            nombre=cliente_data['nombre'],
            direccion=cliente_data['direccion'],
            telefono=cliente_data['telefono']
        )
        db.session.add(cliente)
        db.session.flush()

        total_final = sum(item['subtotal'] for item in carrito)
        nuevo_pedido = Pedidos(
            id_cliente=cliente.id_cliente,
            fecha=datetime.datetime.strptime(cliente_data['fecha'], '%Y-%m-%d'),
            total=total_final
        )
        db.session.add(nuevo_pedido)
        db.session.flush()

        for item in carrito:
            p = Pizzas(
                tamano=item['tamano_label'],
                ingredientes=item['ingredientes'],
                precio=item['subtotal'] / item['cantidad']
            )
            db.session.add(p)
            db.session.flush()

            d = Detalles(
                id_pedido=nuevo_pedido.id_pedido,
                id_pizza=p.id_pizza,
                cantidad=item['cantidad'],
                subtotal=item['subtotal']
            )
            db.session.add(d)

        db.session.commit()
        session.pop('carrito', None)
        session.pop('cliente', None)
        flash('¡Pedido registrado con éxito!', 'success')
        return redirect(url_for('registrarPizza'))

    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar el pedido: {e}', 'danger')
        return redirect(url_for('registrarPizza'))






@app.route("/consultas")
def func():
	return render_template("consultas.html")


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html')

if __name__ == '__main__':
	csrf.init_app(app)
	with app.app_context():
		db.create_all()
	app.run(debug=True)