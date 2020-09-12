from wtforms import Form,StringField,TextAreaField,PasswordField,SubmitField,validators,ValidationError
from flask_wtf.file import FileRequired,FileAllowed,FileField
from flask_wtf import FlaskForm
from .model import Register


class CustomerRegisterForm(FlaskForm):
	name=StringField('Nombre:')
	username=StringField('Nombre de usuario:',[validators.DataRequired()])
	email=StringField('Correo:',[validators.Email(),validators.DataRequired()])
	password=PasswordField('Constraseña:',[validators.DataRequired(),validators.EqualTo('confirm',
	message='Las Constraseñas deben coincidir')])
	confirm=PasswordField('Repite la constraseña',[validators.DataRequired()])
	state=StringField('Estado:',[validators.DataRequired()])
	city=StringField('Ciudad',[validators.DataRequired()])
	contact=StringField('Contacto:',[validators.DataRequired()])
	address=StringField('Direccion:',[validators.DataRequired()])
	zipcode=StringField('código postal:',[validators.DataRequired()])
	profile=FileField('profile',validators=[FileAllowed(['jpg','png','jpeg','gif'])])
	submit=SubmitField('Registrar')


def validate_username(self,username):
	if Register.query.filter_by(username=username.data).first():
		raise ValidationError("Este nombre de usuario ya esta usado")

def validate_email(self, email):
	if Register.query.filter_by(email=email.data).first():
		raise ValidationError("Este Correo  ya esta usado")


class CustomerLoginForm(FlaskForm):
	email=StringField('Correo:',[validators.Email(),validators.DataRequired()])
	password=PasswordField('Constraseña:',[validators.DataRequired()])



