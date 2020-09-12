from wtforms import Form, SubmitField,IntegerField,DecimalField,FloatField,StringField,TextAreaField,validators,BooleanField,DecimalField
from flask_wtf.file import FileField,FileRequired,FileAllowed
from shop import db

class Addproducts(Form):
    name = StringField('Producto', [validators.DataRequired()])
    price = DecimalField('Precio', [validators.DataRequired()])
    discount = IntegerField('Descuento', default=0)
    stock=IntegerField('Cantidad',[validators.DataRequired()])
    color = TextAreaField('Colores', [validators.DataRequired()])
    discription = TextAreaField('Descripcion', [validators.DataRequired()])
    image_1 = FileField('Imagen 1', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    image_2 = FileField('Imagen 2', validators=[ FileAllowed(['jpg','png','gif','jpeg'])])
    image_3 = FileField('Imagen 3', validators=[ FileAllowed(['jpg','png','gif','jpeg'])])


class Vendedores(Form):
    name = StringField('Nombre del vendedor', [validators.DataRequired()])
    apellidop = StringField('Apellido Patero', [validators.DataRequired()])
    apellidom = StringField('Apellido Matero', [validators.DataRequired()])
    edad = StringField('Edad', [validators.DataRequired()])
    telefono = StringField('Telefono', [validators.DataRequired()])
    calle = StringField('Calle', [validators.DataRequired()])
    colonia = StringField('Colonia', [validators.DataRequired()])
    numdire = StringField('# de direccion', [validators.DataRequired()])
    image_1 = FileField('Imagen 1', validators=[FileAllowed(['jpg','png','gif','jpeg'])])


class Dueños(Form):
    name = StringField('Nombre del Dueño', [validators.DataRequired()])
    apellidop = StringField('Apellido Patero', [validators.DataRequired()])
    apellidom = StringField('Apellido Matero', [validators.DataRequired()])
    edad = StringField('edad', [validators.DataRequired()])
    telefono = StringField('telefono', [validators.DataRequired()])
    calle = StringField('calle', [validators.DataRequired()])
    colonia = StringField('colonia', [validators.DataRequired()])
    numdire = StringField('# de direccion', [validators.DataRequired()])
    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg','png','gif','jpeg'])])



class Administradores(Form):
    name = StringField('Nombre del Administrador', [validators.DataRequired()])
    apellidop = StringField('Apellido Patero', [validators.DataRequired()])
    apellidom = StringField('Apellido Matero', [validators.DataRequired()])
    edad = StringField('edad', [validators.DataRequired()])
    telefono = StringField('telefono', [validators.DataRequired()])
    calle = StringField('calle', [validators.DataRequired()])
    colonia = StringField('colonia', [validators.DataRequired()])
    numdire = StringField('# de direccion', [validators.DataRequired()])
    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg','png','gif','jpeg'])])
    


class Clientes(Form):
    name = StringField('Nombre del Cliente', [validators.DataRequired()])
    apellidop = StringField('Apellido Patero', [validators.DataRequired()])
    apellidom = StringField('Apellido Matero', [validators.DataRequired()])
    edad = StringField('edad', [validators.DataRequired()])
    telefono = StringField('telefono', [validators.DataRequired()])
    calle = StringField('calle', [validators.DataRequired()])
    colonia = StringField('colonia', [validators.DataRequired()])
    numdire = StringField('# de direccion', [validators.DataRequired()])
    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg','png','gif','jpeg'])])

    
class Ventas(Form):
    name = StringField('fecha', [validators.DataRequired()])
    precio = StringField('precio', [validators.DataRequired()])
    total = StringField('total', [validators.DataRequired()])
    




