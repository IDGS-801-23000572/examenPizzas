from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Pizzas(db.Model):
    __tablename__='pizzas'
    id_pizza = db.Column(db.Integer, primary_key=True)
    tamano = db.Column(db.String(20))
    ingredientes = db.Column(db.String(200))
    precio = db.Column(db.Numeric(8,2))   
    pedidos = db.relationship(
        'Pedidos', 
        secondary='detallesPedido',
        back_populates='pizza'
        )

class Clientes(db.Model):
    __tablename__='clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(20))
    pedidos = db.relationship(
        'Pedidos', 
        back_populates='cliente'
        )

class Pedidos(db.Model):
    __tablename__='pedidos'
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(
        db.Integer,
        db.ForeignKey('clientes.id_cliente'),
        nullable=False)
    cliente = db.relationship('Clientes', back_populates='pedidos')
    pizza = db.relationship('Pizzas', secondary='detallesPedido', back_populates='pedidos')
    fecha = db.Column(db.DateTime, default=datetime.datetime.now) 
    total = db.Column(db.Numeric(10,2))


class Detalles(db.Model):
    __tablename__ = 'detallesPedido'
    id_detalle = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(
        db.Integer,
        db.ForeignKey('pedidos.id_pedido'),
        nullable=False)
    id_pizza = db.Column(
        db.Integer,
        db.ForeignKey('pizzas.id_pizza'),
        nullable=False)
    cantidad = db.Column(db.Integer)
    subtotal = db.Column(db.Numeric(10,2))
    pizza = db.relationship('Pizzas', foreign_keys=[id_pizza])

    __table_args__ = (
        db.UniqueConstraint('id_pedido', 'id_pizza', name='uq_pedido_pizza'),
    )
