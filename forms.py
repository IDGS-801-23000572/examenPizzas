from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, SelectMultipleField, IntegerField, DateField, widgets
from wtforms.validators import DataRequired, NumberRange

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class PizzaForm(FlaskForm):
    nombre = StringField('Nombre completo', validators=[DataRequired()])
    direccion = StringField('Dirección', validators=[DataRequired()])
    telefono = StringField('Teléfono', validators=[DataRequired()])
    fecha = DateField('Fecha', format='%Y-%m-%d', validators=[DataRequired()])
    tamano = RadioField('Tamaño', choices=[
        ('40', 'CH ($40)'),
        ('80', 'MD ($80)'),
        ('120', 'GD ($120)')
    ], validators=[DataRequired()])
    ingredientes = MultiCheckboxField('Ingredientes (+$10)', choices=[
        ('Jamón', 'Jamón'),
        ('Piña', 'Piña'),
        ('Champi', 'Champi')
    ])
    cantidad = IntegerField('Cantidad', default=1, validators=[DataRequired(), NumberRange(min=1)])